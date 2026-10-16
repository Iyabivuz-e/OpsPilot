// lib/api/client.ts
import axios from "axios"

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true, // if your auth uses cookies; otherwise attach the token in the interceptor
  timeout: 30_000,
})

api.interceptors.request.use((config) => {
  config.headers["X-Request-ID"] = crypto.randomUUID()
  return config
})