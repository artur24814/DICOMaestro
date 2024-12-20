import React from 'react'
import { Button } from 'react-bootstrap'

const LeftPanel = ({ imageObjects, setSelectedImage, toggleLeftPanel }) => {
  return (
    <>
      <div className='d-flex justify-content-between m-0 mt-1 p-0'>
        <h5>Files</h5>
        <Button className='btn-close' onClick={toggleLeftPanel} />
      </div>
      <div className='d-flex flex-column mt-1'>
        {imageObjects.map((image, index) => (
          <Button
            key={image.id}
            className='mb-2 p-1'
            variant='light'
            onClick={() => setSelectedImage(imageObjects[index])}
          >
            <img src={image.src} alt={image.alt} style={{ width: '60px' }} />
          </Button>
        ))}
      </div>
    </>
  )
}

export default LeftPanel
