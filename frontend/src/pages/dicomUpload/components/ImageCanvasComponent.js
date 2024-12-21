import React, { useRef, useEffect } from 'react'
import { Container } from 'react-bootstrap'

const ImageCamvasComponent = ({ imageSrc, activeTool, saveMemento, mementoName }) => {
  const canvasRef = useRef(null)

  const handleMouseDown = (event) => {
    if (activeTool) activeTool.onMouseDown(event, { canvas: canvasRef.current })
  }

  const handleMouseMove = (event) => {
    if (activeTool) activeTool.onMouseMove(event, { canvas: canvasRef.current })
  }

  const handleMouseUp = (event) => {
    if (activeTool) {
      activeTool.onMouseUp(event, { canvas: canvasRef.current, saveMemento })

      const ctx = canvasRef.current.getContext('2d')
      const canvasState = ctx.getImageData(0, 0, canvasRef.current.width, canvasRef.current.height)
      saveMemento(mementoName, canvasState)
    }
  }

  const handleMouseOut = (event) => {
    if (activeTool) activeTool.onMouseOut(event, { canvas: canvasRef.current })
  }

  const handleRightClick = (event) => {
    if (activeTool) activeTool.onRightClick(event, { canvas: canvasRef.current })
  }

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')

    if (imageSrc && imageSrc.data) {
      canvas.width = imageSrc.width
      canvas.height = imageSrc.height
      ctx.putImageData(imageSrc, 0, 0)
    } else if (typeof imageSrc === 'string') {
      const img = new Image()
      img.src = imageSrc
      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img, 0, 0, img.width, img.height)
      }
    }
  }, [imageSrc])

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
