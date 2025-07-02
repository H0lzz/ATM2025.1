import { useState } from "react";
import api from "../api/api";

export default function DepositForm({ accountNumber, onSuccess }) {
  const [amount, setAmount] = useState("");

  const handleDeposit = async () => {
    try {
      await api.post(`/accounts/${accountNumber}/credit`, {
        amount: parseFloat(amount),
      });

      await api.post("/notify", {
        account_number: accountNumber,
        type: "deposit",
        amount: parseFloat(amount),
      });

      alert(`Depósito de R$ ${parseFloat(amount).toFixed(2)} realizado com sucesso!`);

      setAmount("");
      onSuccess();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Erro ao realizar depósito.");
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl mb-2">Realizar Depósito</h2>
      <input
        type="number"
        step="0.01"
        className="border p-2 rounded mr-2"
        placeholder="Valor do depósito"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button
        className="bg-green-500 text-white px-4 py-2 rounded"
        onClick={handleDeposit}
      >
        Depositar
      </button>
    </div>
  );
}
