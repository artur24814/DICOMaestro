import React from 'react'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import { Button, Form, Alert, Spinner } from 'react-bootstrap'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../contexts/AuthContext.js'
import userLoginSchema from '../validators/UserLoginValidation.js'

export const LoginForm = ({ redirectPath }) => {
  const navigate = useNavigate()
  const { login } = useAuth()

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(userLoginSchema)
  })

  const mutation = useMutation({
    mutationFn: async (data) => {
      const user = await login(data)
      if (!user) {
        throw new Error('Login failed')
      }
      return user
    },
    onSuccess: () => {
      navigate(redirectPath || '/')
    }
  })

  const onSubmit = (data) => {
    mutation.mutate(data)
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {mutation.isError && <Alert variant='danger'>Invalid email or password. Please try again.</Alert>}
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

      <Button variant='primary' type='submit' className='w-100' disabled={mutation.isPending}>
        {mutation.isPending && (
          <Spinner
            as='span'
            animation='border'
            size='sm'
            role='status'
            aria-hidden='true'
            className='me-2'
          />
        )}
        {mutation.isPending ? 'Logging in...' : 'Login'}
      </Button>
    </Form>
  )
}
