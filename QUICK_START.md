# Quick Start Guide

Get the Insurance Claims Processing System running in 5 minutes!

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

## Step 1: Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Start the Python API

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
```

## Step 3: Start the Frontend

In a new terminal:

```bash
# Start the development server
npm run dev
```

The application will be available at `http://127.0.0.1:5000`

## Step 4: Test the System

1. Open your browser to `http://127.0.0.1:5000`
2. Upload a PDF document (or skip if you want to use default content)
3. Enter a query like: "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
4. Click "Process Claim"
5. View the results!

## Example Queries to Try

- "32-year-old female, maternity care in Mumbai, 24-month policy"
- "55-year-old male, accident injury in Delhi, 6-month policy"
- "28-year-old female, dental surgery in Bangalore, 12-month policy"

## Troubleshooting

### Python API Issues
- Make sure all packages are installed: `pip install -r requirements.txt`
- Check if port 8000 is available
- Try: `python -c "import torch; print('PyTorch OK')"`

### Frontend Issues
- Make sure Node.js server is running on port 5000
- Check browser console for errors
- Try refreshing the page

### File Upload Issues
- Ensure file is PDF, DOCX, TXT, or EML format
- Check file size (max 10MB)
- Try with a different file

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the [API Documentation](API_DOCUMENTATION.md) for technical details
- Explore the codebase structure in the project folders

## Support

If you encounter issues:
1. Check the troubleshooting section in the main README
2. Open an issue on GitHub
3. Contact the development team

Happy processing! 🚀
