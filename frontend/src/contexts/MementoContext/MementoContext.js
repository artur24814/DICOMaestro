import React, { createContext, useContext } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import MementoManager from './MementoManager'

const MementoContext = createContext()

export const MEMENTO_MANGER_NAME = 'mementoManager'

export const MementoProvider = ({ children }) => {
  const queryClient = useQueryClient()

  const getMementoManagerFromCache = () => {
    const cachedMementoManager = queryClient.getQueryData([MEMENTO_MANGER_NAME])
    if (cachedMementoManager) {
      return cachedMementoManager
    }
    const newMementoManager = new MementoManager()
    queryClient.setQueryData([MEMENTO_MANGER_NAME], newMementoManager)
    return newMementoManager
  }

  const saveMemento = (name, state) => {
    const mementoManager = getMementoManagerFromCache()
    mementoManager.save(name, state)
    queryClient.setQueryData([MEMENTO_MANGER_NAME], mementoManager)
    return state
  }

  const undoMemento = (name) => {
    const mementoManager = getMementoManagerFromCache()
    const state = mementoManager.undo(name)
    queryClient.setQueryData([MEMENTO_MANGER_NAME], mementoManager)
    return state
  }

  const redoMemento = (name) => {
    const mementoManager = getMementoManagerFromCache()
    const state = mementoManager.redo(name)
    queryClient.setQueryData([MEMENTO_MANGER_NAME], mementoManager)
    return state
  }

  const currentMementoState = (name) => {
    const mementoManager = getMementoManagerFromCache()
    return mementoManager.getCurrentState(name)
  }

  return (
    <MementoContext.Provider value={{
      saveMemento,
      undoMemento,
      redoMemento,
      currentMementoState
    }}
    >
      {children}
    </MementoContext.Provider>
  )
}

export const useMemento = () => useContext(MementoContext)
