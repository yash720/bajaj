import re
import json
import nltk
import os
import pdfplumber
from docx import Document
from email import parser, policy
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, M2M100ForConditionalGeneration, M2M100Tokenizer
from pdf2image import convert_from_path
import pytesseract
import logging
import fasttext
from cachetools import LRUCache
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Also enable print statements for immediate visibility
import sys
def print_log(message):
    """Print message to both console and log"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    logger.info(message)

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize models
embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
llm = pipeline("text2text-generation", model="google/flan-t5-base", max_length=200, device=-1)

# Load fasttext language detection model
FASTTEXT_MODEL_PATH = "lid.176.bin"
if not os.path.exists(FASTTEXT_MODEL_PATH):
    raise FileNotFoundError(f"FastText model not found at {FASTTEXT_MODEL_PATH}. Download it from https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin and place it in the project root.")
lang_detector = fasttext.load_model(FASTTEXT_MODEL_PATH)

# Initialize M2M100 translation model
translator_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
translator_tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
translation_cache = LRUCache(maxsize=1000)

# Supported languages
supported_languages = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'hi': 'Hindi',
    'zh': 'Chinese', 'ar': 'Arabic', 'ru': 'Russian', 'ja': 'Japanese', 'pt': 'Portuguese',
    'it': 'Italian', 'ko': 'Korean', 'bn': 'Bengali', 'ta': 'Tamil', 'te': 'Telugu'
}

ocr_cache = LRUCache(maxsize=10)
embedding_cache = LRUCache(maxsize=10)

def detect_language(text):
    """Detect language of text using fasttext."""
    try:
        text = text.replace('\n', ' ')[:1000]  # Limit text for faster detection
        predictions = lang_detector.predict(text, k=1)
        lang = predictions[0][0].replace('_label_', '')
        return lang if lang in supported_languages else 'en'
    except Exception as e:
        logging.error(f"Language detection failed: {e}, defaulting to English.")
        return 'en'

def translate_text(texts, target_lang, src_lang='en'):
    """Batch translate texts to target language using M2M100."""
    if not texts or target_lang == src_lang:
        return texts if isinstance(texts, list) else [texts]
    
    results = []
    uncached_texts = []
    uncached_indices = []
    
    # Check cache for translations
    if isinstance(texts, list):
        for i, text in enumerate(texts):
            cache_key = (text, target_lang)
            if cache_key in translation_cache:
                results.append(translation_cache[cache_key])
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
    else:
        cache_key = (texts, target_lang)
        if cache_key in translation_cache:
            return translation_cache[cache_key]
        uncached_texts.append(texts)
        uncached_indices.append(0)

    if uncached_texts:
        try:
            translator_tokenizer.src_lang = src_lang
            inputs = translator_tokenizer(uncached_texts, return_tensors="pt", padding=True, truncation=True)
            outputs = translator_model.generate(**inputs, forced_bos_token_id=translator_tokenizer.get_lang_id(target_lang))
            translated = translator_tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            # Update cache and results
            for i, text, translated_text in zip(uncached_indices, uncached_texts, translated):
                cache_key = (text, target_lang)
                translation_cache[cache_key] = translated_text
                if isinstance(texts, list):
                    results.insert(i, translated_text)
                else:
                    return translated_text
        except Exception as e:
            logging.error(f"Translation failed for {uncached_texts} to {target_lang}: {e}")
            if isinstance(texts, list):
                results.extend(uncached_texts)  # Fallback to original texts
            else:
                return texts

    return results if isinstance(texts, list) else results[0]

def extract_text_from_image(pdf_path, lang='eng'):
    """Extract text from scanned PDFs using OCR with downsampling."""
    cache_key = (pdf_path, lang)
    if cache_key in ocr_cache:
        return ocr_cache[cache_key]
    
    try:
        images = convert_from_path(pdf_path, dpi=200)  # Reduced DPI for speed
        text = ""
        for image in images:
            image = image.resize((int(image.width * 0.5), int(image.height * 0.5)), Image.Resampling.LANCZOS)  # Downsample
            text += pytesseract.image_to_string(image, lang=lang) + "\n"
        text = text.strip()
        ocr_cache[cache_key] = text
        return text
    except Exception as e:
        logging.error(f"OCR extraction failed for {pdf_path}: {e}")
        return ""

def extract_text_from_pdf(file_path, doc_lang='eng'):
    """Extract text from PDF using pdfplumber with OCR fallback."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text(layout=True) or ""
                if not page_text.strip():
                    logging.info(f"Performing OCR on page {page.page_number} of {file_path} with lang={doc_lang}")
                    image = page.to_image(resolution=200).original  # Reduced resolution
                    page_text = pytesseract.image_to_string(image, lang=doc_lang)
                text += page_text + "\n"
            return text.strip()
    except Exception as e:
        logging.warning(f"pdfplumber failed for {file_path}: {e}. Attempting OCR.")
        return extract_text_from_image(file_path, doc_lang)

