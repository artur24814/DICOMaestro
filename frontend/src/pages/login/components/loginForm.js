import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import * as yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'
import { Button, Form, Alert } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../contexts/AuthContext.js'

const schema = yup.object().shape({
  email: yup.string().email('Invalid email').required('Required'),
  password: yup.string().min(6, 'Password should be at least 6 characters long').required('Required')
})

export const LoginForm = ({ redirectPath }) => {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [errorLoginMsg, setErrorLoginMsg] = useState(null)

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema)
  })

  const onSubmit = async (data) => {
    try {
      const user = await login(data)
      if (!user) {
        throw new Error()
      }
      navigate(redirectPath || '/')
      setErrorLoginMsg(null)
    } catch (error) {
      setErrorLoginMsg('Invalid email or password. Please try again.')
    }
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {errorLoginMsg && <Alert variant='danger'>{errorLoginMsg}</Alert>}
      <Form.Group className='mb-3' controlId='formEmail'>
        <Form.Label>Email</Form.Label>
        <Form.Control
          type='email'
          placeholder='Enter email'
          {...register('email')}
          isInvalid={!!errors.email}
        />
        <Form.Control.Feedback type='invalid'>
          {errors.email ? errors.email.message : ''}
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className='mb-3' controlId='formPassword'>
        <Form.Label>Password</Form.Label>
        <Form.Control
          type='password'
          placeholder='Password'
          {...register('password')}
          isInvalid={!!errors.password}
        />
        <Form.Control.Feedback type='invalid'>
          {errors.password ? errors.password.message : ''}
        </Form.Control.Feedback>
      </Form.Group>

      <Button variant='primary' type='submit' className='w-100'>
        Login
      </Button>
    </Form>
  )
}
