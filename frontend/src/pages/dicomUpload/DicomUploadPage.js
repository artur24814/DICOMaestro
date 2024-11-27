import React, { useState } from 'react'
import withAuth from '../../utils/withAuth'
import DicomFileUploadForm from './components/DicomFileUploadForm.js'
import ImageManipulationComponent from './components/ImageManipulationComponent.js'

const DicomUploadPage = () => {
  const [dicomFile, setDicomFile ] = useState()
  const handleSubmit = (data) => {
    setDicomFile(data.dicomFile[0])
    console.log('Uploaded file:', data.dicomFile[0])
    console.log('Is 3D:', data.is3d)
    console.log('Output format:', data.outputFormat)
  }

  return (
    <>
      {!dicomFile ? (
        <DicomFileUploadForm handleFormSubmit={handleSubmit}/>
        ) : (
        <ImageManipulationComponent />
        )}
    </>
  )
}

export default withAuth(DicomUploadPage)
