import * as yup from 'yup'

const userRegistrationSchema = yup.object().shape({
  first_name: yup.string().min(2, 'Too Short').max(50, 'Too Long!').required('Required'),
  last_name: yup.string().min(2, 'Too Short').max(50, 'Too Long!').required('Required'),
  email: yup.string().email('Invalid email').required('Required'),
  password: yup.string().min(6, 'Password should be at least 6 characters long').required('Required'),
  confirm_password: yup.string().oneOf([yup.ref('password')], 'Passwords must match').required('Required')
})

export default userRegistrationSchema
