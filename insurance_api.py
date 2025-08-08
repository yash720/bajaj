#!/usr/bin/env python3
"""
Insurance Claims Processing System
A complete multilingual system for processing insurance claims with document analysis.
"""

import re
import json
import nltk
import os
import pdfplumber
from docx import Document
from email import parser, policy
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from pdf2image import convert_from_path
import pytesseract
import logging
from langdetect import detect, DetectorFactory
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from pathlib import Path
import tempfile
import shutil
from typing import Optional, Dict, Any
from dataclasses import dataclass
from PIL import Image

# Ensure consistent language detection
DetectorFactory.seed = 0

# Configuration class
@dataclass
class Config:
    """Configuration settings for the insurance claims system."""
    # Model settings
    EMBEDDER_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "google/flan-t5-base"
    
    # Language settings
    SUPPORTED_LANGUAGES: Dict[str, str] = None
    
    # Business rules
    DEFAULT_COVERAGE: int = 500000
    DEFAULT_WAITING_PERIOD: int = 36
    
    # Processing thresholds
    SIMILARITY_PRIMARY: float = 0.5
    SIMILARITY_FALLBACK: float = 0.3
    MIN_CLAUSE_LENGTH: int = 20
    MAX_CLAUSES: int = 1000
    TOP_K_CLAUSES: int = 3
    
    # OCR settings
    PDF_DPI: int = 200
    EMBEDDING_BATCH_SIZE: int = 32
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    def __post_init__(self):
        if self.SUPPORTED_LANGUAGES is None:
            self.SUPPORTED_LANGUAGES = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 
                'de': 'German', 'hi': 'Hindi', 'zh': 'Chinese', 
                'ar': 'Arabic', 'ru': 'Russian', 'ja': 'Japanese', 
                'pt': 'Portuguese', 'it': 'Italian', 'ko': 'Korean'
            }

