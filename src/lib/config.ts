// TIPM Configuration Utility
// Handles environment-specific configuration for local development and production

export interface TIPMConfig {
  apiBaseUrl: string;
  environment: 'development' | 'production' | 'staging';
  isLocalDev: boolean;
  isProduction: boolean;
  corsOrigins: string[];
}

// Import environment configuration
import { environmentConfig, validateEnvironment } from './environment';

// Environment detection
const isLocalDev = environmentConfig.environment === 'development';
const isProduction = environmentConfig.environment === 'production';

// API Base URL configuration
const getApiBaseUrl = (): string => {
  return environmentConfig.apiBaseUrl;
};

// CORS origins for different environments
const getCorsOrigins = (): string[] => {
  return environmentConfig.corsOrigins;
};

// Main configuration object
export const config: TIPMConfig = {
  apiBaseUrl: getApiBaseUrl(),
  environment: environmentConfig.environment,
  isLocalDev,
  isProduction,
  corsOrigins: getCorsOrigins(),
};

// Environment-specific configurations
export const developmentConfig = {
  ...config,
  debug: true,
  logLevel: 'debug',
  apiTimeout: 10000,
};

export const productionConfig = {
  ...config,
  debug: false,
  logLevel: 'error',
  apiTimeout: 30000,
};

// Get current configuration based on environment
export const getCurrentConfig = (): TIPMConfig => {
  return environmentConfig.environment === 'development' ? developmentConfig : productionConfig;
};

// Configuration validation
export const validateConfig = (): boolean => {
  // Use the environment validation
  return validateEnvironment();
};

// Export default configuration
export default config;
