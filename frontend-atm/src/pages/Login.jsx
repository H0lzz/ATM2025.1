import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/api"

export default function Login() {
  const [accountNumber, setAccountNumber] = useState("")
  const [pin, setPin] = useState("")
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const response = await api.post("/auth", {
        account_number: Number(accountNumber),
        pin: Number(pin),
      })

      const { is_admin } = response.data

      if (response.data.status === "Authenticated") {
        localStorage.setItem("accountNumber", accountNumber);

        if (response.data.is_admin) {
          navigate("/admin", { state: { accountNumber } });
        } else {
          navigate("/client", { state: { accountNumber } });
        }
      }
    } catch (err) {
      alert("Erro na autenticação: " + (err.response?.data?.detail || "desconhecido"))
    }
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4 bg-gray-100">
      <h1 className="text-2xl font-bold">Login</h1>
      <input
        className="border p-2 rounded"
        placeholder="Número da Conta"
        value={accountNumber}
        onChange={(e) => setAccountNumber(e.target.value)}
      />
      <input
        className="border p-2 rounded"
        placeholder="PIN"
        type="password"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleLogin}
      >
        Entrar
      </button>
    </div>
  )
}
