import * as yup from 'yup'

const dicomUploadShema = yup.object().shape({
  dicomFile: yup.mixed().required("File is required").test(
    'fileFormat', 'Invalid file extension. Allowed: .dcm, .DCM, .zip', (value) => {
      if (!value || value === 0) return false
      const allowedExtensions = ['.dcm', '.zip']
      const fileName = value[0]?.name.toLowerCase() || ''
      return allowedExtensions.some((ext) => fileName.endsWith(ext))
    }
  ),
  is3d: yup.boolean(),
  outputFormat: yup.string().oneOf(['2D', 'GIF'], 'Invalid format')
})

export default dicomUploadShema