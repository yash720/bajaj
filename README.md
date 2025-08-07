# 🏥 BajajBot - Insurance Claim Analysis System

## 📋 Overview

BajajBot is an intelligent insurance claim analysis system that processes insurance queries and policy documents to provide automated claim decisions. The system uses AI/ML models to analyze insurance policies and determine claim eligibility based on policy terms and conditions.

## 🚀 Features

- **📄 PDF Document Processing**: Upload and analyze insurance policy documents
- **🤖 AI-Powered Analysis**: Uses NLP and machine learning for claim evaluation
- **🌍 Multi-Language Support**: Supports multiple languages including Hindi, English, Spanish, French, etc.
- **☁️ Cloud Storage**: Secure file storage using Cloudinary
- **📊 Real-time Analysis**: Instant claim decision and justification
- **💾 Database Storage**: MongoDB integration for data persistence
- **🎨 Modern UI**: Beautiful, responsive React frontend

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   React App     │    │   File Upload   │    │    Results Display      │  │
│  │   (Frontend)    │    │   Component     │    │      Component          │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            NODE.JS BACKEND                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Express.js    │    │   Multer        │    │    Axios HTTP Client    │  │
│  │   Server        │    │   File Handler  │    │    (Python API Call)    │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Cloudinary    │    │   MongoDB       │    │    FormData Builder     │  │
│  │   Upload/Download│   │   Storage       │    │    (File Processing)    │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PYTHON AI/ML API                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   FastAPI       │    │   PyMuPDF       │    │    FastText Language    │  │
│  │   Server        │    │   PDF Parser    │    │    Detection            │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Sentence      │    │   M2M100        │    │    NLTK Text            │  │
│  │   Transformers  │    │   Translation   │    │    Processing           │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Semantic      │    │   Claim         │    │    Decision             │  │
│  │   Search        │    │   Evaluation    │    │    Engine               │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA STORAGE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   MongoDB       │    │   Cloudinary    │    │    Temporary Files      │  │
│  │   Atlas         │    │   Cloud Storage │    │    (Local Processing)   │  │
│  │   (Claim Data)  │    │   (PDF Files)   │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘

📊 DATA FLOW:
User Upload → Frontend Validation → Backend Processing → Cloudinary Storage → 
Python AI Analysis → MongoDB Storage → Results Display
```

## 📁 Project Structure

```
BajajBot/
├── client/                 # React Frontend
│   ├── src/
│   │   ├── components/     # UI Components
│   │   │   ├── query-form.tsx      # Claim submission form
│   │   │   ├── pdf-upload.tsx      # File upload component
│   │   │   ├── results-display.tsx # Results display
│   │   │   └── ui/         # Reusable UI components
│   │   ├── pages/         # Page Components
│   │   ├── hooks/         # Custom Hooks
│   │   └── lib/           # Utilities
├── server/                 # Node.js Backend
│   ├── routes.ts          # API Routes (/api/claims)
│   ├── storage.ts         # MongoDB operations
│   ├── cloudinary.ts      # Cloudinary file handling
│   └── config.ts          # Environment configuration
├── insurance_api.py        # Python AI/ML API
├── shared/                 # Shared Types/Schemas
│   └── schema.ts          # Zod schemas & TypeScript types
└── uploads/               # Temporary File Storage
```

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Query** for state management
- **Lucide React** for icons

### Backend
- **Node.js** with Express
- **TypeScript** for type safety
- **MongoDB** with Mongoose
- **Cloudinary** for file storage
- **Multer** for file uploads

### AI/ML API
- **Python** with FastAPI
- **Sentence Transformers** for NLP
- **Transformers** (Hugging Face) for translation
- **PyMuPDF** for PDF processing
- **FastText** for language detection

## 🔧 Installation & Setup

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- MongoDB Atlas account
- Cloudinary account

### 1. Clone Repository
```bash
git clone <repository-url>
cd BajajBot
```

### 2. Install Dependencies
```bash
# Frontend dependencies
npm install

# Python dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# MongoDB Configuration
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/

# Server Configuration
PORT=5000
NODE_ENV=development
```

### 4. Start Services
```bash
# Terminal 1: Start Python AI API
python insurance_api.py

# Terminal 2: Start Node.js Backend
npm run dev

