import MementoManager from '../../src/contexts/MementoContext/MementoManager'

describe('MementoManager Class', () => {
  let manager

  beforeEach(() => {
    manager = new MementoManager()
  })

  test('should create a new memento when saving a state', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }

    manager.save('item1', state1)
    expect(manager.getCurrentState('item1')).toEqual(state1)

    manager.save('item1', state2)
    expect(manager.getCurrentState('item1')).toEqual(state2)

    // try to save again, return alredy existed
    manager.save('item1', state1)
    expect(manager.getCurrentState('item1')).toEqual(state1)
  })

  test('should undo to the previous state', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }

    manager.save('item1', state1)
    manager.save('item1', state2)

    const undoneState = manager.undo('item1')
    expect(undoneState).toEqual(state1)
    expect(manager.getCurrentState('item1')).toEqual(state1)
  })

  test('should redo to the next state', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }

    manager.save('item1', state1)
    manager.save('item1', state2)
    manager.undo('item1')

    expect(manager.redo('item1')).toEqual(state2)
    expect(manager.getCurrentState('item1')).toEqual(state2)
  })

  test('should not undo when at the oldest state', () => {
    const state1 = { data: 'state1' }

    manager.save('item1', state1)
    expect(manager.undo('item1')).toBeNull()

    // undo again
    expect(manager.undo('item1')).toBeNull()
    expect(manager.getCurrentState('item1')).toEqual(state1)
  })

  test('should return null if memento does not exist for the given name', () => {
    const state1 = { data: 'state1' }

    manager.save('item1', state1)
    expect(manager.getCurrentState('item2')).toBeNull()
    expect(manager.undo('item2')).toBeNull()
    expect(manager.redo('item2')).toBeNull()
  })

  test('should create multiple mementos for different names', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }
    const state3 = { data: 'state3' }

    manager.save('item1', state1)
    manager.save('item2', state2)
    manager.save('item1', state3)

    expect(manager.getCurrentState('item1')).toEqual(state3)
    expect(manager.getCurrentState('item2')).toEqual(state2)
  })

  test('should not overwrite an existing memento when calling save again for the same name', () => {
    const state1 = { data: 'state1' }
    const state2 = { data: 'state2' }

    manager.save('item1', state1)
    // try create again
    manager.save('item1', state2)

    expect(manager.getCurrentState('item1')).toEqual(state2)
  })
})
