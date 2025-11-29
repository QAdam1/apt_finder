import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

const schema = z.object({
  MONGO_URI: z.string().url(),
  MONGO_DB_NAME: z.string().min(1),
  OPENAI_API_KEY: z.string().min(1),
  SCRAPER_GROUP_ID: z.string().optional(),
  SCRAPER_EMAIL: z.string().optional(),
  SCRAPER_PASSWORD: z.string().optional(),
  SCRAPER_INTERVAL_SECONDS: z.string().optional(),
});

const parsed = schema.safeParse(process.env);

if (!parsed.success) {
  console.error('Invalid environment configuration', parsed.error.flatten().fieldErrors);
  throw new Error('Configuration validation failed');
}

export const settings = {
  mongoUri: parsed.data.MONGO_URI,
  mongoDbName: parsed.data.MONGO_DB_NAME,
  openAiKey: parsed.data.OPENAI_API_KEY,
  scraper: {
    groupId: parsed.data.SCRAPER_GROUP_ID,
    email: parsed.data.SCRAPER_EMAIL,
    password: parsed.data.SCRAPER_PASSWORD,
    intervalSeconds: parsed.data.SCRAPER_INTERVAL_SECONDS
      ? parseInt(parsed.data.SCRAPER_INTERVAL_SECONDS, 10)
      : 300,
  },
};
