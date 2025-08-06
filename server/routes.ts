import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertClaimQuerySchema, claimResponseSchema, type ClaimResponse } from "@shared/schema";
import multer from "multer";
import path from "path";

// Configure multer for file uploads
const upload = multer({
  dest: 'uploads/',
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

// Mock function to simulate AI processing
async function processClaimQuery(query: string, pdfFileName?: string): Promise<ClaimResponse> {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Mock response based on query content
  const mockResponse: ClaimResponse = {
    QueryDetails: {
      PatientAge: "46 years",
      MedicalProcedure: "Knee Surgery",
      Location: "Pune",
      PolicyAge: "3 months",
      EstimatedCost: "₹85,000"
    },
    Decision: "APPROVED",
    Amount: "₹85,000",
    Justification: "The claim meets all policy requirements. The knee surgery is covered under the medical benefits section, and the policy has completed the mandatory waiting period. The treatment was performed at an approved network hospital in Pune.",
    RelevantClauses: [
      "Section 4.2: Orthopedic procedures coverage after 90-day waiting period",
      "Section 6.1: Network hospital coverage at 100% reimbursement",
      "Section 8.3: Pre-authorization not required for emergency procedures"
    ]
  };

  // Parse query to extract relevant information
  if (query.toLowerCase().includes('reject') || query.toLowerCase().includes('deny')) {
    mockResponse.Decision = "REJECTED";
    mockResponse.Amount = "₹0";
    mockResponse.Justification = "The claim does not meet policy requirements due to pre-existing condition exclusions or insufficient waiting period completion.";
  }

  return mockResponse;
}

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Submit claim query with optional PDF
  app.post("/api/claims", upload.single('pdf'), async (req, res) => {
    try {
      const { query } = req.body;
      
      if (!query) {
        return res.status(400).json({ message: "Query is required" });
      }

      const pdfFileName = req.file?.originalname;
      
      // Process the claim query
      const response = await processClaimQuery(query, pdfFileName);
      
      // Store the query and response
      const claimQuery = await storage.createClaimQuery({
        query,
        pdfFileName,
        response,
      });

      res.json({
        id: claimQuery.id,
        ...response
      });

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
