// src/utils/api.ts
/**
 * Fetch wrapper with automatic 401 handling
 * Automatically logs out user when receiving 401 Unauthorized
 */

let logoutCallback: (() => void) | null = null;

// Register logout callback from AuthContext
export const setLogoutCallback = (callback: () => void) => {
  logoutCallback = callback;
};

// Custom fetch wrapper
export const apiFetch = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  try {
    const response = await fetch(url, options);

    // Handle 401 Unauthorized - auto logout
    if (response.status === 401) {
      console.warn('Received 401 Unauthorized - logging out user');

      if (logoutCallback) {
        logoutCallback();

        // Redirect to login page
        window.location.href = '/login';
      }
    }

    return response;
  } catch (error) {
    console.error('API fetch error:', error);
    throw error;
  }
};

// Helper for authenticated requests
export const authenticatedFetch = async (
  url: string,
  token: string | null,
  options: RequestInit = {}
): Promise<Response> => {
  if (!token) {
    throw new Error('No authentication token available');
  }

  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
  };

  return apiFetch(url, { ...options, headers });
};
