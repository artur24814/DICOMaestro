import Memento from '../../src/contexts/MementoContext/Memento.js'

describe('Memento Class', () => {
  let memento

  beforeEach(() => {
    memento = new Memento()
  })

  test('should initialize with empty history and current state as null', () => {
    expect(memento.history).toEqual([])
    expect(memento.currentState).toBeNull()
  })

  test('should save a state and update the current state', () => {
    const state1 = { data: 'state1' }
    memento.save(state1)
    expect(memento.currentState).toEqual(state1)
    expect(memento.history).toEqual([state1])
  })

  test('should undo to the previous state', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    memento.save(state1)
    memento.save(state2)
    const undoneState = memento.undo()
    expect(undoneState).toEqual(state1)
    expect(memento.currentState).toEqual(state1)
  })

  test('should not undo when at the oldest state', () => {
    const state1 = { data: 'state1' }
    memento.save(state1)
    memento.undo()
    const undoneState = memento.undo()
    expect(undoneState).toBeNull()
    expect(memento.currentState).toEqual(state1)
  })

  test('should redo to the next state', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    memento.save(state1)
    memento.save(state2)
    memento.undo()
    const redoneState = memento.redo()
    expect(redoneState).toEqual(state2)
    expect(memento.currentState).toEqual(state2)
  })

  test('should not redo when at the newest state', () => {
    const state1 = { data: 'state1' }
    memento.save(state1)
    const redoneState = memento.redo()
    expect(redoneState).toBeNull()
    expect(memento.currentState).toEqual(state1)
  })

  test('should remove future states when saving a new state after undo', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    const state3 = { data: 'state3' }
    memento.save(state1)
    memento.save(state2)
    memento.undo()
    memento.save(state3)
    expect(memento.history).toEqual([state1, state3])
    expect(memento.currentState).toEqual(state3)
  })

  test('should limit the number of saved states to maxHistorySize', () => {
    const memento = new Memento(3)
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    const state3 = { data: 'state3' }
    const state4 = { data: 'state4' }

    memento.save(state1)
    memento.save(state2)
    memento.save(state3)
    memento.save(state4)

    // The oldest state (state1) has been deleted, so only state2, state3 and state4 are in the history
    expect(memento.history).toEqual([state2, state3, state4])
    expect(memento.currentIndex).toBe(2)
  })

  test('should maintain functionality with maxHistorySize', () => {
    const memento = new Memento(2)
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    const state3 = { data: 'state3' }

    memento.save(state1)
    memento.save(state2)
    memento.save(state3)

    // The oldest state (state1) has been deleted, so only state2 and state3 are in the history
    expect(memento.history).toEqual([state2, state3])
    expect(memento.currentState).toEqual(state3)

    memento.undo()
    expect(memento.currentState).toEqual(state2)

    memento.redo()
    expect(memento.currentState).toEqual(state3)
  })
})
