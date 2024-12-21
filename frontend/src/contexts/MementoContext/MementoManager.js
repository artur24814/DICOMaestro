import Memento from './Memento'

class MementoManager {
  constructor () {
    this.mementos = {}
  }

  create (name) {
    if (!this.mementos[name]) {
      this.mementos[name] = new Memento()
    }
  }

  save (name, state) {
    this.create(name)
    const memento = this.mementos[name]
    return memento.save(state)
  }

  undo (name) {
    const memento = this.mementos[name]
    if (memento) {
      return memento.undo()
    }
    return null
  }

  redo (name) {
    const memento = this.mementos[name]
    if (memento) {
      return memento.redo()
    }
    return null
  }

  getCurrentState (name) {
    const memento = this.mementos[name]
    return memento?.currentState || null
  }
}

export default MementoManager
