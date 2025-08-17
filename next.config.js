// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',         // <- CRUCIAL FIX FOR VERCEL DEPLOYMENT
  reactStrictMode: true,
  experimental: {
    serverActions: true,        // (Optional) keep if you're using server actions
  },
};

module.exports = nextConfig;
