import * as yup from 'yup'

const userLoginSchema = yup.object().shape({
  email: yup.string().email('Invalid email').required('Required'),
  password: yup.string().min(6, 'Password should be at least 6 characters long').required('Required')
})

export default userLoginSchema