# Initialize configuration
config = Config()

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('insurance_claims.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InsuranceClaimsProcessor:
    """Main class for processing insurance claims."""
    
    def __init__(self):
        self.embedder = None
        self.llm = None
        self.translation_models = {}
        self.embedding_cache = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all required models."""
        try:
            # Download NLTK data
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
            
            # Initialize embedder
            logger.info("Loading sentence transformer model...")
            self.embedder = SentenceTransformer(config.EMBEDDER_MODEL, device='cpu')
            
            # Initialize LLM
            logger.info("Loading language model...")
            self.llm = pipeline(
                "text2text-generation", 
                model=config.LLM_MODEL, 
                max_length=200, 
                device=-1  # Use CPU
            )
            
            logger.info("Models initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            raise
    
    def detect_language(self, text: str) -> str:
        """Detect language of text with fallback options."""
        try:
            if not text or len(text.strip()) < 3:
                return 'en'
            
            # Clean and limit text for detection
            text = re.sub(r'[^\w\s]', ' ', text)
            text = text.replace('\n', ' ')[:1000]
            
            detected_lang = detect(text)
            
            # Map some common variations
            lang_mapping = {
                'zh-cn': 'zh', 'zh-tw': 'zh'
            }
            detected_lang = lang_mapping.get(detected_lang, detected_lang)
            
            return detected_lang if detected_lang in config.SUPPORTED_LANGUAGES else 'en'
            
        except Exception as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English.")
            return 'en'
    
    def get_translator(self, target_lang: str):
        """Load or reuse translation model for target language."""
        if target_lang not in config.SUPPORTED_LANGUAGES or target_lang == 'en':
            return None
        
        if target_lang not in self.translation_models:
            try:
                model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
                logger.info(f"Loading translation model for {target_lang}...")
                
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                self.translation_models[target_lang] = pipeline(
                    "translation", 
                    model=model, 
                    tokenizer=tokenizer, 
                    device=-1
                )
                
                logger.info(f"Translation model for {target_lang} loaded successfully!")
                
            except Exception as e:
                logger.error(f"Failed to load translation model for {target_lang}: {e}")
                return None
        
        return self.translation_models[target_lang]
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'en') -> str:
        """Translate text to target language."""
        if not text or target_lang == source_lang or target_lang == 'en':
            return text
        
        translator = self.get_translator(target_lang)
        if translator:
            try:
                # Handle long texts by splitting them
                if len(text) > 500:
                    sentences = text.split('. ')
                    translated_parts = []
                    for sentence in sentences:
                        if sentence.strip():
                            result = translator(sentence.strip())[0]['translation_text']
                            translated_parts.append(result)
                    return '. '.join(translated_parts)
                else:
                    return translator(text)[0]['translation_text']
                    
            except Exception as e:
                logger.error(f"Translation failed for '{text[:50]}...' to {target_lang}: {e}")
        
        return text
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using pdfplumber with OCR fallback."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text(layout=True) or ""
                        if not page_text.strip():
                            logger.info(f"Performing OCR on page {page_num} of {file_path}")
                            image = page.to_image(resolution=config.PDF_DPI).original
                            page_text = pytesseract.image_to_string(image, lang='eng')
                        text += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error processing page {page_num}: {e}")
                        continue
                
                return text.strip()
                
        except Exception as e:
            logger.warning(f"pdfplumber failed for {file_path}: {e}. Attempting full OCR.")
            return self.extract_text_from_image(file_path)
    
    def extract_text_from_image(self, pdf_path: str) -> str:
        """Extract text from scanned PDFs using OCR."""
        try:
            images = convert_from_path(pdf_path, dpi=config.PDF_DPI)
            text = ""
            for i, image in enumerate(images):
                try:
                    # Optimize image for OCR
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    page_text = pytesseract.image_to_string(image, lang='eng')
                    text += page_text + "\n"
                    
                except Exception as e:
                    logger.warning(f"OCR failed for page {i+1}: {e}")
                    continue
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction failed for {pdf_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from Word document."""
        try:
            doc = Document(file_path)
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            return "\n".join(paragraphs)
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path}: {e}")
            return ""
    
    def extract_text_from_email(self, file_path: str) -> str:
        """Extract text from email file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                msg = parser.BytesParser(policy=policy.default).parse(f)
                
                if msg.is_multipart():
                    text_parts = []
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            payload = part.get_payload(decode=True)
                            if payload:
                                text_parts.append(payload.decode('utf-8', errors='ignore'))
                    return "\n".join(text_parts)
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        return payload.decode('utf-8', errors='ignore')
            return ""
            
        except Exception as e:
            logger.error(f"Error reading email {file_path}: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from supported document formats."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif ext == '.docx':
                return self.extract_text_from_docx(file_path)
            elif ext == '.eml':
                return self.extract_text_from_email(file_path)
            elif ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Try to read as text file if no extension
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except:
                    raise ValueError(f"Unsupported file format: {ext}")
                    
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            raise
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing artifacts and footer content."""
        if not text:
            return ""
        
        # Remove common artifacts
        cleaning_patterns = [
            (r'Page \d+ of \d+\n?', ''),
            (r'© \d{4}.*?\n', '\n'),
            (r'Edelweiss General Insurance.*?(?=\n\s*\n|\Z)', ''),
            (r'UIN:.*?(\n|$)', ''),
            (r'(Reach us on|IRDAI|CIN:|Email:|Website:|Toll-Free).*?(\n|$)', ''),
            (r'(\d+,\s*)+', ''),
            (r'(\n\s*){3,}', '\n\n'),
            (r'^(From|Subject|To|Date):.*?\n', ''),
            (r'\b(iv\s*){2,}', ' '),
        ]
        
        for pattern, replacement in cleaning_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()
    
    def parse_document(self, file_path: str) -> list:
        """Parse document into clauses with metadata."""
        text = self.clean_text(self.extract_text(file_path))
        
        if not text:
            logger.warning(f"No text extracted from {file_path}")
            return []
        
        logger.info(f"Extracted {len(text)} characters from document")
        
        # Split into sections
        sections = re.split(r'\n\s*(\d+\.\s+|[A-Z]\.\s+|[ivxlc]+\.\s+)', text, flags=re.IGNORECASE)
        
        clauses = []
        seen_clauses = set()
        
        for section in sections:
            if not section.strip():
                continue
            
            # Split section into potential clauses
            lines = section.split('\n')
            current_clause = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if line starts a new clause
                if re.match(r'^\s*[\da-zA-Z]\)\s|^\s*[-*•]\s', line):
                    if current_clause:
                        self._add_clause(current_clause, clauses, seen_clauses, file_path)
                        current_clause = ""
                    current_clause = line
                else:
                    current_clause += " " + line
            
            # Add the last clause
            if current_clause:
                self._add_clause(current_clause, clauses, seen_clauses, file_path)
        
        logger.info(f"Extracted {len(clauses)} clauses from document")
        
        # Generate embeddings
        if clauses and file_path not in self.embedding_cache:
            clause_texts = [clause[0] for clause in clauses]
            try:
                embeddings = self.embedder.encode(
                    clause_texts, 
                    convert_to_tensor=True, 
                    batch_size=config.EMBEDDING_BATCH_SIZE,
                    device='cpu'
                )
                self.embedding_cache[file_path] = embeddings
                logger.info("Generated embeddings for clauses")
            except Exception as e:
                logger.error(f"Error generating embeddings: {e}")
        
        return clauses
    
    def _add_clause(self, clause_text: str, clauses: list, seen_clauses: set, file_path: str):
        """Add clause if it meets criteria."""
        clause_text = clause_text.strip()
        
        # Filter criteria
        if (clause_text and 
            clause_text not in seen_clauses and 
            len(clause_text) >= config.MIN_CLAUSE_LENGTH and
            not re.search(r'(UIN|IRDAI|CIN:|Email:|Website:)', clause_text, re.IGNORECASE) and
            len(clauses) < config.MAX_CLAUSES):
            
            seen_clauses.add(clause_text)
            clauses.append((
                clause_text, 
                {
                    "file": os.path.basename(file_path), 
                    "position": len(clauses),
                    "length": len(clause_text)
                }
            ))
    
    def parse_query(self, query: str, query_lang: str) -> Dict[str, Any]:
        """Extract entities from query."""
        # Translate to English for processing
        if query_lang != 'en':
            english_query = self.translate_text(query, 'en', query_lang)
        else:
            english_query = query
        
        patterns = {
            "age": r'(\d{1,3})(?:\s*(?:years?|yrs?|Y))?',
            "gender": r'\b([MF]|male|female|man|woman)\b',
            "procedure": r'([a-zA-Z\s]+(?:surgery|procedure|care|treatment|operation))',
            "location": r'\b([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]+)*)\b(?=.*(?:\d+-?month|policy))',
            "policy_duration": r'(\d{1,2})-?month'
        }
        
        extracted = {
            "age": None, "gender": None, "procedure": None, 
            "location": None, "policy_duration": None
        }
        
        # Extract using regex
        for key, pattern in patterns.items():
            match = re.search(pattern, english_query, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if key == "gender":
                    extracted[key] = "Male" if value.lower() in ['m', 'male', 'man'] else "Female"
                else:
                    extracted[key] = value
        
        # Fallback to LLM if needed
        if not all(extracted.values()):
            try:
                llm_result = self._extract_with_llm(english_query)
                for key, value in llm_result.items():
                    if not extracted[key] and value:
                        extracted[key] = str(value)
            except Exception as e:
                logger.warning(f"LLM extraction failed: {e}")
        
        logger.info(f"Extracted query details: {extracted}")
        return extracted
    
    def _extract_with_llm(self, query: str) -> Dict[str, Any]:
        """Use LLM to extract entities from query."""
        prompt = f"""Extract information from: "{query}"
        Return JSON with: age (number), gender (Male/Female), procedure (medical procedure), 
        location (city name), policy_duration (months as number).
        Only extract if clearly stated. Return null for missing information.
        
        Example: {{"age": 32, "gender": "Female", "procedure": "maternity care", "location": "Mumbai", "policy_duration": 6}}
        
        JSON:"""
        
        try:
            response = self.llm(prompt)[0]['generated_text']
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            logger.error(f"LLM parsing error: {e}")
            return {}
    
    def search_clauses(self, query: str, clauses: list, file_path: str) -> list:
        """Find relevant clauses using semantic search."""
        if not clauses:
            return []
        
        try:
            query_embedding = self.embedder.encode(query, convert_to_tensor=True, device='cpu')
            
            # Get or generate clause embeddings
            if file_path in self.embedding_cache:
                clause_embeddings = self.embedding_cache[file_path]
            else:
                clause_texts = [clause[0] for clause in clauses]
                clause_embeddings = self.embedder.encode(
                    clause_texts, 
                    convert_to_tensor=True, 
                    batch_size=config.EMBEDDING_BATCH_SIZE,
                    device='cpu'
                )
                self.embedding_cache[file_path] = clause_embeddings
            
            # Calculate similarities
            similarities = util.cos_sim(query_embedding, clause_embeddings)[0]
            
            # Get top results
            top_k = min(config.TOP_K_CLAUSES, len(clauses))
            top_indices = torch.argsort(similarities, descending=True)[:top_k]
            
            # Filter by similarity thresholds
            results = [
                (clauses[i], similarities[i].item()) 
                for i in top_indices 
                if similarities[i] > config.SIMILARITY_PRIMARY
            ]
            
            if not results:
                results = [
                    (clauses[i], similarities[i].item()) 
                    for i in top_indices 
                    if similarities[i] > config.SIMILARITY_FALLBACK
                ]
            
            logger.info(f"Found {len(results)} relevant clauses")
            return results
            
        except Exception as e:
            logger.error(f"Error in clause search: {e}")
            return []
    
    def evaluate_decision(self, query_details: Dict[str, Any], relevant_clauses: list, query: str) -> Dict[str, Any]:
        """Evaluate insurance claim decision."""
        procedure = query_details.get("procedure", "").lower()
        policy_duration = int(query_details.get("policy_duration", 0)) if query_details.get("policy_duration") else 0
        
        decision = {
            "Decision": "Rejected",
            "Amount": None,
            "Justification": "No relevant coverage found or insufficient policy duration.",
            "Confidence": 0.0
        }
        
        # Check for accident cases
        is_accident = "accident" in procedure or "accident" in query.lower()
        is_maternity = any(term in procedure for term in ["maternity", "pregnancy", "childbirth", "baby"])
        
        max_confidence = 0.0
        
        for clause, confidence in relevant_clauses:
            clause_text = clause[0].lower()
            
            # Skip exclusions
            if "excluded" in clause_text or "not covered" in clause_text:
                continue
            
            # Check waiting periods
            waiting_match = re.search(r'(\d{1,2})-?month.*waiting', clause_text)
            if waiting_match:
                waiting_period = int(waiting_match.group(1))
                if policy_duration < waiting_period and not is_accident:
                    decision.update({
                        "Decision": "Rejected",
                        "Amount": None,
                        "Justification": f"Policy has {waiting_period}-month waiting period. Current duration: {policy_duration} months.",
                        "Confidence": confidence
                    })
                    return decision
            
            # Check for coverage
            coverage_terms = ["covered", "benefit", "sum insured", "reimbursement"]
            if any(term in clause_text for term in coverage_terms):
                if is_accident and "accident" in clause_text:
                    decision.update({
                        "Decision": "Approved",
                        "Amount": config.DEFAULT_COVERAGE,
                        "Justification": f"Accident coverage applies. No waiting period required.",
                        "Confidence": confidence
                    })
                    return decision
                
                if is_maternity and any(term in clause_text for term in ["maternity", "pregnancy", "childbirth"]):
                    if policy_duration >= 9:  # Typical maternity waiting period
                        decision.update({
                            "Decision": "Approved",
                            "Amount": config.DEFAULT_COVERAGE,
                            "Justification": f"Maternity coverage applies after waiting period.",
                            "Confidence": confidence
                        })
                        return decision
                
                if confidence > max_confidence:
                    max_confidence = confidence
                    decision.update({
                        "Decision": "Approved",
                        "Amount": config.DEFAULT_COVERAGE,
                        "Justification": f"Coverage found in policy terms.",
                        "Confidence": confidence
                    })
        
        return decision
    
    def process_query(self, query: str, document_path: str) -> Dict[str, Any]:
        """Process insurance claim query."""
        try:
            logger.info(f"Processing query: {query}")
            
            # Detect language
            query_lang = self.detect_language(query)
            logger.info(f"Detected language: {config.SUPPORTED_LANGUAGES.get(query_lang, 'Unknown')}")
            
            # Extract clauses from document
            clauses = self.parse_document(document_path)
            if not clauses:
                error_msg = self.translate_text("No content extracted from document", query_lang)
                return {"error": error_msg}
            
            # Parse query
            query_details = self.parse_query(query, query_lang)
            
            # Search for relevant clauses
            relevant_clauses = self.search_clauses(query, clauses, document_path)
            
            # Make decision
            decision = self.evaluate_decision(query_details, relevant_clauses, query)
            
            # Prepare response
            response = {
                "QueryDetails": {
                    "age": query_details["age"],
                    "gender": self.translate_text(query_details["gender"], query_lang) if query_details["gender"] else None,
                    "procedure": self.translate_text(query_details["procedure"], query_lang) if query_details["procedure"] else None,
                    "location": self.translate_text(query_details["location"], query_lang) if query_details["location"] else None,
                    "policy_duration": query_details["policy_duration"]
                },
                "Decision": self.translate_text(decision["Decision"], query_lang),
                "Amount": decision["Amount"],
                "Justification": self.translate_text(decision["Justification"], query_lang),
                "Confidence": decision.get("Confidence", 0.0),
                "RelevantClauses": [
                    {
                        "text": self.translate_text(clause[0], query_lang),
                        "source": clause[1]["file"],
                        "position": clause[1]["position"],
                        "confidence": round(conf, 3)
                    }
                    for clause, conf in relevant_clauses
                ],
                "Language": config.SUPPORTED_LANGUAGES.get(query_lang, "English"),
                "ProcessedAt": datetime.now().isoformat()
            }
            
            logger.info(f"Processing completed. Decision: {decision['Decision']}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            error_msg = self.translate_text(f"Processing error: {str(e)}", query_lang)
            return {"error": error_msg}


# Initialize the processor
processor = InsuranceClaimsProcessor()

# FastAPI application
app = FastAPI(
    title="Insurance Claims Processing API",
    description="Multilingual insurance claims processing system with document analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-claim")
async def process_claim(
    query: str = Form(..., description="Insurance claim query in any supported language"),
    file: UploadFile = File(..., description="Policy document (PDF, DOCX, TXT, EML)")
):
    """Process an insurance claim query against a policy document."""
    
    temp_file = None
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        # Create temporary file
        suffix = Path(file.filename).suffix or '.txt'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        
        # Save uploaded file
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        logger.info(f"Processing file: {file.filename} ({len(content)} bytes)")
        
        # Process the claim
        result = processor.process_query(query, temp_file.name)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/supported-languages")
async def supported_languages():
    """Get list of supported languages."""
    return {"languages": config.SUPPORTED_LANGUAGES}

if __name__ == "__main__":
    # For development
    uvicorn.run(
        app, 
        host=config.HOST, 
        port=config.PORT,
        log_level="info"
    )