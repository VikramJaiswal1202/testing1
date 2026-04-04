const { createServer } = require('http');
const { parse } = require('url');
const next = require('next');
const { execSync } = require('child_process');
const fs = require('fs');

const dev = process.env.NODE_ENV !== 'production';

// If running in production and .next doesn't exist, build it first
if (!dev && !fs.existsSync('.next')) {
  console.log('Building Next.js application...');
  execSync('npm run build', { stdio: 'inherit' });
}

// Render requires binding to 0.0.0.0 to receive external traffic
const hostname = '0.0.0.0';
const port = parseInt(process.env.PORT, 10) || 10000;

const app = next({ dev, hostname, port });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  createServer((req, res) => {
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  }).listen(port, hostname, (err) => {
    if (err) throw err;
    console.log(`> Ready on http://${hostname}:${port}`);
  });
}).catch((err) => {
  console.error('Error starting server', err);
  process.exit(1);
});
