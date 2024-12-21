import React from 'react'
import { render, screen, act } from '@testing-library/react'
import { MementoProvider, useMemento } from '../../src/contexts/MementoContext/MementoContext'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import MementoManager from '../../src/contexts/MementoContext/MementoManager'

const MEMENTO_MANGER_NAME = 'mementoManager'
const queryClient = new QueryClient()

const TestComponent = () => {
  const { saveMemento, undoMemento, redoMemento, currentMementoState } = useMemento()

  const state1 = { data: 'state1' }
  const state2 = { data: 'state2' }

  return (
    <div>
      <button onClick={() => saveMemento('item1', state1)}>Save State 1</button>
      <button onClick={() => saveMemento('item1', state2)}>Save State 2</button>
      <button onClick={() => undoMemento('item1')}>Undo</button>
      <button onClick={() => redoMemento('item1')}>Redo</button>
      <div data-testid='current-state'>{JSON.stringify(currentMementoState('item1'))}</div>
    </div>
  )
}

const renderWithProvider = (ui) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MementoProvider>{ui}</MementoProvider>
    </QueryClientProvider>
  )
}

describe('MementoContext', () => {
  test('should interact with MementoManager and update cache', async () => {
    renderWithProvider(<TestComponent />)

    const saveState1Button = screen.getByText('Save State 1')
    const saveState2Button = screen.getByText('Save State 2')

    act(() => {
      saveState1Button.click()
    })
    let cachedMementoManager = queryClient.getQueryData([MEMENTO_MANGER_NAME])
    expect(cachedMementoManager).toBeInstanceOf(MementoManager)
    expect(cachedMementoManager.getCurrentState('item1')).toEqual({ data: 'state1' })

    act(() => {
      saveState2Button.click()
    })
    cachedMementoManager = queryClient.getQueryData([MEMENTO_MANGER_NAME])
    expect(cachedMementoManager.getCurrentState('item1')).toEqual({ data: 'state2' })
  })
})
