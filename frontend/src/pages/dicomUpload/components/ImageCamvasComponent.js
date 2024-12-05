import React, { useRef, useEffect, useState } from 'react'
import { Container } from 'react-bootstrap'

const ImageCamvasComponent = ({ imageSrc }) => {
  const canvasRef = useRef(null)
  const [isDrawing, setIsDrawing] = useState(false)

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

  const startDrawing = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top)
    setIsDrawing(true)
  }

  const draw = (e) => {
    if (!isDrawing) return
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const ctx = canvas.getContext('2d')
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top)
    ctx.strokeStyle = 'red'
    ctx.lineWidth = 2
    ctx.stroke()
  }

  const stopDrawing = () => {
    setIsDrawing(false)
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
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseOut={stopDrawing}
      />
      {!imageSrc && (
        <p style={{ color: 'gray' }}>No image to display on canvas.</p>
      )}
    </Container>
  )
}

export default ImageCamvasComponent
