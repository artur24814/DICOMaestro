import React, { useRef, useEffect } from 'react'
import { Container } from 'react-bootstrap'

const ImageCamvasComponent = ({ imageSrc, activeTool }) => {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (imageSrc) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      const img = new Image()
      img.src = imageSrc
      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img, 0, 0, img.width, img.height)
      }
    }
  }, [imageSrc])

  const handleMouseDown = (event) => {
    if (activeTool) activeTool.onMouseDown(event, { canvas: canvasRef.current })
  }

  const handleMouseMove = (event) => {
    if (activeTool) activeTool.onMouseMove(event, { canvas: canvasRef.current })
  }

  const handleMouseUp = (event) => {
    if (activeTool) activeTool.onMouseUp(event, { canvas: canvasRef.current })
  }

  const handleMouseOut = (event) => {
    if (activeTool) activeTool.onMouseOut(event, { canvas: canvasRef.current })
  }

  const handleRightClick = (event) => {
    if (activeTool) activeTool.onRightClick(event, { canvas: canvasRef.current })
  }

  return (
    <Container className='d-flex align-items-center justify-content-center min-vh-100'>
      <canvas
        ref={canvasRef}
        style={{
          border: '1px solid black',
          borderRadius: '8px',
          maxWidth: '100%',
          display: imageSrc ? 'block' : 'none'
        }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseOut={handleMouseOut}
        onContextMenu={handleRightClick}
      />
      {!imageSrc && (
        <p style={{ color: 'gray' }}>No image to display on canvas.</p>
      )}
    </Container>
  )
}

export default ImageCamvasComponent
