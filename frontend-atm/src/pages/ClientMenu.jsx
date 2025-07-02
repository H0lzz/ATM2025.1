import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import WithdrawForm from "../components/WithdrawForm";
import DepositForm from "../components/DepositForm";
import DispenserSettings from "./DispenserSettings";
import api from "../api/api";

export default function ClientMenu() {
  const location = useLocation();
  const navigate = useNavigate();

  const accountNumber = location.state?.accountNumber;

  const [balance, setBalance] = useState(null);

  const fetchBalance = async () => {
    try {
      const response = await api.get(`/accounts/${accountNumber}/balance`);
      const { total_balance, available_balance } = response.data;
      setBalance({ total: total_balance, available: available_balance });
    } catch (err) {
      console.error(err);
      alert("Erro ao buscar saldo.");
    }
  };

  useEffect(() => {
    if (!accountNumber) {
      alert("Número da conta não encontrado. Redirecionando...");
      navigate("/");
    } else {
      fetchBalance();
    }
  }, [accountNumber]);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">🏧 Menu do Cliente</h1>
      {balance ? (
        <>
          <p className="text-lg">💰 Saldo total: R$ {balance.total.toFixed(2)}</p>
          <p className="text-lg mb-6">💳 Saldo disponível: R$ {balance.available.toFixed(2)}</p>
          <DepositForm accountNumber={accountNumber} onSuccess={fetchBalance} />
          <WithdrawForm accountNumber={accountNumber} onSuccess={fetchBalance} />
          <DispenserSettings />
        </>
      ) : (
        <p>Carregando saldo...</p>
      )}
    </div>
  );
}
