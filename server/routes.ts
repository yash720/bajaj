import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertClaimQuerySchema, claimResponseSchema, type ClaimResponse } from "@shared/schema";
import multer from "multer";
import path from "path";
import axios from "axios";
import FormData from "form-data";
import fs from "fs";
// File processing utilities

// Configure multer for memory storage (for direct file processing)
const upload = multer({
  storage: multer.memoryStorage(),
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed'), false);
    }
  },
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
});

// Remove the mock processClaimQuery function

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Submit claim query with optional PDF
  app.post("/api/claims", upload.single('pdf'), async (req, res) => {
    try {
      console.log("Received claim request:", { 
        hasFile: !!req.file, 
        fileName: req.file?.originalname,
        query: req.body.query 
      });

      const { query } = req.body;
      if (!query) {
        return res.status(400).json({ message: "Query is required" });
      }

      let pdfFileName: string | null = null;

      // Process file directly if provided
      if (req.file) {
        pdfFileName = req.file.originalname;
        console.log('File received for direct processing:', pdfFileName);
      } else {
        console.log("No file provided, will use default content");
      }

      // Prepare data for Python API
      const form = new FormData();
      form.append('query', query);
      
      if (req.file) {
        // Send file directly to Python API
        form.append('file', req.file.buffer, {
          filename: pdfFileName || 'document.pdf',
          contentType: 'application/pdf'
        });
      } else {
        // Create a temporary file with default content if no PDF is provided
        const defaultContent = `Insurance Policy Document

This is a sample insurance policy document containing standard terms and conditions.

1. Hospitalization Coverage
   - Inpatient hospitalization is covered up to the sum insured
   - Pre and post hospitalization expenses are covered
   - Room rent and boarding expenses are covered

2. Waiting Periods
   - Pre-existing conditions: 36-month waiting period
   - Maternity benefits: 24-month waiting period
   - Specific diseases: 12-month waiting period

3. Exclusions
   - Cosmetic surgery
   - Dental treatment (except due to accident)
   - Treatment outside India (except emergency)

4. Claim Process
   - Submit claim within 30 days of discharge
   - Provide all medical documents
   - Cashless facility available at network hospitals`;
        
        form.append('file', Buffer.from(defaultContent), {
          filename: 'default_policy.txt',
          contentType: 'text/plain'
        });
      }

      // Send to Python API
      console.log("Sending request to Python API...");
      const pythonApiUrl = 'http://127.0.0.1:8000/process';
      
      try {
        const response = await axios.post(pythonApiUrl, form, {
          headers: form.getHeaders(),
          maxContentLength: Infinity,
          maxBodyLength: Infinity,
          timeout: 30000, // 30 second timeout
        });
        
        console.log("Python API response received:", response.status);
        console.log("Response data:", JSON.stringify(response.data, null, 2));
        
        // Store the query and response
        const claimQuery = await storage.createClaimQuery({
          query,
          pdfFileName,
          response: response.data,
        });
        
        console.log("Claim stored in database with ID:", claimQuery.id);
        
        res.json({
          id: claimQuery.id,
          ...response.data
        });
      } catch (pythonError) {
        console.error("Error calling Python API:", pythonError);
        if (pythonError.response) {
          console.error("Python API error response:", pythonError.response.data);
          return res.status(500).json({ 
            message: "Python API error", 
            error: pythonError.response.data 
          });
        } else if (pythonError.code === 'ECONNREFUSED') {
          return res.status(500).json({ 
            message: "Python API is not running. Please start insurance_api.py" 
          });
        } else {
          return res.status(500).json({ 
            message: "Failed to process claim with Python API",
            error: pythonError.message 
          });
        }
      }
    } catch (error) {
      console.error("Error processing claim:", error);
      res.status(500).json({ message: "Internal server error processing claim" });
    }
  });

  // Get claim query by ID
  app.get("/api/claims/:id", async (req, res) => {
    try {
      const { id } = req.params;
      const claimQuery = await storage.getClaimQuery(id);
      
      if (!claimQuery) {
        return res.status(404).json({ message: "Claim query not found" });
      }

      res.json(claimQuery);
    } catch (error) {
      console.error("Error fetching claim:", error);
      res.status(500).json({ message: "Internal server error fetching claim" });
    }
  });

  // Get all claim queries
  app.get("/api/claims", async (req, res) => {
    try {
      const claimQueries = await storage.getAllClaimQueries();
      res.json(claimQueries);
    } catch (error) {
      console.error("Error fetching claims:", error);
      res.status(500).json({ message: "Internal server error fetching claims" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
