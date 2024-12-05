import React from 'react'
import { Container, Button, Row, Col, Image } from 'react-bootstrap'
import heroImage from '../../../assets/img/hero-img.jpeg'

const HeroSection = () => {
  return (
    <header className='text-white text-center py-5' style={{ background: 'linear-gradient(135deg, #d1e8ff, #b3cce6)' }}>
      <Container>
        <Row className='align-items-center'>
          <Col lg={6} className='text-lg-start'>
            <h1 className='display-4 fw-bold'>Discover DICOM Viewer</h1>
            <p className='lead'>
              A modern, open-source solution for viewing DICOM images, exploring metadata, and generating custom files. Safe, secure, and free.
            </p>
            <Button variant='primary' size='lg mb-3' href='#dicom-info'>
              Learn More
            </Button>
          </Col>
          <Col lg={6}>
            <Image src={heroImage} alt='DICOM Viewer Hero' className='img-fluid rounded shadow-sm' />
          </Col>
        </Row>
      </Container>
    </header>
  )
}

export default HeroSection
