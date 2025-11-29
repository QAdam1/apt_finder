import { MongoClient } from 'mongodb';
import { settings } from './config.js';

let client;
let db;

export async function connectMongo() {
  if (db) return db;
  client = new MongoClient(settings.mongoUri);
  await client.connect();
  db = client.db(settings.mongoDbName);
  return db;
}

export function getDb() {
  if (!db) throw new Error('Mongo has not been initialized. Call connectMongo first.');
  return db;
}

export async function closeMongo() {
  if (client) {
    await client.close();
  }
  client = undefined;
  db = undefined;
}
