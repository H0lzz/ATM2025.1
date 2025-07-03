import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import AdminMenu from "./pages/AdminMenu"
import ClientMenu from "./pages/ClientMenu"

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/admin" element={<AdminMenu />} />
        <Route path="/client" element={<ClientMenu />} />
      </Routes>
    </BrowserRouter>
  )
}
