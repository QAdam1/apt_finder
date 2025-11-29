export function mapScrapedPost(raw) {
  return {
    source: raw.source,
    raw: raw.raw,
    posted_at: raw.posted_at ? new Date(raw.posted_at) : undefined,
    scraped_at: new Date(),
    status: {
      is_active: true,
      last_seen_at: new Date(),
      deleted_at: null,
    },
  };
}
