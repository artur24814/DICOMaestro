/* eslint-disable react/jsx-curly-spacing, multiline-ternary */

import React, { useState, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
import withAuth from '../../utils/withAuth'
import api from '../../api/axiosConfig.js'
import { DICOM_READ_API_URL } from '../../consts/apiUrls.js'
import DicomFileUploadForm from './components/DicomFileUploadForm.js'
import ImageManipulationComponent from './components/ImageManipulationComponent.js'
import FullScreenSpinner from '../../components/fullScreenSpiner.js'
import './DicomUploadPage.css'

const DicomUploadPage = () => {
  const [dicomFile, setDicomFile] = useState()

  const fetchDicomMetadata = useCallback(async () => {
    if (!dicomFile) return
    const formData = new FormData()
    formData.append('file', dicomFile)

    const response = await api.post(DICOM_READ_API_URL, formData, {
      headers: {
        ...api.defaults.headers.common,
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }, [dicomFile])

  const { data: dicomMetadata, isLoading } = useQuery({
    queryKey: dicomFile ? ['dicomMetadata', dicomFile.name] : null,
    queryFn: fetchDicomMetadata,
    enabled: !!dicomFile,
    staleTime: 60000
  })

  const handleSubmit = (data) => {
    if (data.dicomFile && data.dicomFile[0] !== dicomFile) {
      setDicomFile(data.dicomFile[0])
    }
  }

  return (
    <>
      {!dicomFile ? (
        <DicomFileUploadForm handleFormSubmit={ handleSubmit } />
      ) : isLoading ? (
        <FullScreenSpinner />
      ) : (
        <ImageManipulationComponent metadata={dicomMetadata} />
      )}
    </>
  )
}

export default withAuth(DicomUploadPage)
