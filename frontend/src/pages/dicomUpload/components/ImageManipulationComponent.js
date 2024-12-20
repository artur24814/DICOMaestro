import React, { useState } from 'react'
import { Container, Row, Col, Button, Navbar, Nav, Card } from 'react-bootstrap'
import { LuPencilLine, LuPanelLeftOpen, LuPanelLeftClose, LuPanelRightOpen, LuPanelRightClose } from 'react-icons/lu'
import { BiRectangle } from 'react-icons/bi'
import { FaPaintbrush } from 'react-icons/fa6'
import { FaPen } from 'react-icons/fa'
import ImageCamvasComponent from './ImageCamvasComponent'
import LineTool from '../../../components/LineTool'
import RectangleTool from '../../../components/RectangleTool'
import PaintTool from '../../../components/PaintTool'
import DrawTool from '../../../components/DrawTool'

const ImageManipulationComponent = (metadata) => {
  const metaDataTable = Object.entries(metadata.metadata).filter(([key]) => key !== 'Images' && key !== 'PixelData')
  const imageObjects = metadata.metadata.Images.map((url, index) => ({
    id: index + 1,
    src: `data:image/png;base64,${url}`,
    alt: `Image ${index + 1}`
  }))

  const [showLeftPanel, setShowLeftPanel] = useState(true)
  const [showRightPanel, setShowRightPanel] = useState(true)
  const [selectedImage, setSelectedImage] = useState(imageObjects[0])
  const [activeTool, setActiveTool] = useState(null)

  const toggleLeftPanel = () => setShowLeftPanel(!showLeftPanel)
  const toggleRightPanel = () => setShowRightPanel(!showRightPanel)
  const handleSelectTool = (tool) => setActiveTool(tool)

  const getColSizes = () => {
    if (showLeftPanel && showRightPanel) return { left: 1, center: 9, right: 2 }
    if (showLeftPanel && !showRightPanel) return { left: 1, center: 11, right: 0 }
    if (!showLeftPanel && showRightPanel) return { left: 0, center: 10, right: 2 }
    return { left: 0, center: 12, right: 0 }
  }

  const { left, center, right } = getColSizes()

  return (
    <div>
      <Navbar bg='dark' variant='dark' className='p-0 m-0'>
        <Container fluid>
          <Nav className='me-auto'>
            <div className='vr text-white' />
            <Nav.Link onClick={toggleLeftPanel}>
              {showLeftPanel ? <LuPanelLeftClose /> : <LuPanelLeftOpen />}
            </Nav.Link>
            <Nav.Link onClick={toggleRightPanel}>
              {showRightPanel ? <LuPanelRightClose /> : <LuPanelRightOpen />}
            </Nav.Link>
            <div className='vr text-white' />
            <Nav.Link onClick={() => handleSelectTool(new DrawTool())}>
              <FaPen />
            </Nav.Link>
            <Nav.Link onClick={() => handleSelectTool(new PaintTool())}>
              <FaPaintbrush />
            </Nav.Link>
            <Nav.Link onClick={() => handleSelectTool(new LineTool())}>
              <LuPencilLine />
            </Nav.Link>
            <Nav.Link onClick={() => handleSelectTool(new RectangleTool())}>
              <BiRectangle />
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <Container fluid className='min-vh-100'>
        <Row>

          {/* Left Panel: Thumbnails */}
          {showLeftPanel && (
            <Col md={left} className='d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end images-container'>
              <div className='d-flex flex-column'>
                {imageObjects.map((image, index) => (
                  <Button
                    key={image.id}
                    className='mb-2 p-1'
                    variant='light'
                    onClick={() => setSelectedImage(imageObjects[index])}
                  >
                    <img src={image.src} alt={image.alt} style={{ width: '60px' }} />
                  </Button>
                ))}
              </div>
            </Col>
          )}

          <Col md={center} className='bg-dark bg-gradient'>
            <ImageCamvasComponent key={selectedImage.id} imageSrc={selectedImage.src} activeTool={activeTool} />
          </Col>

          {/* Right Panel: Display fake data */}
          {showRightPanel && (
            <Col md={right} className='d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end table-container pt-3'>
              <h5>Metadata:</h5>
              <Row xs={1} md={1} lg={1} className='g-2 pb-3'>
                {metaDataTable.map(([key, value], index) => (
                  <Col key={index}>
                    <Card>
                      <Card.Body className='p-2'>
                        <Card.Title className='fs-6'>{key}</Card.Title>
                        <Card.Text className='text-muted p-0' style={{ fontSize: '0.8rem' }}>
                          {typeof value === 'object' ? JSON.stringify(value, null, 2) : value}
                        </Card.Text>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Col>
          )}
        </Row>
      </Container>
    </div>
  )
}

export default ImageManipulationComponent
