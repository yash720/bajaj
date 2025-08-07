// Configuration for the application
export const config = {
  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME || 'your_cloud_name',
    apiKey: process.env.CLOUDINARY_API_KEY || 'your_api_key',
    apiSecret: process.env.CLOUDINARY_API_SECRET || 'your_api_secret',
  },
  database: {
    url: process.env.DATABASE_URL || 'mongodb+srv://codefreaks0:g2zl7q8EeWllpWzT@cluster0.mh8jeol.mongodb.net/',
  },
  server: {
    port: process.env.PORT || 5000,
    nodeEnv: process.env.NODE_ENV || 'development',
  },
};

// Instructions for setting up Cloudinary:
// 1. Go to https://cloudinary.com/ and create a free account
// 2. Get your Cloud Name, API Key, and API Secret from the dashboard
// 3. Set these environment variables:
//    CLOUDINARY_CLOUD_NAME=your_cloud_name
//    CLOUDINARY_API_KEY=your_api_key
//    CLOUDINARY_API_SECRET=your_api_secret