def extract_text_from_docx(file_path):
    """Extract text from Word (.docx) document."""
    try:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    except Exception as e:
        logging.error(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_text_from_email(file_path):
    """Extract text from email (.eml) file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            msg = parser.BytesParser(policy=policy.default).parse(f)
            if msg.is_multipart():
                text = "".join(
                    part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    for part in msg.walk() if part.get_content_type() == 'text/plain'
                )
            else:
                text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return text.strip()
    except Exception as e:
        logging.error(f"Error reading email {file_path}: {e}")
        return ""

def extract_text(file_path, doc_lang='eng'):
    """Extract text from supported document formats."""
    ext = os.path.splitext(file_path)[1].lower()
    logging.info(f"Extracting text from {file_path} with extension '{ext}'")
    
    # If no extension, try to read as text file
    if not ext:
        logging.info(f"No extension found, treating as text file")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logging.info(f"Read {len(content)} characters from text file")
                return content
        except Exception as e:
            logging.error(f"Error reading file without extension {file_path}: {e}")
            return ""
    
    try:
        if ext == '.pdf':
            return extract_text_from_pdf(file_path, doc_lang)
        elif ext == '.docx':
            return extract_text_from_docx(file_path)
        elif ext == '.eml':
            return extract_text_from_email(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logging.info(f"Read {len(content)} characters from text file")
                return content
        else:
            logging.error(f"Unsupported file format: {ext}")
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return ""

# Compiled regex for faster matching
section_splitter = re.compile(r'\n\s*(\d+\.\s+|[A-Z]\.\s+|[i|ii|iii|iv|v|vi|vii|viii|ix|x]+\.\s+|[-*•]\s+)', re.IGNORECASE)
clause_splitter = re.compile(r'^\s*[\da-zA-Z]\)\s|^\s*[-*•]\s', re.IGNORECASE)
footer_cleaner = re.compile(r'(Page \d+ of \d+\n?|© \d{4}.?\n|Edelweiss General Insurance Co.?(?=\n\s*\n|\Z)|UIN:.?(\n|$)|Reach us on|IRDAI Regn\.|CIN:|Email:|Website:|Issuing/Corporate Office:|Grievance Redressal Officer:|Toll-Free Number).?(\n|$)', re.IGNORECASE | re.DOTALL)

def clean_text(text):
    """Clean text by removing artifacts and footer content."""
    text = footer_cleaner.sub('', text)
    text = re.sub(r'(\d+,\s*)+', '', text)
    text = re.sub(r'(\n\s*){2,}', '\n', text)
    text = re.sub(r'^(From|Subject|To|Date):.*?\n', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'\b(iv\s*){2,}', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'(We will also cover\n)+', 'We will also cover\n', text)
    return text.strip()

def parse_document(file_path, doc_lang='eng'):
    """Parse document into unique, complete clauses with metadata."""
    text = clean_text(extract_text(file_path, doc_lang))
    logging.info(f"Raw text length: {len(text) if text else 0}")
    if not text:
        logging.warning(f"No text extracted from {file_path}")
        return []

    # Process clauses in chunks
    sections = section_splitter.split(text)
    clauses = []
    seen_clauses = set()
    current_clause = ""
    max_clauses = 1000  # Limit to prevent memory overload
    
    for section in sections:
        if section.strip() and len(clauses) < max_clauses:
            section_clauses = []
            for line in section.split('\n'):
                if clause_splitter.match(line):
                    if current_clause:
                        section_clauses.append(current_clause.strip())
                        current_clause = ""
                    section_clauses.append(line.strip())
                else:
                    current_clause += " " + line.strip()
            if current_clause:
                section_clauses.append(current_clause.strip())
                current_clause = ""
            for clause in section_clauses:
                clause = clause.strip()
                if (clause and clause not in seen_clauses and len(clause) > 15 and
                    not re.search(r'(UIN|Edelweiss General Insurance|Reach us on|IRDAI|CIN:|Email:|Website:)', clause, re.IGNORECASE)):
                    seen_clauses.add(clause)
                    clauses.append((clause, {"file": os.path.basename(file_path), "position": len(clauses)}))
                    if len(clauses) >= max_clauses:
                        break

    if file_path not in embedding_cache:
        clause_texts = [clause[0] for clause in clauses]
        if clause_texts:
            embeddings = embedder.encode(clause_texts, convert_to_tensor=True, device='cpu', batch_size=32)  # Batch processing
            embedding_cache[file_path] = embeddings
    return clauses

def parse_query(query, query_lang):
    """Extract key entities from query using regex and LLM fallback, translating to English if needed."""
    if query_lang != 'en':
        query = translate_text(query, 'en', query_lang)

    patterns = {
        "age": r'(\d{1,3}|\b(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\b[-\s]?\b(?:one|two|three|four|five|six|seven|eight|nine)?\b)',
        "gender": r'[MmFf]|male|female|homme|femme|mujer|hombre|पुरुष|महिला',
        "procedure": r'([a-zA-Z\s]+(?:surgery|procedure|care|soins|cirugía|देखभाल))',
        "location": r'(?<!\d[MmFf])([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+))(?=\s(?:,|$|\d-month))',
        "policy_duration": r'(\d{1,2})-month\s*(?:policy|insurance|póliza|police)?'
    }

    extracted = {
        "age": None, "gender": None, "procedure": None, "location": None, "policy_duration": None
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            if key == "gender":
                extracted[key] = "Male" if match.group(0).lower() in ['m', 'male', 'homme', 'hombre', 'पुरुष'] else "Female"
            elif key == "procedure":
                extracted[key] = match.group(1).strip()
            elif key == "location":
                extracted[key] = match.group(1)
            else:
                extracted[key] = match.group(1)

    if not all(extracted.values()):
        prompt = f"""Extract from query '{query}' the following entities and return as JSON:
        - Age (number, e.g., 32 or 'thirty-two' as 32)
        - Gender (Male/Female)
        - Procedure (e.g., maternity care)
        - Location (e.g., city like Mumbai, not the procedure)
        - Policy Duration (e.g., number of months like 6)
        Ensure Location is a geographical place, not the procedure. Prioritize the city name before the policy duration. Return:
        json
        {{
            "age": null,
            "gender": null,
            "procedure": null,
            "location": null,
            "policy_duration": null
        }}
        """
        try:
            response = llm(prompt)[0]['generated_text']
            llm_extracted = json.loads(response)
            for key, value in llm_extracted.items():
                if not extracted[key] and value:
                    extracted[key] = str(value)
        except Exception as e:
            logging.warning(f"LLM query parsing failed: {e}")

    return extracted

def search_clauses(query, clauses, file_path):
    """Retrieve relevant clauses using semantic search with fallback."""
    if not clauses:
        return []

    query_embedding = embedder.encode(query, convert_to_tensor=True, device='cpu')
    clause_embeddings = embedding_cache.get(file_path, embedder.encode([clause[0] for clause in clauses], convert_to_tensor=True, device='cpu', batch_size=32))

    similarities = util.cos_sim(query_embedding, clause_embeddings)[0]
    top_k = min(3, len(clauses))
    top_indices = torch.argsort(similarities, descending=True)[:top_k]
    results = [(clauses[i], similarities[i].item()) for i in top_indices if similarities[i] > 0.5]
    if not results:
        results = [(clauses[i], similarities[i].item()) for i in top_indices if similarities[i] > 0.3]
    return results

def evaluate_decision(query_details, relevant_clauses, query):
    """Evaluate decision based on query and clauses."""
    procedure = query_details.get("procedure", "").lower()
    policy_duration = int(query_details.get("policy_duration", 0)) if query_details.get("policy_duration") else 0
    is_accident = "accident" in procedure or "accident" in query.lower()
    is_maternity = "maternity" in procedure.lower() or "baby" in procedure.lower()

    decision = {
        "Decision": "Rejected",
        "Amount": None,
        "Justification": "No relevant coverage found or policy duration insufficient."
    }

    for clause, _ in relevant_clauses:
        clause_text = clause[0].lower()
        if "dental surgery" in clause_text and "outside india" in clause_text:
            continue
        if any(term in clause_text for term in [procedure, "maternity care", "well mother care", "well baby care"]) and "waiting period" in clause_text:
            waiting_period = int(re.search(r'(\d{1,2})-month', clause_text).group(1)) if re.search(r'(\d{1,2})-month', clause_text) else 36
            if policy_duration < waiting_period:
                decision.update({
                    "Decision": "Rejected",
                    "Amount": None,
                    "Justification": f"Clause: '{clause[0]}' - {procedure.title()} has a {waiting_period}-month waiting period; policy duration is {policy_duration} months."
                })
                return decision
        if "pre-existing" in clause_text and "waiting period" in clause_text:
            waiting_period = int(re.search(r'(\d{1,2})-month', clause_text).group(1)) if re.search(r'(\d{1,2})-month', clause_text) else 36
            if policy_duration < waiting_period:
                decision.update({
                    "Decision": "Rejected",
                    "Amount": None,
                    "Justification": f"Clause: '{clause[0]}' - Pre-existing condition excluded for {waiting_period} months; policy duration is {policy_duration} months."
                })
                return decision
        if "waiting period" in clause_text and re.search(r'(\d{1,2})-day', clause_text):
            waiting_period_days = int(re.search(r'(\d{1,2})-day', clause_text).group(1))
            if policy_duration * 30 < waiting_period_days:
                decision.update({
                    "Decision": "Rejected",
                    "Amount": None,
                    "Justification": f"Clause: '{clause[0]}' - {waiting_period_days}-day waiting period applies; policy duration is {policy_duration} months."
                })
                return decision
        if is_accident and "accident" in clause_text and "waiting period" not in clause_text:
            decision.update({
                "Decision": "Approved",
                "Amount": 500000,
                "Justification": f"Clause: '{clause[0]}' - Accident-related procedure covered without waiting period."
            })
            return decision
        if is_maternity and any(term in clause_text for term in ["maternity", "well mother care", "routine medical care", "preventive care", "immunizations"]):
            decision.update({
                "Decision": "Approved",
                "Amount": 500000,
                "Justification": f"Clause: '{clause[0]}' - {procedure.title()} covered under maternity or well mother care for a {policy_duration}-month policy."
            })
            return decision
        if "inpatient" in clause_text and ("covered" in clause_text or "sum insured" in clause_text):
            decision.update({
                "Decision": "Approved",
                "Amount": 500000,
                "Justification": f"Clause: '{clause[0]}' - {procedure.title()} covered under inpatient hospitalization for a {policy_duration}-month policy."
            })
            return decision

    return decision

def process_query(query, document_path):
    """Process query and return structured JSON response in the query's language."""
    print_log("=" * 60)
    print_log("STARTING CLAIM PROCESSING")
    print_log("=" * 60)
    print_log(f"Query: {query}")
    print_log(f"Document path: {document_path}")
    
    query_lang = detect_language(query)
    print_log(f"Detected query language: {supported_languages.get(query_lang, 'English')}")

    doc_text = extract_text(document_path, 'eng')  # Initial extraction for language detection
    doc_lang = detect_language(doc_text) if doc_text else 'eng'
    print_log(f"Detected document language: {doc_lang}")
    print_log(f"Document text length: {len(doc_text) if doc_text else 0}")

    if not os.path.exists(document_path):
        error_msg = translate_text("Document not found", query_lang)
        print_log(f"ERROR: Document not found: {document_path}")
        return {"error": error_msg}

    print_log("Extracting clauses from document...")
    clauses = parse_document(document_path, doc_lang)
    print_log(f"Number of clauses extracted: {len(clauses)}")
    if not clauses:
        error_msg = translate_text("No content extracted from document", query_lang)
        print_log(f"ERROR: No clauses extracted from {document_path}")
        return {"error": error_msg}

    print_log("Parsing query details...")
    query_details = parse_query(query, query_lang)
    print_log(f"Query details: {query_details}")

    print_log("Searching for relevant clauses...")
    relevant_clauses = search_clauses(query, clauses, document_path)
    print_log(f"Found {len(relevant_clauses)} relevant clauses")

    print_log("Evaluating decision...")
    decision = evaluate_decision(query_details, relevant_clauses, query)
    print_log(f"Decision: {decision['Decision']}")
    print_log(f"Amount: {decision['Amount']}")
    print_log(f"Justification: {decision['Justification'][:100]}...")

    # Batch translate all textual fields
    print_log("Translating results...")
    texts_to_translate = [
        query_details["gender"],
        query_details["procedure"],
        query_details["location"],
        decision["Decision"],
        decision["Justification"]
    ] + [clause[0] for clause, _ in relevant_clauses]
    texts_to_translate = [t for t in texts_to_translate if t]  # Remove None
    translated_texts = translate_text(texts_to_translate, query_lang) if texts_to_translate else []
    
    # Assign translated texts safely
    translated_idx = 0
    response = {
        "QueryDetails": {
            "age": query_details["age"],
            "gender": translated_texts[translated_idx] if query_details["gender"] and translated_idx < len(translated_texts) else query_details["gender"],
            "procedure": translated_texts[translated_idx + 1] if query_details["procedure"] and translated_idx + 1 < len(translated_texts) else query_details["procedure"],
            "location": translated_texts[translated_idx + 2] if query_details["location"] and translated_idx + 2 < len(translated_texts) else query_details["location"],
            "policy_duration": query_details["policy_duration"]
        },
        "Decision": translated_texts[translated_idx + 3] if translated_idx + 3 < len(translated_texts) else decision["Decision"],
        "Amount": decision["Amount"],
        "Justification": translated_texts[translated_idx + 4] if translated_idx + 4 < len(translated_texts) else decision["Justification"],
        "RelevantClauses": [
            {
                "text": clause[0],
                "source": clause[1]["file"],
                "position": clause[1]["position"]
            } for clause, _ in relevant_clauses
        ] if relevant_clauses else []
    }
    
    print_log("=" * 60)
    print_log("FINAL RESPONSE")
    print_log("=" * 60)
    print_log(f"Decision: {response['Decision']}")
    print_log(f"Amount: {response['Amount']}")
    print_log(f"RelevantClauses count: {len(response['RelevantClauses'])}")
    print_log(f"QueryDetails: {response['QueryDetails']}")
    print_log("=" * 60)
    
    return response

# At the end, add FastAPI app and endpoint
app = FastAPI()

@app.post("/process")
async def process(query: str = Form(...), file: UploadFile = File(...)):
    print_log("=" * 60)
    print_log("NEW REQUEST RECEIVED")
    print_log("=" * 60)
    print_log(f"Query: {query}")
    print_log(f"File: {file.filename}")
    print_log(f"File size: {file.size if hasattr(file, 'size') else 'Unknown'} bytes")
    
    # Create a temporary file with proper extension
    file_extension = os.path.splitext(file.filename)[1] if file.filename else '.txt'
    if not file_extension:
        file_extension = '.txt'
    
    file_location = f"temp_{file.filename or 'document'}{file_extension}"
    
    try:
        # Write file content
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print_log(f"File saved: {file_location}, size: {len(content)} bytes")
        
        # Process the query
        print_log("Starting query processing...")
        result = process_query(query, file_location)
        
        # Clean up
        if os.path.exists(file_location):
            os.remove(file_location)
            print_log(f"Temporary file removed: {file_location}")
        
        print_log("=" * 60)
        print_log("REQUEST COMPLETED SUCCESSFULLY")
        print_log("=" * 60)
        return JSONResponse(content=result)
    except Exception as e:
        print_log(f"ERROR in process_query: {e}")
        # Clean up on error
        if os.path.exists(file_location):
            os.remove(file_location)
        result = {"error": str(e)}
        return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)