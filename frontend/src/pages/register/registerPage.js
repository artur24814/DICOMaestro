import React from 'react'
import RegisterForm from './components/RegisterForm'
import { Card, Container, Row, Col } from 'react-bootstrap'
import { LOGIN_PAGE_URL } from '../../consts/urls'

const RedirectPage = () => {
  return (
    <Container className='d-flex align-items-center justify-content-center min-vh-100'>
      <Row className='w-100'>
        <Col md={6} lg={4} className='mx-auto'>
          <Card className='p-4 shadow-sm'>
            <Card.Body>
              <h3 className='text-center mb-4'>Register</h3>
              <RegisterForm />
              <p className='text-center mt-3'>
                Already have an account? <a href={LOGIN_PAGE_URL}>log in here</a>
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default RedirectPage
