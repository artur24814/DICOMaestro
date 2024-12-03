import axios from "axios"
import { ACCESS_TOKEN_NAME } from "./tokenConfig"

const api = axios.create({
  baseURL:  process.env.REACT_APP_API_URL,
  withCredentials: true,
})

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem(ACCESS_TOKEN_NAME)
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default api