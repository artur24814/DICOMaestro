import React from "react"
import { Container, Card, Form, Button, Row, Col } from 'react-bootstrap'
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import { FiUpload } from 'react-icons/fi'
import dicomUploadShema from "../validators/dicomUploadValidation"

const DicomFileUploadForm = ({ handleFormSubmit }) => {
  const {register, handleSubmit, formState: { errors }} = useForm({
    resolver: yupResolver(dicomUploadShema)
  })

  return (
    <Container className="mt-5 d-flex h-100 align-items-center justify-content-center"
      style={{ backgroundColor: '#ffffff', minHeight: '76vh' }}>
      <Card className="shadow-lg p-2" style={{ width: '40rem' }}>
        <Card.Body>
          <h2 className="text-center mb-4">
            <FiUpload className="me-2" />
            DICOM Uploader
          </h2>
          <Form onSubmit={handleSubmit(handleFormSubmit)}>
            <Form.Group controlId="formFile" className="mb-4">
              <Form.Label className="fw-semibold"><FiUpload /> Upload a file</Form.Label>
              <Form.Control
                type="file"
                accept=".dcm" {...register('dicomFile')}
              />
              <Form.Control.Feedback type="invalid" style={{ display: 'block', color: 'red', fontSize: '0.9em' }}>
                {errors.dicomFile?.message}
              </Form.Control.Feedback>
            </Form.Group>

            <Row className="mb-4">
              <Col>
                <Form.Group controlId="formatSelect">
                  <Form.Label className="fw-semibold">Format to return</Form.Label>
                  <Form.Select {...register('outputFormat')}>
                    <option value="2D">2d</option>
                    <option value="GIF">Gif</option>
                  </Form.Select>
                  <Form.Control.Feedback type="invalid" style={{ display: 'block', color: 'red', fontSize: '0.9em' }}>
                    {errors.outputFormat?.message}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
              <Col className="d-flex align-items-end">
                <Form.Check
                  type="checkbox"
                  label="Is this file 3D?"
                  {...register('is3d')}
                />
              </Col>
            </Row>

            <Button variant="primary" type="submit" className="w-100">
              Send
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  )
}

export default DicomFileUploadForm