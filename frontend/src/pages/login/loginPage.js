import React from 'react'
import { LoginForm } from './components/loginForm.js'
import { Card, Container, Row, Col } from 'react-bootstrap'
import { REGISTER_PAGE_URL } from '../../consts/urls.js'

const LoginPage = ({ redirectPath = '/' }) => {
  return (
    <Container className='d-flex align-items-center justify-content-center min-vh-100'>
      <Row className='w-100'>
        <Col md={6} lg={4} className='mx-auto'>
          <Card className='p-4 shadow-sm'>
            <Card.Body>
              <h3 className='text-center mb-4'>Login</h3>
              <LoginForm onLogin={redirectPath} />
              <p className='text-center mt-3'>
                Don't have an account? <a href={REGISTER_PAGE_URL}>Register here</a>
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default LoginPage
