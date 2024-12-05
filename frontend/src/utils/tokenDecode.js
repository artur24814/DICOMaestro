import { jwtDecode } from 'jwt-decode'

export const getUserAndExpTimeFromToken = (token) => {
  const decodedToken = getDecodedJWTToken(token)

  const user = getUserFromDecodedToken(decodedToken)
  return [user, decodedToken.exp]
}

export const getUserFromDecodedToken = (decodedToken) => {
  return decodedToken.first_name + ' ' + decodedToken.last_name
}

export const getDecodedJWTToken = (token) => {
  return jwtDecode(token)
}
