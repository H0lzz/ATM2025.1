import { useEffect, useState } from "react";
import api from "../api/api";

export default function DispenserSettings() {
  const [denomination, setDenomination] = useState(null);

  const fetchStrategy = async () => {
    try {
      const res = await api.get("/dispenser/strategy");
      setDenomination(res.data.current_strategy);
    } catch (err) {
      alert("Erro ao buscar estratégia do dispenser");
    }
  };

  const updateStrategy = async (value) => {
  try {
    await api.post("/dispenser/set-strategy", value, {
      headers: { "Content-Type": "application/json" }
    });
    setDenomination(value);
    alert(`Estratégia atualizada para R$ ${value}`);
  } catch (err) {
    alert(err.response?.data?.detail || JSON.stringify(err) || "Erro ao atualizar estratégia");
  }
};

  useEffect(() => {
    fetchStrategy();
  }, []);

  return (
    <div className="mt-6">
      <h2 className="text-xl mb-2">Estratégia do Dispenser</h2>
      <p>Atual: R$ {denomination}</p>
      <button
        onClick={() => updateStrategy(20)}
        className="bg-blue-500 text-white px-4 py-1 mr-2 rounded"
      >
        Usar R$20
      </button>
      <button
        onClick={() => updateStrategy(100)}
        className="bg-green-500 text-white px-4 py-1 rounded"
      >
        Usar R$100
      </button>
    </div>
  );
}
