import { PythonShell } from 'python-shell';
import { connectMongo, getDb, mapScrapedPost } from '@apt/common';
import { settings } from '@apt/common';

async function runScrape() {
  await connectMongo();
  const posts = await new Promise((resolve, reject) => {
    const results = [];
    const shell = new PythonShell('services/scraper/src/python/scrape.py', {
      mode: 'text',
      env: {
        ...process.env,
        SCRAPER_GROUP_ID: settings.scraper.groupId,
        SCRAPER_EMAIL: settings.scraper.email,
        SCRAPER_PASSWORD: settings.scraper.password,
      },
    });
    shell.on('message', (msg) => results.push(msg));
    shell.end((err) => {
      if (err) return reject(err);
      try {
        const payload = results.join('\n');
        resolve(JSON.parse(payload || '[]'));
      } catch (parseErr) {
        reject(parseErr);
      }
    });
  });

  if (!posts.length) return;
  const db = getDb();
  const docs = posts.map(mapScrapedPost);
  await db.collection('posts_raw').insertMany(docs, { ordered: false }).catch((err) => {
    if (err.code !== 11000) throw err;
  });
}

function start() {
  const intervalMs = settings.scraper.intervalSeconds * 1000;
  runScrape().catch((err) => console.error('Scrape failed', err));
  setInterval(() => runScrape().catch((err) => console.error('Scrape failed', err)), intervalMs);
}

start();
