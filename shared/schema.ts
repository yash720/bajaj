import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp, json } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const claimQueries = pgTable("claim_queries", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  query: text("query").notNull(),
  pdfFileName: text("pdf_file_name"),
  response: json("response"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertClaimQuerySchema = createInsertSchema(claimQueries).pick({
  query: true,
  pdfFileName: true,
  response: true,
});

export const claimResponseSchema = z.object({
  QueryDetails: z.object({
    age: z.string().nullable(),
    gender: z.string().nullable(),
    procedure: z.string().nullable(),
    location: z.string().nullable(),
    policy_duration: z.string().nullable(),
  }),
  Decision: z.string(),
  Amount: z.number().nullable(),
  Justification: z.string(),
  Confidence: z.number().optional(),
  RelevantClauses: z.array(z.object({
    text: z.string(),
    source: z.string(),
    position: z.number(),
    confidence: z.number().optional(),
  })),
  Language: z.string().optional(),
  ProcessedAt: z.string().optional(),
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertClaimQuery = z.infer<typeof insertClaimQuerySchema>;
export type ClaimQuery = typeof claimQueries.$inferSelect;
export type ClaimResponse = z.infer<typeof claimResponseSchema>;