# Terminal 3: Start React Frontend
cd client && npm run dev
```

## 🔄 How It Works

### 1. User Interface Flow
```
User Uploads PDF → Frontend Validation → Backend Processing → AI Analysis → Results Display
```

### 2. File Processing Pipeline
1. **Upload**: User uploads insurance policy PDF
2. **Cloudinary Storage**: File stored securely in cloud
3. **Database**: File metadata stored in MongoDB
4. **Python Processing**: AI models analyze document content
5. **Analysis**: Extract clauses, evaluate claims, generate decisions

### 3. AI Analysis Process
1. **Document Extraction**: Extract text from PDF using PyMuPDF
2. **Language Detection**: Detect document language using FastText
3. **Clause Extraction**: Parse document into insurance clauses
4. **Query Processing**: Extract claim details from user query
5. **Semantic Search**: Find relevant clauses using embeddings
6. **Decision Making**: Evaluate claim based on policy terms
7. **Translation**: Translate results to user's language

## 📡 API Routes

### Backend Routes (Node.js)

#### POST `/api/claims`
Process insurance claim query with optional PDF upload.

**Request:**
```json
{
  "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
  "pdf": [File Upload]
}
```

**Response:**
```json
{
  "id": "claim_id",
  "QueryDetails": {
    "age": "46",
    "gender": "Male",
    "procedure": "knee surgery",
    "location": "Pune",
    "policy_duration": "3"
  },
  "Decision": "Approved",
  "Amount": 500000,
  "Justification": "Clause analysis...",
  "RelevantClauses": [
    {
      "text": "Inpatient hospitalization is covered...",
      "source": "policy_document.pdf",
      "position": 0
    }
  ]
}
```

#### GET `/api/claims/:id`
Retrieve specific claim by ID.

#### GET `/api/claims`
Get all claim queries.

### Python AI API Routes

#### POST `/process`
Process query and document for claim analysis.

**Request:**
```
FormData:
- query: "insurance query text"
- file: PDF document
```

**Response:**
```json
{
  "QueryDetails": {...},
  "Decision": "Approved/Rejected",
  "Amount": 500000,
  "Justification": "...",
  "RelevantClauses": [...]
}
```

## 🎯 Key Features Explained

### 1. Document Processing
- **PDF Text Extraction**: Uses PyMuPDF for reliable text extraction
- **OCR Support**: Handles scanned documents with Tesseract OCR
- **Multi-format Support**: PDF, DOCX, TXT, EML files

### 2. AI Analysis
- **Language Detection**: Automatically detects document language
- **Translation**: Translates results to user's preferred language
- **Semantic Search**: Finds relevant policy clauses using embeddings
- **Decision Logic**: Evaluates claims based on waiting periods, exclusions, etc.

### 3. Claim Evaluation Rules
- **Waiting Periods**: Checks policy duration vs. required waiting periods
- **Pre-existing Conditions**: Evaluates coverage for pre-existing conditions
- **Accident Claims**: Special handling for accident-related claims
- **Maternity Benefits**: Specific rules for maternity coverage
- **Geographic Coverage**: Location-based coverage evaluation

### 4. Database Schema

#### ClaimQueries Collection
```javascript
{
  id: String,              // Unique claim ID
  query: String,           // User's insurance query
  pdfFileName: String,     // Original PDF filename
  cloudinaryUrl: String,   // Cloudinary storage URL
  response: Object,        // AI analysis results
  createdAt: Date          // Timestamp
}
```

## 🚀 Deployment

### Frontend Deployment
```bash
cd client
npm run build
# Deploy build folder to hosting service
```

### Backend Deployment
```bash
npm run build
# Deploy to Node.js hosting (Vercel, Heroku, etc.)
```

### Python API Deployment
```bash
# Deploy to Python hosting (Railway, Render, etc.)
# Ensure all dependencies are in requirements.txt
```

## 🔍 Troubleshooting

### Common Issues

1. **Python API Not Starting**
   - Check if all dependencies are installed
   - Verify sentencepiece is installed: `pip install sentencepiece`
   - Check if fasttext model exists: `lid.176.bin`

2. **File Upload Issues**
   - Verify Cloudinary credentials in .env
   - Check file size limits (10MB max)
   - Ensure PDF format is correct

3. **Database Connection**
   - Verify MongoDB connection string
   - Check network connectivity
   - Ensure MongoDB Atlas IP whitelist

4. **Frontend Issues**
   - Clear browser cache
   - Check console for errors
   - Verify API endpoints are accessible

## 📊 Performance Optimization

- **Caching**: Translation and embedding results cached
- **Batch Processing**: Multiple texts processed together
- **File Compression**: Images downsampled for OCR
- **Memory Management**: Temporary files cleaned up automatically

## 🔒 Security Features

- **File Validation**: Only PDF files accepted
- **Size Limits**: 10MB file size restriction
- **Cloud Storage**: Secure file storage in Cloudinary
- **Input Sanitization**: Query text sanitized before processing

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section

---

**BajajBot** - Making insurance claim analysis intelligent and accessible! 🏥✨
