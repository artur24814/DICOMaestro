import React from 'react'
import { Spinner, Container, Row, Col } from 'react-bootstrap'

const FullScreenSpinner = () => {
  return (
    <Container fluid className='d-flex justify-content-center align-items-center' style={{ minHeight: '100vh' }}>
      <Row className='w-100'>
        <Col className='d-flex justify-content-center'>
          <Spinner animation='border' role='status' variant='primary' style={{ width: '6rem', height: '6rem' }}>
            <span className='visually-hidden'>Loading...</span>
          </Spinner>
        </Col>
      </Row>
    </Container>
  )
}

export default FullScreenSpinner
