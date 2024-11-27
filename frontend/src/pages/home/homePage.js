import React from 'react'
import HeroSection from './components/heroSection'
import FeaturesSection from './components/featuresSection'
import SecuritySection from './components/securitySection'
import DICOMInformationSection from './components/dicomInfoSection'
import APISection from './components/apiSection'

const HomePage = () => {
  return (
    <>
      <HeroSection />
      <FeaturesSection />
      <SecuritySection />
      <DICOMInformationSection />
      <APISection />
    </>
  )
}

export default HomePage