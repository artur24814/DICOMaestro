import ShapeTool from './abstractions/ShapeToolABC'

class RectangleTool extends ShapeTool {
  constructor (color = 'black') {
    super(color)
  }

  drawShape (offsetX, offsetY, ctx) {
    const width = offsetX - this.startPoint.x
    const height = offsetY - this.startPoint.y
    ctx.beginPath()
    ctx.rect(this.startPoint.x, this.startPoint.y, width, height)
    ctx.strokeStyle = this.color
    ctx.stroke()
  }
}

export default RectangleTool
