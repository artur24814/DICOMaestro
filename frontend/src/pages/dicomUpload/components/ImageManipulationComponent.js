import React, { useState } from 'react'
import { Container, Row, Col, Button, Navbar, Nav } from 'react-bootstrap'
import { FiLayers } from 'react-icons/fi'
import ImageCamvasComponent from './ImageCamvasComponent'


const imageData = [
  { id: 1, src: 'https://via.placeholder.com/300', alt: 'Image 1' },
  { id: 2, src: 'https://via.placeholder.com/300', alt: 'Image 2' },
  { id: 3, src: 'https://via.placeholder.com/800', alt: 'Image 3' },
];

const fakeData = [
  { id: 1, name: 'Fake Data 1', value: '1234' },
  { id: 2, name: 'Fake Data 2', value: '5678' },
  { id: 3, name: 'Fake Data 3', value: '91011' },
];

const ImageManipulationComponent = () => {
  const [showLeftPanel, setShowLeftPanel] = useState(true)
  const [showRightPanel, setShowRightPanel] = useState(true)
  const [selectedImage, setSelectedImage] = useState(imageData[0])

  
  const toggleLeftPanel = () => setShowLeftPanel(!showLeftPanel);
  const toggleRightPanel = () => setShowRightPanel(!showRightPanel)

  const getColSizes = () => {
    if (showLeftPanel && showRightPanel) return { left: 1, center: 9, right: 2 }
    if (showLeftPanel && !showRightPanel) return { left: 1, center: 11, right: 0 }
    if (!showLeftPanel && showRightPanel) return { left: 0, center: 10, right: 2 }
    return { left: 0, center: 12, right: 0 }
  };

  const { left, center, right } = getColSizes()

  return (
    <div>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container fluid>
          <Nav className="me-auto">
            <Nav.Link>
              <FiLayers /> Data
            </Nav.Link>
            <Nav.Link onClick={toggleLeftPanel}>
              {showLeftPanel ? 'Hide Left Panel' : 'Show Left Panel'}
            </Nav.Link>
            <Nav.Link onClick={toggleRightPanel}>
              {showRightPanel ? 'Hide Right Panel' : 'Show Right Panel'}
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <Container fluid className="min-vh-100">
        <Row>

          {/* Left Panel: Thumbnails */}
          {showLeftPanel && (
            <Col md={left} className="d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end">
              <div className="d-flex flex-column">
                {imageData.map((image, index) => (
                  <Button
                    key={image.id}
                    className="mb-2 p-1"
                    variant="light"
                    onClick={() => setSelectedImage(imageData[index])}
                  >
                    <img src={image.src} alt={image.alt} style={{ width: '60px' }} />
                  </Button>
                ))}
              </div>
            </Col>
          )}

          <Col md={center} className='bg-dark-subtle'>
            <ImageCamvasComponent key={selectedImage.id} imageSrc={selectedImage.src}/>
          </Col>

          {/* Right Panel: Display fake data */}
          {showRightPanel && (
            <Col md={right} className="d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end">
              <div className="border p-3">
                <h5>Data:</h5>
                <ul>
                  {fakeData.map((data) => (
                    <li key={data.id}>
                      {data.name}: {data.value}
                    </li>
                  ))}
                </ul>
              </div>
            </Col>
          )}
        </Row>
      </Container>
    </div>
  );
};

export default ImageManipulationComponent
