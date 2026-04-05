import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Attach access token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");

  if (token) {
    config.headers.Auth = `Bearer ${token}`;
  }

  return config;
});

// Refresh logic
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem("refreshToken");

        if (!refresh) throw new Error("No refresh token");

        const res = await axios.post(
          "http://127.0.0.1:8000/client/refresh/",
          { refresh }
        );

        const newAccess = res.data.access;

        localStorage.setItem("accessToken", newAccess);

        originalRequest.headers.Auth = `Bearer ${newAccess}`;

        return api(originalRequest);
      } catch (err) {
        console.log("Refresh failed", err);

        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = "/";

        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default api;