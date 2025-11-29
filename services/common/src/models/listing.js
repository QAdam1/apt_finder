import { ObjectId } from 'mongodb';

export function toListingInsert(listing) {
  const now = new Date();
  return {
    ...listing,
    meta: {
      created_at: now,
      updated_at: now,
      ...(listing.meta || {}),
    },
  };
}

export function mapListingSummary(doc) {
  return {
    id: doc._id instanceof ObjectId ? doc._id.toString() : doc._id,
    title: doc.title,
    url: doc.url,
    city: doc.location?.city,
    neighborhood: doc.location?.neighborhood,
    price: doc.pricing?.price,
    rooms: doc.details?.rooms,
    score: doc.score ?? 0,
  };
}
