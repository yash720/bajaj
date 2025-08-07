# ⚡ BajajBot Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. **Environment Setup** ✅
```bash
# .env file already configured with your credentials:
CLOUDINARY_CLOUD_NAME=dfdfugipq
CLOUDINARY_API_KEY=717998256159241
CLOUDINARY_API_SECRET=f7mJSgTzLGifGHbmXpY09VsCoJM
DATABASE_URL=mongodb+srv://codefreaks0:g2zl7q8EeWllpWzT@cluster0.mh8jeol.mongodb.net/
```

### 2. **Start All Services**
```bash
# Terminal 1: Python AI API
python insurance_api.py

# Terminal 2: Node.js Backend + Frontend
npm run dev
```

### 3. **Access Your Application**
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:5000/api
- **Python AI API**: http://localhost:8000

## 🎯 Quick Test

1. **Open Browser**: Go to http://localhost:5000
2. **Upload PDF**: Click "Browse Files" and select any insurance policy PDF
3. **Enter Query**: Type: `"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"`
4. **Submit**: Click "Process Claim"
5. **View Results**: See the analysis results!

## 📊 Expected Results

```json
{
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

## 🔧 Troubleshooting

### If Python API doesn't start:
```bash
pip install sentencepiece
python insurance_api.py
```

### If frontend doesn't load:
```bash
npm install
npm run dev
```

### If file upload fails:
- Check file size (max 10MB)
- Ensure it's a PDF file
- Verify Cloudinary credentials

## 📱 API Testing

### Test with curl:
```bash
# Test claim processing
curl -X POST http://localhost:5000/api/claims \
  -F "query=46-year-old male, knee surgery in Pune, 3-month-old insurance policy" \
  -F "pdf=@your_policy.pdf"
```

### Test Python API directly:
```bash
curl -X POST http://localhost:8000/process \
  -F "query=46-year-old male, knee surgery in Pune, 3-month-old insurance policy" \
  -F "file=@your_policy.pdf"
```

## 🎉 Success Indicators

✅ **Python API**: "INFO: Uvicorn running on http://127.0.0.1:8000"  
✅ **Backend**: "Connected to MongoDB"  
✅ **Frontend**: "Claim Analysis Complete" message  
✅ **File Upload**: Green checkmark with file details  
✅ **Results**: Proper RelevantClauses array (not undefined)  

## 📞 Need Help?

- Check console logs for errors
- Verify all services are running
- Ensure ports 5000 and 8000 are free
- Check .env file configuration

---

**Your BajajBot is ready to analyze insurance claims! 🏥✨**
