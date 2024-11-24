import React from 'react'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Container, Navbar, Nav, NavDropdown, Button } from 'react-bootstrap'
import '../styles/navbar.css'
import api from '../api/axiosConfig.js'
import { LOGIN_PAGE_URL, REGISTER_PAGE_URL, HOME_PAGE_URL } from '../consts/urls.js'

const NavbarComponent = () => {
  const isAuthenticated = false
  return (
    <Navbar bg="light" expand="lg" sticky="top" className="shadow-sm">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">DICOMaestro</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            {/* <Nav.Link as={Link} to='/' className="fw-bold">action</Nav.Link> */}
            <Nav.Link href="/#features" className="fw-bold">Features</Nav.Link>
            <Nav.Link href="/#security" className="fw-bold">Security</Nav.Link>
            <Nav.Link href="/#api" className="fw-bold">API</Nav.Link>
          </Nav>
          {isAuthenticated ? (
            <Nav>
              <NavDropdown title={'user'} id="collapsible-nav-dropdown" className='mt-1'>
                <NavDropdown.Item href="#action/3.1" className="fw-bold">Action</NavDropdown.Item>
                <NavDropdown.Item as={Link} to='/' className="fw-bold">
                  Image processing
                </NavDropdown.Item>
              </NavDropdown>
              <Nav.Link as={Link} to={HOME_PAGE_URL}>
                <Button variant="outline-light"  className="me-2">
                  Logout
                </Button>
              </Nav.Link>
            </Nav>
          ) : (
            <Nav>
              <Nav.Link as={Link} to={LOGIN_PAGE_URL} className="fw-bold">
                  Login
              </Nav.Link>
              <Nav.Link as={Link} to={REGISTER_PAGE_URL} className="fw-bold">
                  Register
              </Nav.Link>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default NavbarComponent