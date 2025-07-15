// C:\Users\edwin\Codex_Boaster\frontend\next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*', // Match any request starting with /api/
        destination: 'http://127.0.0.1:8000/api/:path*', // Proxy it to your backend
      },
      // If you have non-/api prefixed backend routes, you'll need another rule
      // For example, if your backend also handles '/hipcortex/logs' directly (without '/api')
      // and your frontend is making calls to that, you might need:
      // {
      //   source: '/hipcortex/:path*',
      //   destination: 'http://127.0.0.1:8000/hipcortex/:path*',
      // },
    ];
  },
};

module.exports = nextConfig;