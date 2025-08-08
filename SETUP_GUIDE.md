# Insurance Claims Processing System - Setup Guide

This guide will help you set up and run the complete insurance claims processing system with frontend and backend integration.

## System Overview

The system consists of three main components:
1. **Python API** (Port 8000) - AI-powered claims processing
2. **Node.js Server** (Port 5000) - Backend API and frontend serving
3. **React Frontend** - User interface

## Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git** (for cloning the repository)

## Step 1: Install Dependencies

### Install Node.js Dependencies
```bash
npm install
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: The first time you run this, it will download several large AI models which may take 10-15 minutes depending on your internet connection.

## Step 2: Start the Python API

The Python API provides the AI-powered claims processing functionality.

```bash
# Start the insurance processing API
python start_api.py
```

You should see output like:
```
Starting Insurance Claims Processing API...
API will be available at: http://127.0.0.1:8000
Health check: http://127.0.0.1:8000/health
Supported languages: http://127.0.0.1:8000/supported-languages

Press Ctrl+C to stop the API
--------------------------------------------------
```

**Keep this terminal open** - the Python API needs to stay running.

## Step 3: Start the Frontend Server

In a **new terminal window**, start the Node.js server which serves both the API and frontend:

```bash
npm run dev
```

You should see output like:
```
serving on port 5000
```

The application will be available at `http://127.0.0.1:5000`

## Step 4: Test the System

### Option 1: Use the Web Interface
1. Open your browser to `http://127.0.0.1:5000`
2. Upload a PDF document (or skip to use default content)
3. Enter a query like: "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
4. Click "Process Claim"
5. View the results!

### Option 2: Test the API Directly
```bash
python test_python_api.py
```

This will test all API endpoints and show you the results.

## Example Queries to Try

- **English**: "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
- **Hindi**: "32 साल की महिला, मुंबई में मातृत्व देखभाल, 24 महीने की पॉलिसी"
- **Spanish**: "55 años, hombre, lesión por accidente en Delhi, póliza de 6 meses"
- **French**: "28 ans, femme, soins de maternité à Bangalore, police de 12 mois"

## Troubleshooting

### Python API Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Problem**: API fails to start
**Solution**: Check if port 8000 is available:
```bash
# On Windows
netstat -an | findstr :8000
# On Linux/Mac
lsof -i :8000
```

**Problem**: Models take too long to download
**Solution**: The first run downloads AI models. This is normal and only happens once.

### Frontend Issues

**Problem**: Frontend not connecting to backend
**Solution**: 
1. Ensure Node.js server is running on port 5000
2. Check browser console for errors
3. Try refreshing the page

**Problem**: File upload issues
**Solution**:
1. Ensure file is PDF, DOCX, TXT, or EML format
2. Check file size (max 10MB)
3. Try with a different file

### Database Issues

**Problem**: Database connection errors
**Solution**: The system uses in-memory storage by default. No database setup required.

## API Endpoints

### Python API (Port 8000)
- `POST /process-claim` - Process insurance claim with document
- `GET /health` - Health check
- `GET /supported-languages` - List supported languages

### Node.js Server (Port 5000)
- `POST /api/claims` - Submit claim query with file upload
- `GET /api/claims/:id` - Get claim by ID
- `GET /api/claims` - Get all claims

## Supported Languages

The system supports 12+ languages:
- English (en)
- Hindi (hi)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (zh)
- Arabic (ar)
- Russian (ru)
- Japanese (ja)
- Portuguese (pt)
- Italian (it)
- Korean (ko)

## File Formats Supported

- **PDF** - Insurance policy documents
- **DOCX** - Word documents
- **TXT** - Plain text files
- **EML** - Email files

## Performance Notes

- **First Run**: Models download takes 10-15 minutes
- **Processing Time**: 5-15 seconds per claim
- **Memory Usage**: ~2GB RAM required
- **File Size**: Max 10MB per upload

## Development Mode

For development, you can run both servers with hot reloading:

```bash
# Terminal 1: Python API with auto-restart
python start_api.py

# Terminal 2: Node.js with hot reload
npm run dev
```

## Production Deployment

For production deployment:

1. **Python API**: Deploy to a Python hosting service (Railway, Render, etc.)
2. **Frontend**: Build and deploy to a static hosting service
3. **Environment Variables**: Set up proper environment variables
4. **CORS**: Configure CORS settings for your domain

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Look at the console logs for error messages
3. Ensure all dependencies are installed
4. Verify ports 5000 and 8000 are available
5. Check that both servers are running

## Quick Commands Reference

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Start Python API
python start_api.py

# Start frontend (in new terminal)
npm run dev

# Test API
python test_python_api.py

# Check if ports are in use
netstat -an | findstr :8000
netstat -an | findstr :5000
```

---

**Your insurance claims processing system is now ready! 🚀**
