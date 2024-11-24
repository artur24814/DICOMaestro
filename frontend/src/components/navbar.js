import React from 'react'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Container, Navbar, Nav, NavDropdown, Button } from 'react-bootstrap'
import '../styles/navbar.css'
import api from '../api/axiosConfig.js'

const NavbarComponent = () => {
  const isAuthenticated = false
  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="navbar-custom">
      <Container>
        <Navbar.Brand as={Link} to="/">DICOMaestro</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to='/'>action</Nav.Link>
          </Nav>
          {isAuthenticated ? (
            <Nav>
              <NavDropdown title={'user'} id="collapsible-nav-dropdown" className='mt-1'>
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item as={Link} to='/'>
                  Image processing
                </NavDropdown.Item>
              </NavDropdown>
              <Nav.Link as={Link} to="/">
                <Button variant="outline-light"  className="me-2">
                  Logout
                </Button>
              </Nav.Link>
            </Nav>
          ) : (
            <Nav>
              <Nav.Link as={Link} to="/login">
                <Button variant="outline-light" className="me-2">
                  Login
                </Button>
              </Nav.Link>
              <Nav.Link as={Link} to="/register">
                <Button variant="outline-light" className="me-2">
                  Register
                </Button>
              </Nav.Link>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default NavbarComponent