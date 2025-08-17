// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // <-- IMPORTANT
  reactStrictMode: true,
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig;
