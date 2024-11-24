import React from 'react'
import { Container, Row, Col, Card } from 'react-bootstrap'
import featureImage1 from '../../../assets/img/feature-1.jpeg'
import featureImage2 from '../../../assets/img/feature-2.webp'
import featureImage3 from '../../../assets/img/feature-3.jpeg'

const FeaturesSection = () => {
  return (
    <section id="features" className="py-5 bg-light">
      <Container>
        <h2 className="text-center mb-5 fw-bold">Key Features</h2>
        <Row>
          <Col md={4} className="mb-4">
            <Card className="shadow-sm h-100">
              <Card.Img variant="top" src={featureImage1} alt="Feature 1" />
              <Card.Body>
                <Card.Title>View DICOM Images</Card.Title>
                <Card.Text>
                  Effortlessly load and view both single images and full image sequences, such as CT and MRI scans.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="shadow-sm h-100">
              <Card.Img variant="top" src={featureImage2} className='h-100 object-fit-cover' alt="Feature 2" />
              <Card.Body>
                <Card.Title>Explore Metadata</Card.Title>
                <Card.Text>
                  Access comprehensive metadata embedded in DICOM files, providing valuable insights into medical data.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="shadow-sm h-100">
              <Card.Img variant="top" src={featureImage3} alt="Feature 3" />
              <Card.Body>
                <Card.Title>Create Custom Files</Card.Title>
                <Card.Text>
                  Generate tailored DICOM files for your projects using our flexible developer API.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </section>
  )
}

export default FeaturesSection