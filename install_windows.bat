@echo off
echo ========================================
echo Installing Insurance API Dependencies
echo ========================================
echo.

echo Installing basic packages...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install protobuf==4.25.1

echo.
echo Installing PyTorch (CPU version)...
pip install torch==2.1.1+cpu --index-url https://download.pytorch.org/whl/cpu

echo.
echo Installing AI/ML packages...
pip install transformers==4.35.2
pip install sentence-transformers==2.2.2

echo.
echo Installing document processing packages...
pip install pdfplumber==0.10.3
pip install python-docx==1.1.0
pip install pdf2image==1.16.3
pip install pytesseract==0.3.10

echo.
echo Installing utility packages...
pip install langdetect==1.0.9
pip install nltk==3.8.1
pip install Pillow==10.1.0
pip install numpy==1.24.3
pip install scikit-learn==1.3.2

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run: python start_api.py
pause
