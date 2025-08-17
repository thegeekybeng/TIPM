// src/lib/utils/proxyFetch.ts

export const tryFetch = async (url: string): Promise<Response | null> => {
    try {
      const response = await fetch(url);
      return response.ok ? response : null;
    } catch {
      return null;
    }
  };
  
  export const tryFetchWithProxies = async (url: string): Promise<Response | null> => {
    const proxies = [
      '', // no proxy
      'https://api.allorigins.win/raw?url=',
      'https://corsproxy.io/?',
      'https://cors-anywhere.herokuapp.com/'
    ];
  
    for (const proxy of proxies) {
      const fullUrl = proxy ? `${proxy}${url}` : url;
      const response = await tryFetch(fullUrl);
      if (response) return response;
    }
    return null;
  };