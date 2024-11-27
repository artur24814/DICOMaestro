import React from 'react'
import { Container, Button, Row, Col, Image } from 'react-bootstrap'
import featureImage3 from '../../../assets/img/feature-3.jpeg'

const APISection = () => {
  return (
    <section id="api" className="py-5">
      <Container>
        <h2 className="text-center fw-bold mb-5">Developer API</h2>
        <Row className="align-items-center">
          <Col md={6} className='text-center'>
            <p className="lead">
              Integrate DICOM Viewer into your applications with our robust API. Automate processes like loading images, exploring metadata, and creating new DICOM files effortlessly.
            </p>
            <Button variant="primary" href="#documentation">
              Explore API Documentation
            </Button>
          </Col>
          <Col md={6}>
            <Image src={featureImage3} alt="API Integration" className="img-fluid rounded" />
          </Col>
        </Row>
      </Container>
    </section>
  )
}

export default APISection