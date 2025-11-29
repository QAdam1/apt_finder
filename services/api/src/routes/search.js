import { searchListings } from '../services/listingsSearch.js';

async function routes(fastify) {
  fastify.post('/listings', async (request, reply) => {
    const { query, filters, limit = 20 } = request.body || {};
    if (!query) {
      return reply.code(400).send({ error: 'query is required' });
    }
    const results = await searchListings({ query, filters, limit });
    return { results };
  });
}

export default routes;
