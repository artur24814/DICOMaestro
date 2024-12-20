import DrawingTool from './abstractions/DrawingToolABC'

class DrawTool extends DrawingTool {
  constructor (color = 'red', lineWidth = 2) {
    super(color, lineWidth)
    this.drawing = false
  }

  onMouseDown (event, context) {
    this.drawing = true
    this.draw(event, context)
  }

  onMouseMove (event, context) {
    if (this.drawing) {
      this.draw(event, context)
    }
  }

  onMouseUp (event, context) {
    this.drawing = false
  }

  onMouseOut (event, context) {
    this.drawing = false
  }

  draw (event, context) {
    const canvas = context.canvas
    const rect = canvas.getBoundingClientRect()
    const ctx = canvas.getContext('2d')
    ctx.lineTo(event.clientX - rect.left, event.clientY - rect.top)
    ctx.strokeStyle = this.color
    ctx.lineWidth = this.lineWidth
    ctx.stroke()
  }
}

export default DrawTool
