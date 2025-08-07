import mongoose from 'mongoose';
import { config } from './config';

// MongoDB connection
mongoose.connect(config.database.url)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Claim Query Schema
const claimQuerySchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  query: { type: String, required: true },
  pdfFileName: { type: String },
  cloudinaryUrl: { type: String },
  response: { type: mongoose.Schema.Types.Mixed },
  createdAt: { type: Date, default: Date.now }
});

const ClaimQuery = mongoose.model('ClaimQuery', claimQuerySchema);

// Generate UUID for MongoDB
function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

export const storage = {
  async createClaimQuery(data: {
    query: string;
    pdfFileName?: string;
    cloudinaryUrl?: string;
    response: any;
  }) {
    const id = generateId();
    const claimQuery = new ClaimQuery({
      id,
      ...data
    });
    await claimQuery.save();
    return { id, ...data };
  },

  async getClaimQuery(id: string) {
    const claimQuery = await ClaimQuery.findOne({ id });
    return claimQuery ? claimQuery.toObject() : null;
  },

  async getAllClaimQueries() {
    const claimQueries = await ClaimQuery.find().sort({ createdAt: -1 });
    return claimQueries.map(query => query.toObject());
  },

  async deleteClaimQuery(id: string) {
    await ClaimQuery.deleteOne({ id });
  }
};
