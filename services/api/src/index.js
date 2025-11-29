import Fastify from 'fastify';
import cors from '@fastify/cors';
import { connectMongo, closeMongo } from '@apt/common';
import searchRoutes from './routes/search.js';

const fastify = Fastify({ logger: true });

fastify.register(cors, { origin: '*' });
fastify.register(searchRoutes, { prefix: '/search' });

fastify.addHook('onReady', async () => {
  await connectMongo();
});

fastify.addHook('onClose', async () => {
  await closeMongo();
});

const port = process.env.PORT || 8000;
fastify.listen({ port, host: '0.0.0.0' }).catch((err) => {
  fastify.log.error(err);
  process.exit(1);
});
