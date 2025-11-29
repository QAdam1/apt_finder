import { connectMongo, getDb, closeMongo } from '@apt/common';

const VECTOR_INDEX_NAME = 'listing_embedding_index';
const EMBEDDING_DIMENSIONS = 1536;

async function createPostsRawIndexes(db) {
  await db.collection('posts_raw').createIndex({ 'source.post_id': 1 }, { unique: true });
  await db.collection('posts_raw').createIndex({ posted_at: 1 });
  await db.collection('posts_raw').createIndex({ scraped_at: 1 });
  console.log('Ensured indexes on posts_raw');
}

async function createListingsIndexes(db) {
  const listings = db.collection('listings');
  await listings.createIndex({ 'location.city': 1 });
  await listings.createIndex({ 'location.neighborhood': 1 });
  await listings.createIndex({ 'pricing.price': 1 });
  await listings.createIndex({ 'details.rooms': 1 });
  await listings.createIndex({ 'availability.from_date': 1 });
  console.log('Ensured standard indexes on listings');

  try {
    await db.command({
      createSearchIndexes: 'listings',
      indexes: [
        {
          name: VECTOR_INDEX_NAME,
          definition: {
            mappings: {
              dynamic: true,
              fields: {
                embedding: {
                  type: 'vector',
                  path: 'embedding',
                  numDimensions: EMBEDDING_DIMENSIONS,
                  similarity: 'cosine',
                },
              },
            },
          },
        },
      ],
    });
    console.log(`Ensured vector index '${VECTOR_INDEX_NAME}' on listings.embedding`);
  } catch (err) {
    console.warn('Could not create vector index automatically. If using Atlas, create it via the UI.');
    console.warn(err?.message || err);
  }
}

async function main() {
  await connectMongo();
  const db = getDb();
  await createPostsRawIndexes(db);
  await createListingsIndexes(db);
  await closeMongo();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
