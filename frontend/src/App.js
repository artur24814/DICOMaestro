import React from "react"
import NavbarComponent from "./components/navbar.js"
import HomePage from "./pages/home/homePage.js"
import LoginPage from "./pages/login/loginPage.js"
import RedirectPage from "./pages/register/registerPage.js"
import FooterComponent from "./components/footer.js"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  return (
    <Router>
      <QueryClientProvider client={queryClient}>
        <NavbarComponent />

        <Routes>
          <Route path="/" Component={HomePage} />
          <Route path="/login" Component={LoginPage} />
          <Route path="/register" Component={RedirectPage} />
        </Routes>

        <FooterComponent />
      </QueryClientProvider>
    </Router>
  )
}

export default App;
