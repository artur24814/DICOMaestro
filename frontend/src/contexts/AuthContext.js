import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axiosConfig.js'
import { MAX_TOKEN_LIFE_TIME, ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME } from '../api/tokenConfig.js'
import { LOGIN_PAGE_URL } from '../consts/urls'
import { LOGIN_API_URL, REGISTER_API_URL, REFRESH_API_TOKEN } from '../consts/apiUrls.js'
import { getDecodedJWTToken, getUserFromDecodedToken } from '../utils/tokenDecode.js'

const AuthContext = createContext(null)

const AuthProvider = ({ children }) => {
  const [isFirstPageLoading, setFirstPageLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem(REFRESH_TOKEN_NAME))
  const [user, setUser] = useState(localStorage.getItem('user'))
  const [token, setToken] = useState(localStorage.getItem(ACCESS_TOKEN_NAME))
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem(REFRESH_TOKEN_NAME))

  const navigate = useNavigate()

  const login = useCallback(async (data) => {
    const response = await api.post(LOGIN_API_URL, data)
    const user = getUserFromDecodedToken(getDecodedJWTToken(response.data.access))

    setUser(user)
    setIsAuthenticated(true)
    setToken(response.data.access)
    setRefreshToken(response.data.refresh)

    localStorage.setItem(ACCESS_TOKEN_NAME, response.data.access)
    localStorage.setItem(REFRESH_TOKEN_NAME, response.data.refresh)
    localStorage.setItem('user', user)
    return user
  }, [
    setUser,
    setIsAuthenticated,
    setToken,
    setRefreshToken
  ])

  const registerUser = useCallback(async (data) => {
    const response = await api.post(REGISTER_API_URL, data)
    return response
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    setIsAuthenticated(false)
    setToken(null)
    setRefreshToken(null)

    localStorage.removeItem('user')
    localStorage.removeItem(ACCESS_TOKEN_NAME)
    localStorage.removeItem(REFRESH_TOKEN_NAME)

    navigate(LOGIN_PAGE_URL)
  }, [navigate])

  const setNewToken = useCallback(async (refreshToken) => {
    const response = await api.post(REFRESH_API_TOKEN, { refresh: refreshToken })
    if (response.status === 200) {
      localStorage.setItem(ACCESS_TOKEN_NAME, response.data.access)
    } else {
      logout()
    }

    setFirstPageLoading(false)
  }, [logout])

  useEffect(() => {
    if (isFirstPageLoading && refreshToken) {
      setNewToken(refreshToken)
    }
    const interval = setInterval(() => {
      if (refreshToken) {
        setNewToken(refreshToken)
      }
    }, MAX_TOKEN_LIFE_TIME)
    return () => clearInterval(interval)
  }, [refreshToken, isFirstPageLoading, setNewToken])

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, registerUser, logout, user, token }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider

export const useAuth = () => useContext(AuthContext)
