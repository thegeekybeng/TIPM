// TIPM Environment Configuration
// This file provides environment-specific configuration for the frontend

export interface EnvironmentConfig {
  apiBaseUrl: string;
  environment: 'development' | 'production' | 'staging';
  corsOrigins: string[];
  debug: boolean;
}

// Get environment variables with fallbacks
const getEnvVar = (key: string, fallback: string): string => {
  if (typeof window !== 'undefined') {
    // Browser environment
    return (window as any).__ENV__?.[key] || fallback;
  }
  // Node.js environment
  return process.env[key] || fallback;
};

// Environment detection
const isDevelopment = getEnvVar('NODE_ENV', 'development') === 'development';
const isProduction = getEnvVar('NODE_ENV', 'development') === 'production';

// API Base URL configuration
const getApiBaseUrl = (): string => {
  // Priority order:
  // 1. Environment variable (NEXT_PUBLIC_API_BASE)
  // 2. Local development default
  // 3. Production default
  
  const envApiBase = getEnvVar('NEXT_PUBLIC_API_BASE', '');
  
  if (envApiBase) {
    return envApiBase;
  }
  
  if (isDevelopment) {
    return 'http://localhost:8000';
  }
  
  // Production defaults
  if (isProduction) {
    return 'https://tipm-api.onrender.com';
  }
  
  return 'http://localhost:8000';
};

// CORS origins for different environments
const getCorsOrigins = (): string[] => {
  if (isDevelopment) {
    return [
      'http://localhost:3000',
      'http://127.0.0.1:3000',
      'http://localhost:3001',
      'http://localhost:3002'
    ];
  }
  
  return [
    'https://tipm.vercel.app',
    'https://tipm-app.vercel.app',
    'https://tipm-app.onrender.com',
    'https://tipm-api.onrender.com'
  ];
};

// Main configuration object
export const environmentConfig: EnvironmentConfig = {
  apiBaseUrl: getApiBaseUrl(),
  environment: isDevelopment ? 'development' : 'production',
  corsOrigins: getCorsOrigins(),
  debug: isDevelopment,
};

// Environment-specific configurations
export const developmentConfig: EnvironmentConfig = {
  ...environmentConfig,
  debug: true,
};

export const productionConfig: EnvironmentConfig = {
  ...environmentConfig,
  debug: false,
};

// Get current configuration based on environment
export const getCurrentConfig = (): EnvironmentConfig => {
  return isDevelopment ? developmentConfig : productionConfig;
};

// Configuration validation
export const validateEnvironment = (): boolean => {
  const currentConfig = getCurrentConfig();
  
  if (!currentConfig.apiBaseUrl) {
    console.error('❌ API base URL is not configured');
    return false;
  }
  
  if (!currentConfig.apiBaseUrl.startsWith('http')) {
    console.error('❌ Invalid API base URL format');
    return false;
  }
  
  console.log('✅ Environment configuration validated successfully');
  console.log(`🌍 Environment: ${currentConfig.environment}`);
  console.log(`🔗 API Base URL: ${currentConfig.apiBaseUrl}`);
  console.log(`🔒 CORS Origins: ${currentConfig.corsOrigins.join(', ')}`);
  
  return true;
};

// Export default configuration
export default environmentConfig;
