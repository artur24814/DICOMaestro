import DrawingTool from './abstractions/DrawingToolABC'

class PaintTool extends DrawingTool {
  constructor (color = 'black') {
    super(color)
    this.painting = false
  }

  onMouseDown (event, context) {
    this.painting = true
    this.paint(event, context)
  }

  onMouseMove (event, context) {
    if (this.painting) {
      this.paint(event, context)
    }
  }

  onMouseUp (event, context) {
    this.painting = false
  }

  onMouseOut (event, context) {
    this.painting = false
  }

  paint (event, context) {
    const { offsetX, offsetY } = event.nativeEvent
    const canvas = context.canvas
    const ctx = canvas.getContext('2d')

    ctx.beginPath()
    ctx.arc(offsetX, offsetY, 5, 0, Math.PI * 2)
    ctx.fillStyle = this.color
    ctx.fill()
  }
}

export default PaintTool
