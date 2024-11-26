import React from "react"
import NavbarComponent from "./components/navbar.js"
import HomePage from "./pages/home/homePage.js"
import LoginPage from "./pages/login/loginPage.js"
import RedirectPage from "./pages/register/registerPage.js"
import FooterComponent from "./components/footer.js"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LOGIN_PAGE_URL, REGISTER_PAGE_URL, HOME_PAGE_URL } from "./consts/urls.js"
import AuthProvider from "./contexts/AuthContext.js"

const queryClient = new QueryClient()

function App() {
  return (
    <Router>
      <QueryClientProvider client={queryClient}>
        <AuthProvider >
          <NavbarComponent />

          <Routes>
            <Route path={HOME_PAGE_URL} element={<HomePage />} />
            <Route path={LOGIN_PAGE_URL} element={<LoginPage />} />
            <Route path={REGISTER_PAGE_URL} element={<RedirectPage />} />
          </Routes>

          <FooterComponent />
        </AuthProvider>
      </QueryClientProvider>
    </Router>
  )
}

export default App;
