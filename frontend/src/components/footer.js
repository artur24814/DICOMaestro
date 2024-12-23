import React from 'react'
import { Container } from 'react-bootstrap'
import { FaGithub } from 'react-icons/fa'

const FooterComponent = () => {
  return (
    <footer className='bg-dark text-white py-3'>
      <Container className='d-flex justify-content-between'>
        <p className='mb-0'>Open-source under MIT License. © 2024 DICOMaestro.</p>
        <a href='https://github.com/artur24814/DICOMaestro' target='_blank' rel='noopener noreferrer' className='text-white'>
          <FaGithub size={24} /> GitHub
        </a>
      </Container>
    </footer>
  )
}

export default FooterComponent
