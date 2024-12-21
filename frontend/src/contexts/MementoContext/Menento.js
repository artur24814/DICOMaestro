const MAX_HISTORY_SIZE = 30

class Memento {
  constructor (maxHistorySize = MAX_HISTORY_SIZE) {
    this.history = []
    this.currentIndex = -1
    this.maxHistorySize = maxHistorySize
  }

  save (state) {
    // Delete future states if we add a new one
    if (this.currentIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.currentIndex + 1)
    }
    this.history.push(state)
    this.currentIndex++

    if (this.history.length > this.maxHistorySize) {
      this.history.shift()
      this.currentIndex--
    }
    return state
  }

  undo () {
    if (this.currentIndex >= 0) {
      this.currentIndex--
      return this.history[this.currentIndex]
    }
    return null
  }

  redo () {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++
      return this.history[this.currentIndex]
    }
    return null
  }

  get currentState () {
    return this.currentIndex >= 0 ? this.history[this.currentIndex] : null
  }
}

export default Memento
