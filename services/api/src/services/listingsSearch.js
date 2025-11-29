import { getDb, embedText, mapListingSummary } from '@apt/common';

function buildFilters(filters = {}) {
  const mongoFilter = {};
  if (filters.city) {
    mongoFilter['location.city'] = filters.city;
  }
  if (filters.neighborhoods?.length) {
    mongoFilter['location.neighborhood'] = { $in: filters.neighborhoods };
  }
  if (filters.price_min || filters.price_max) {
    mongoFilter['pricing.price'] = {};
    if (filters.price_min) mongoFilter['pricing.price'].$gte = filters.price_min;
    if (filters.price_max) mongoFilter['pricing.price'].$lte = filters.price_max;
  }
  if (filters.rooms_min || filters.rooms_max) {
    mongoFilter['details.rooms'] = {};
    if (filters.rooms_min) mongoFilter['details.rooms'].$gte = filters.rooms_min;
    if (filters.rooms_max) mongoFilter['details.rooms'].$lte = filters.rooms_max;
  }
  if (filters.from_date_before || filters.from_date_after) {
    mongoFilter['availability.from_date'] = {};
    if (filters.from_date_after) mongoFilter['availability.from_date'].$gte = new Date(filters.from_date_after);
    if (filters.from_date_before) mongoFilter['availability.from_date'].$lte = new Date(filters.from_date_before);
  }
  return Object.keys(mongoFilter).length ? mongoFilter : undefined;
}

export async function searchListings({ query, filters, limit = 20 }) {
  const db = getDb();
  const { vector } = await embedText(query);
  const pipeline = [
    {
      $vectorSearch: {
        index: 'listing_embedding_index',
        path: 'embedding',
        queryVector: vector,
        numCandidates: Math.max(limit * 5, 50),
        limit,
        filter: buildFilters(filters),
      },
    },
    {
      $project: {
        title: 1,
        url: 1,
        location: 1,
        pricing: 1,
        details: 1,
        score: { $meta: 'vectorSearchScore' },
      },
    },
  ];
  const cursor = db.collection('listings').aggregate(pipeline);
  const docs = await cursor.toArray();
  return docs.map(mapListingSummary);
}
