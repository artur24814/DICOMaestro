import DrawingTool from './abstractions/DrawingToolABC.js'

class LineTool extends DrawingTool {
  constructor (color = 'black', lineWidth = 2) {
    super(color, lineWidth)
    this.startPoint = null
  }

  onMouseDown (event, context) {
    const { offsetX, offsetY } = event.nativeEvent
    this.startPoint = { x: offsetX, y: offsetY }

    const canvas = context.canvas
    const ctx = canvas.getContext('2d')
    this.canvasState = ctx.getImageData(0, 0, canvas.width, canvas.height)
  }

  onMouseMove (event, context) {
    if (this.startPoint) {
      const { offsetX, offsetY } = event.nativeEvent
      const canvas = context.canvas
      const ctx = canvas.getContext('2d')

      ctx.putImageData(this.canvasState, 0, 0)

      ctx.beginPath()
      ctx.moveTo(this.startPoint.x, this.startPoint.y)
      ctx.lineTo(offsetX, offsetY)
      ctx.strokeStyle = this.color
      ctx.lineWidth = this.lineWidth
      ctx.stroke()
    }
  }

  onMouseUp (event, context) {
    this.drawingLine = false
    this.startPoint = null
  }

  onMouseOut (event, context) {
    if (this.drawingLine) {
      const canvas = context.canvas
      const ctx = canvas.getContext('2d')

      ctx.putImageData(this.canvasState, 0, 0)
      this.drawingLine = false
      this.startPoint = null
    }
  }

  onRightClick (event, context) {
    event.preventDefault()
    if (this.drawingLine) {
      const canvas = context.canvas
      const ctx = canvas.getContext('2d')

      ctx.putImageData(this.canvasState, 0, 0)
      this.drawingLine = false
      this.startPoint = null
    }
  }
}

export default LineTool
