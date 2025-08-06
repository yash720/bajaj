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

  // Parse query to extract information
  const extractInfo = (query: string) => {
    const ageMatch = query.match(/(\d+)(?:-year-old|F|M|\s+(?:male|female))/i);
    const genderMatch = query.match(/(male|female|M|F)/i);
    const procedureMatch = query.match(/(surgery|care|procedure|treatment|maternity|knee|hip|cardiac|dental)[\s\w]*/i);
    const locationMatch = query.match(/(Mumbai|Delhi|Pune|Bangalore|Chennai|Kolkata|Hyderabad|[\w\s]+(?:\s+city|\s+hospital))/i);
    const policyMatch = query.match(/(\d+)-month/i);

    return {
      age: ageMatch ? ageMatch[1] : null,
      gender: genderMatch ? (genderMatch[1].toLowerCase().startsWith('m') ? 'Male' : 'Female') : null,
      procedure: procedureMatch ? procedureMatch[0].trim() : null,
      location: locationMatch ? locationMatch[1] : null,
      policy_duration: policyMatch ? policyMatch[1] : null,
    };
  };

  const queryDetails = extractInfo(query);
  
  // Determine decision based on query content and policy duration
  const policyMonths = parseInt(queryDetails.policy_duration || "0");
  const isMaternity = query.toLowerCase().includes('maternity');
  const isAccident = query.toLowerCase().includes('accident');
  
  let decision = "Approved";
  let amount = 500000;
  let justification = "The claim meets all policy requirements and coverage terms.";
  
  // Apply business logic
  if (isMaternity && policyMonths < 36) {
    decision = "Rejected";
    amount = null;
    justification = `Maternity care has a 36-month waiting period. Policy duration is ${policyMonths} months.`;
  } else if (queryDetails.procedure?.toLowerCase().includes('pre-existing') && policyMonths < 24) {
    decision = "Rejected";
    amount = null;
    justification = `Pre-existing conditions have a 24-month waiting period. Policy duration is ${policyMonths} months.`;
  } else if (isAccident) {
    decision = "Approved";
    amount = 500000;
    justification = "Accident-related procedures are covered without waiting period.";
  }

  const mockResponse: ClaimResponse = {
    QueryDetails: queryDetails,
    Decision: decision,
    Amount: amount,
    Justification: justification,
    RelevantClauses: [
      {
        text: "Section 4.2: Orthopedic procedures coverage after 90-day waiting period",
        source: "policy_document.pdf",
        position: 1
      },
      {
        text: "Section 6.1: Network hospital coverage at 100% reimbursement",
        source: "policy_document.pdf",
        position: 2
      },
      {
        text: "Section 8.3: Pre-authorization not required for emergency procedures",
        source: "policy_document.pdf", 
        position: 3
      }
    ]
  };

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
