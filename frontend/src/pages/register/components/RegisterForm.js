import React from 'react'
import { Row, Col, FloatingLabel, Form, Button } from 'react-bootstrap'
import userRegistrationSchema from '../validators/UserRegitrationValidation'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import { useMutation } from '@tanstack/react-query'
import { useAuth } from '../../../contexts/AuthContext.js'
import { useNavigate } from 'react-router-dom'
import { LOGIN_PAGE_URL } from '../../../consts/urls.js'

const RegisterForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(userRegistrationSchema)
  })

  const { registerUser } = useAuth()
  const navigate = useNavigate()

  const mutation = useMutation({
    mutationFn: (data) => registerUser(data),
    onSuccess: () => {
      navigate(LOGIN_PAGE_URL)
    },
    onError: (error) => {
      console.error('Error during registration!', error)
    }
  })

  const onSubmit = (data) => {
    mutation.mutate(data)
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Row className='g-2 mb-4'>
        <Col md>
          <FloatingLabel label={errors.first_name ? errors.first_name.message : 'First Name'}>
            <Form.Control
              type='text'
              placeholder='First name'
              {...register('first_name')}
              style={{ borderColor: errors.first_name ? 'red' : '#c0bdbd', color: errors.first_name ? 'red' : 'inherit' }}
            />
          </FloatingLabel>
        </Col>
        <Col md>
          <FloatingLabel label={errors.last_name ? errors.last_name.message : 'Second Name'}>
            <Form.Control
              type='text'
              placeholder='Second name'
              {...register('last_name')}
              style={{ borderColor: errors.last_name ? 'red' : '#c0bdbd', color: errors.last_name ? 'red' : 'inherit' }}
            />
          </FloatingLabel>
        </Col>
      </Row>
      <Row className='g-2 mb-4'>
        <Col md>
          <FloatingLabel label={errors.email ? errors.email.message : 'Email'}>
            <Form.Control
              type='email'
              placeholder='name@example.com'
              {...register('email')}
              style={{ borderColor: errors.email ? 'red' : '#c0bdbd', color: errors.email ? 'red' : 'inherit' }}
            />
          </FloatingLabel>
        </Col>
      </Row>
      <Row className='g-2 mb-4'>
        <Col md>
          <FloatingLabel label={errors.password ? errors.password.message : 'Password'}>
            <Form.Control
              type='password'
              placeholder='Password'
              {...register('password')}
              style={{ borderColor: errors.password ? 'red' : '#c0bdbd', color: errors.password ? 'red' : 'inherit' }}
            />
          </FloatingLabel>
        </Col>
      </Row>
      <Row className='g-2 mb-4'>
        <Col md>
          <FloatingLabel label={errors.confirm_password ? errors.confirm_password.message : 'Confirm password'}>
            <Form.Control
              type='password'
              placeholder='Confirm Password'
              {...register('confirm_password')}
              style={{ borderColor: errors.confirm_password ? 'red' : '#c0bdbd', color: errors.confirm_password ? 'red' : 'inherit' }}
            />
          </FloatingLabel>
        </Col>
      </Row>
      <Row>
        <Col>
          <Button className='w-100' type='submit' disabled={mutation.isLoading}>
            {mutation.isLoading ? 'Registering...' : 'Register'}
          </Button>
        </Col>
      </Row>
      {mutation.isError && <span>Error during registration. Please try again.</span>}
    </Form>
  )
}

export default RegisterForm
