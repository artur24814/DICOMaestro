import React, { useState } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import ImageCamvasComponent from './ImageCamvasComponent'
import ToolBarComponent from './ToolBarComponent'
import LeftPanel from './LeftPanelComponent'
import RightPanel from './RightPanelComponent'

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
      <ToolBarComponent handleSelectTool={handleSelectTool} />

      <Container fluid className='min-vh-100'>
        <Row>

          {showLeftPanel && (
            <Col
              md={left}
              className='d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end images-container position-relative'
            >
              <LeftPanel
                imageObjects={imageObjects}
                setSelectedImage={setSelectedImage}
                toggleLeftPanel={toggleLeftPanel}
              />
            </Col>
          )}
          {!showLeftPanel && (
            <Button
              onClick={toggleLeftPanel}
              className='position-absolute top-50 translate-middle-y start-0 open-button bg-body-secondary move-right'
            >
              &#x276F;
            </Button>
          )}

          <Col md={center} className='bg-dark bg-gradient'>
            <ImageCamvasComponent key={selectedImage.id} imageSrc={selectedImage.src} activeTool={activeTool} />
          </Col>

          {showRightPanel && (
            <Col
              md={right}
              className='d-none d-md-block bg-body-secondary bg-gradient border border-1 border-end table-container pt-3'
            >
              <RightPanel
                toggleRightPanel={toggleRightPanel}
                metaDataTable={metaDataTable}
              />
            </Col>
          )}

          {!showRightPanel && (
            <Button
              onClick={toggleRightPanel}
              className='position-absolute top-50 translate-middle-y end-0 open-button bg-body-secondary move-left'
            >
              &#x276F;
            </Button>
          )}
        </Row>
      </Container>
    </div>
  )
}

export default ImageManipulationComponent
