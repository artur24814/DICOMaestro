import React from 'react'
import { Link } from 'react-router-dom'
import { Container, Navbar, Nav, NavDropdown} from 'react-bootstrap'
import '../styles/navbar.css'
import { LOGIN_PAGE_URL, REGISTER_PAGE_URL, HOME_PAGE_URL, DICOM_PROCESSING_UPLOAD } from '../consts/urls.js'
import { useAuth } from '../contexts/AuthContext.js'

const NavbarComponent = () => {
  const { isAuthenticated, user, logout } = useAuth()
  return (
    <Navbar bg="light" expand="lg" sticky="top" className="shadow-sm">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">DICOMaestro</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/#features" className="fw-bold">Features</Nav.Link>
            <Nav.Link href="/#security" className="fw-bold">Security</Nav.Link>
            <Nav.Link href="/#api" className="fw-bold">API</Nav.Link>
            <Nav.Link as={Link} to={DICOM_PROCESSING_UPLOAD} className="fw-bold">DICOM processing</Nav.Link>
          </Nav>
          {isAuthenticated ? (
            <Nav>
              <NavDropdown title={user} id="collapsible-nav-dropdown" className='mt-1'>
                <NavDropdown.Item href="#action/3.1" className="fw-bold">Action</NavDropdown.Item>
                <NavDropdown.Item as={Link} to='/' className="fw-bold">
                  Image processing
                </NavDropdown.Item>
              </NavDropdown>
              <Nav.Link as={Link} to={HOME_PAGE_URL} onClick={logout} className="fw-bold">
                logout
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