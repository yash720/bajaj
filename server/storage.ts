import { type User, type InsertUser, type ClaimQuery, type InsertClaimQuery } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  createClaimQuery(claimQuery: InsertClaimQuery): Promise<ClaimQuery>;
  getClaimQuery(id: string): Promise<ClaimQuery | undefined>;
  getAllClaimQueries(): Promise<ClaimQuery[]>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private claimQueries: Map<string, ClaimQuery>;

  constructor() {
    this.users = new Map();
    this.claimQueries = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async createClaimQuery(insertClaimQuery: InsertClaimQuery): Promise<ClaimQuery> {
    const id = randomUUID();
    const claimQuery: ClaimQuery = { 
      ...insertClaimQuery, 
      id, 
      createdAt: new Date() 
    };
    this.claimQueries.set(id, claimQuery);
    return claimQuery;
  }

  async getClaimQuery(id: string): Promise<ClaimQuery | undefined> {
    return this.claimQueries.get(id);
  }

  async getAllClaimQueries(): Promise<ClaimQuery[]> {
    return Array.from(this.claimQueries.values());
  }
}

export const storage = new MemStorage();
