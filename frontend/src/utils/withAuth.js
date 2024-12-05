import React from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useLocation, Navigate } from 'react-router-dom'
import { LOGIN_PAGE_URL } from '../consts/urls'

const withAuth = (WrappedComponent) => {
  const AuthenticatedComponent = (props) => {
    const { isAuthenticated } = useAuth()
    const location = useLocation()

    if (!isAuthenticated) {
      return <Navigate to={LOGIN_PAGE_URL} state={{ from: location.pathname }} />
    }
    return <WrappedComponent {...props} />
  }

  return AuthenticatedComponent
}

export default withAuth
