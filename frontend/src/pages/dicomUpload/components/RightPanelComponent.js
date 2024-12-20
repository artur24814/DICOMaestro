import React from 'react'
import { Row, Col, Button, Card } from 'react-bootstrap'

const RightPanel = ({ toggleRightPanel, metaDataTable }) => {
  return (
    <>
      <div className='d-flex justify-content-between m-0 mt-1 p-0'>
        <h5>Metadata:</h5>
        <Button className='btn-close' onClick={toggleRightPanel} />
      </div>
      <Row xs={1} md={1} lg={1} className='g-2 pb-3'>
        {metaDataTable.map(([key, value], index) => (
          <Col key={index}>
            <Card>
              <Card.Body className='p-2'>
                <Card.Title className='fs-6'>{key}</Card.Title>
                <Card.Text className='text-muted p-0' style={{ fontSize: '0.8rem' }}>
                  {typeof value === 'object' ? JSON.stringify(value, null, 2) : value}
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </>
  )
}

export default RightPanel
