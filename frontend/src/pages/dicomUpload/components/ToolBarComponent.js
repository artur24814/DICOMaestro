import React from 'react'
import { Navbar, Container, Nav } from 'react-bootstrap'
import { LuPencilLine } from 'react-icons/lu'
import { BiRectangle } from 'react-icons/bi'
import { FaPaintbrush } from 'react-icons/fa6'
import { FaPen } from 'react-icons/fa'
import LineTool from '../../../components/LineTool'
import RectangleTool from '../../../components/RectangleTool'
import PaintTool from '../../../components/PaintTool'
import DrawTool from '../../../components/DrawTool'

const ToolBarComponent = ({ handleSelectTool }) => {
  return (
    <Navbar bg='dark' variant='dark' className='p-0 m-0'>
      <Container fluid>
        <Nav className='me-auto'>
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
