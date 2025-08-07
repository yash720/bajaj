import React, { useState, useRef } from "react";
import { Upload, File, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PDFUploadProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

export default function PDFUpload({ onFileSelect, selectedFile }: PDFUploadProps) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type === "application/pdf") {
        if (file.size > 10 * 1024 * 1024) { // 10MB limit
          alert("File size must be less than 10MB.");
          return;
        }
        onFileSelect(file);
      } else {
        alert("Please upload only PDF files.");
      }
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type === "application/pdf") {
        if (file.size > 10 * 1024 * 1024) { // 10MB limit
          alert("File size must be less than 10MB.");
          return;
        }
        onFileSelect(file);
      } else {
        alert("Please upload only PDF files.");
      }
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = () => {
    onFileSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="mb-6">
      <label className="block text-lg font-medium text-gray-900 mb-2">
        Upload Policy Document (Optional)
      </label>
      
      {selectedFile ? (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <File className="h-8 w-8 text-green-600" />
              <div>
                <p className="font-medium text-green-800">{selectedFile.name}</p>
                <p className="text-sm text-green-600">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleRemoveFile}
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ) : (
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 cursor-pointer ${
            dragOver
              ? "border-bajaj-blue bg-blue-50"
              : "border-gray-300 hover:border-bajaj-blue hover:bg-gray-50"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
        >
          <Upload className={`mx-auto h-12 w-12 mb-4 ${dragOver ? "text-bajaj-blue" : "text-gray-400"}`} />
          <p className="text-lg font-medium text-gray-900 mb-2">
            Upload your policy document
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Drag and drop a PDF file here, or click to browse
          </p>
          <Button
            type="button"
            variant="outline"
            className="border-bajaj-blue text-bajaj-blue hover:bg-bajaj-blue hover:text-white"
          >
            Browse Files
          </Button>
          <p className="text-xs text-gray-400 mt-2">
            PDF files only, max 10MB
          </p>
        </div>
      )}
      
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleFileInput}
      />
    </div>
  );
}
