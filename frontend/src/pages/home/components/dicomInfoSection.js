import React from 'react'
import { Container, Button, Row, Col, Image } from 'react-bootstrap'
import dicomIllustration from '../../../assets/img/dicom-illustration.webp'


const DICOMInformationSection = () => {
  return (
    <section id="dicom-info" className="py-5 bg-light">
      <Container>
        <h2 className="text-center fw-bold mb-5">About DICOM</h2>
        <Row className="align-items-center">
          <Col md={6}>
            <Image src={dicomIllustration} alt="DICOM Format" className="img-fluid rounded shadow-sm" />
          </Col>
          <Col md={6} className='text-center'>
            <p className="lead">
              The **DICOM format** (Digital Imaging and Communications in Medicine) 
              is the standard for storing and transmitting medical imaging data. 
              It includes both the image itself and metadata, which provides context 
              like patient information, modality settings, and timestamps.
            </p>
            <Button variant="primary" href="https://dicomstandard.org/" target="_blank">
              Learn More About DICOM
            </Button>
          </Col>
        </Row>
      </Container>
    </section>
  )
}

export default DICOMInformationSection