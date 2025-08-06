# Overview

This is a Bajaj Intelligent Claims Assistant - a full-stack web application that processes insurance claims using AI. The system allows users to submit insurance claims with natural language queries and optional PDF attachments, then provides AI-powered analysis with recommendations for approval or rejection. The application features a modern, responsive UI with Bajaj branding and provides detailed claim evaluations including relevant policy clauses and justifications.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: React 18 with TypeScript using Vite for build tooling
- **UI Components**: Shadcn/ui component library built on Radix UI primitives
- **Styling**: Tailwind CSS with custom Bajaj brand theming (blue color scheme)
- **State Management**: TanStack Query (React Query) for server state management
- **Routing**: Wouter for lightweight client-side routing
- **Form Handling**: React Hook Form with Zod validation

## Backend Architecture
- **Framework**: Express.js with TypeScript
- **Database**: PostgreSQL with Drizzle ORM for type-safe database operations
- **Database Provider**: Neon Database (serverless PostgreSQL)
- **File Uploads**: Multer middleware for PDF file processing (10MB limit)
- **Storage Strategy**: In-memory storage with interface for easy migration to persistent storage
- **API Design**: RESTful endpoints with proper error handling and logging

## Database Schema
- **Users Table**: Basic user management with username/password
- **Claim Queries Table**: Stores claim submissions with query text, optional PDF filename, AI response, and timestamps
- **Data Validation**: Drizzle-Zod integration for runtime type safety

## AI Processing
- **Mock AI Service**: Simulated claim processing that analyzes queries and returns structured responses
- **Response Structure**: Standardized claim analysis including patient details, decision, amount, justification, and relevant policy clauses
- **Processing Flow**: 2-second simulated delay with multi-step UI feedback

## Authentication & Security
- **File Validation**: PDF-only uploads with size restrictions
- **Input Sanitization**: Zod schema validation for all inputs
- **CORS Configuration**: Credential-based requests for session management

# External Dependencies

## Core Framework Dependencies
- **Database**: `@neondatabase/serverless` for PostgreSQL connectivity
- **ORM**: `drizzle-orm` with `drizzle-kit` for migrations and schema management
- **Frontend**: React ecosystem with Vite, TanStack Query, and Wouter router
- **UI Components**: Comprehensive Radix UI component suite via Shadcn/ui

## Development Tools
- **Build System**: Vite with React plugin and TypeScript support
- **Styling**: Tailwind CSS with PostCSS for processing
- **Validation**: Zod for runtime type checking and form validation
- **File Processing**: Multer for handling PDF uploads

## Third-Party Services
- **Database Hosting**: Neon Database (serverless PostgreSQL)
- **Fonts**: Google Fonts (Poppins font family)
- **Development**: Replit-specific plugins for enhanced development experience

## Production Considerations
- **Build Output**: Separate client and server builds with ESM modules
- **Environment Variables**: Database URL configuration required
- **Session Management**: Connect-pg-simple for PostgreSQL session storage (configured but not actively used)