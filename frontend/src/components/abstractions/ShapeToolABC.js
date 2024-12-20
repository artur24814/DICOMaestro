import DrawingTool from './DrawingToolABC'

class ShapeTool extends DrawingTool {
  constructor (color = 'black') {
    super(color)
    this.startPoint = null
    this.drawingShape = false
  }

  drawShape () {
    throw new Error('Method "drawShape()" must be implemented.')
  }

  onMouseDown (event, context) {
    const { offsetX, offsetY } = event.nativeEvent
    this.startPoint = { x: offsetX, y: offsetY }
    this.drawingShape = true

    const canvas = context.canvas
    const ctx = canvas.getContext('2d')
    this.canvasState = ctx.getImageData(0, 0, canvas.width, canvas.height)
  }

  onMouseMove (event, context) {
    if (this.startPoint && this.drawingShape) {
      const { offsetX, offsetY } = event.nativeEvent
      const canvas = context.canvas
      const ctx = canvas.getContext('2d')
      ctx.putImageData(this.canvasState, 0, 0)
      this.drawShape(offsetX, offsetY, ctx)
    }
  }

  onMouseUp (event, context) {
    this.drawingShape = false
    this.startPoint = null
  }

  onMouseOut (event, context) {
    if (this.drawingShape) {
      const canvas = context.canvas
      const ctx = canvas.getContext('2d')

      ctx.putImageData(this.canvasState, 0, 0)
      this.drawingRectangle = false
      this.startPoint = null
    }
  }
}

export default ShapeTool
