import { useState } from "react";
import api from "../api/api";

export default function WithdrawForm({ accountNumber, onSuccess }) {
  const [amount, setAmount] = useState("");

  const handleWithdraw = async () => {
    try {
      const response = await api.post(`/accounts/${accountNumber}/debit`, {
        amount: parseFloat(amount),
      });

      await api.post("/notify", {
        account_number: accountNumber,
        type: "withdraw",
        amount: parseFloat(amount),
      });

      alert(`Saque de R$ ${parseFloat(amount).toFixed(2)} realizado com sucesso!`);

      setAmount("");
      onSuccess();
    } catch (err) {
      console.error(err);
      alert("Erro ao realizar saque.");
    }
  };

  return (
    <div className="flex flex-col gap-2 mt-4">
      <h2 className="text-xl mb-2">Realizar Saque</h2>
      <input
        type="number"
        placeholder="Valor do saque"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        className="border p-2 rounded"
      />
      <button
        onClick={handleWithdraw}
        className="bg-red-500 text-white px-4 py-2 rounded"
      >
        Sacar
      </button>
    </div>
  );
}
