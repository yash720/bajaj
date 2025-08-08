// Configuration for the application
export const config = {
  database: {
    url: process.env.DATABASE_URL || 'mongodb+srv://codefreaks0:g2zl7q8EeWllpWzT@cluster0.mh8jeol.mongodb.net/',
  },
  server: {
    port: process.env.PORT || 5000,
    nodeEnv: process.env.NODE_ENV || 'development',
  },
};
