import React from 'react'
import { Navbar, Container, Nav } from 'react-bootstrap'
import { LuPencilLine } from 'react-icons/lu'
import { BiRectangle } from 'react-icons/bi'
import { FaPaintbrush } from 'react-icons/fa6'
import { FaPen, FaUndoAlt, FaRedoAlt } from 'react-icons/fa'
import LineTool from '../../../components/LineTool'
import RectangleTool from '../../../components/RectangleTool'
import PaintTool from '../../../components/PaintTool'
import DrawTool from '../../../components/DrawTool'

const ToolBarComponent = ({ handleSelectTool, undoMemento, redoMemento, handleCanvasChange, mementoName }) => {
  const handleUndo = () => {
    const canvasState = undoMemento(mementoName)
    if (canvasState !== null) {
      handleCanvasChange(canvasState)
    } else {
      console.warn(`No undo state available for ${mementoName}`)
    }
  }

  const handleRedo = () => {
    const canvasState = redoMemento(mementoName)
    if (canvasState !== null) {
      handleCanvasChange(canvasState)
    } else {
      console.warn(`No redo state available for ${mementoName}`)
    }
  }

  return (
    <Navbar bg='dark' variant='dark' className='p-0 m-0'>
      <Container fluid>
        <Nav className='me-auto'>
          <div className='vr text-white' />
          <Nav.Link onClick={() => handleUndo()}>
            <FaUndoAlt />
          </Nav.Link>
          <Nav.Link onClick={() => handleRedo()}>
            <FaRedoAlt />
          </Nav.Link>
          <div className='vr text-white' />
          <Nav.Link onClick={() => handleSelectTool(new DrawTool())}>
            <FaPen />
          </Nav.Link>
          <Nav.Link onClick={() => handleSelectTool(new PaintTool())}>
            <FaPaintbrush />
          </Nav.Link>
          <Nav.Link onClick={() => handleSelectTool(new LineTool())}>
            <LuPencilLine />
          </Nav.Link>
          <Nav.Link onClick={() => handleSelectTool(new RectangleTool())}>
            <BiRectangle />
          </Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  )
}

export default ToolBarComponent
