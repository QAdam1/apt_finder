import OpenAI from 'openai';
import { settings } from './config.js';

const EMBEDDING_MODEL = 'text-embedding-3-small';

const client = new OpenAI({ apiKey: settings.openAiKey });

export async function embedText(text) {
  const response = await client.embeddings.create({
    input: text,
    model: EMBEDDING_MODEL,
  });
  return {
    vector: response.data[0].embedding,
    model: EMBEDDING_MODEL,
  };
}
