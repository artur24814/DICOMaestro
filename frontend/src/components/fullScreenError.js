import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'
import { FaExclamationCircle } from 'react-icons/fa'

const FullScreenError = ({ text = 'An error occurred!' }) => {
  return (
    <Container
      fluid
      className='d-flex justify-content-center align-items-center bg-light'
      style={{ minHeight: '100vh', textAlign: 'center' }}
    >
      <Row className='w-100'>
        <Col className='d-flex flex-column justify-content-center align-items-center'>
          <FaExclamationCircle
            size={96}
            color='red'
            className='mb-4'
          />
          <h1 className='text-danger'>{text}</h1>
        </Col>
      </Row>
    </Container>
  )
}

export default FullScreenError
