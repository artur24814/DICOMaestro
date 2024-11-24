import React from 'react'
import { Container } from 'react-bootstrap'

const SecuritySection = () => {
  return (
    <section id="security" className="py-5">
      <Container>
        <h2 className="fw-bold mb-4 text-center">Security You Can Trust</h2>
        <p className="lead text-center mb-4">
          DICOM Viewer ensures your data's privacy and security by implementing advanced processing methods:
        </p>
        <ul className="list-unstyled text-center lead">
          <li>💻 Image processing is done **locally in your browser** without saving data.</li>
          <li>🔒 Metadata and sensitive information are never stored or shared.</li>
          <li>🛠️ Backend operations support safe file loading without data retention.</li>
        </ul>
      </Container>
    </section>
  )
}

export default SecuritySection