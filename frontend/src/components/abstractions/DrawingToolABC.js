class DrawingTool {
  constructor (color = 'black', lineWidth = 2) {
    if (new.target === DrawingTool) {
      throw new Error('Cannot instantiate an abstract class')
    }
    this.color = color
    this.lineWidth = lineWidth
  }

  onMouseDown (event, context) {
    throw new Error('Method "onMouseDown" must be implemented.')
  }

  onMouseMove (event, context) {
    throw new Error('Method "onMouseMove" must be implemented.')
  }

  onMouseUp (event, context) {
    throw new Error('Method "onMouseUp" must be implemented.')
  }

  onMouseOut (event, context) {
    throw new Error('Method "onMouseOut" must be implemented.')
  }

  onRightClick (event, context) {
    throw new Error('Method "onRightClick" must be implemented.')
  }
}

export default DrawingTool
