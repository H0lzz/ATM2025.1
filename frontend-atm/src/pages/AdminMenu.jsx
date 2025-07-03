import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

export default function AdminMenu() {
  const [accountNumber, setAccountNumber] = useState("");
  const [accountInfo, setAccountInfo] = useState(null);
  const [message, setMessage] = useState("");

  const [newAccount, setNewAccount] = useState({
    account_number: "",
    pin: "",
    available_balance: "",
    total_balance: "",
    is_admin: false,
  });

  const [updateAccount, setUpdateAccount] = useState({
    pin: "",
    available_balance: "",
    total_balance: "",
    is_admin: false,
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  const handleGetAccount = async () => {
    try {
      const res = await api.get(`/accounts/${accountNumber}`);
      setAccountInfo(res.data);
      setMessage("");
    } catch (err) {
      setAccountInfo(null);
      setMessage("Conta não encontrada.");
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await api.delete(`/accounts/${accountNumber}`);
      setAccountInfo(null);
      setMessage("Conta deletada com sucesso.");
    } catch (err) {
      setMessage("Erro ao deletar conta.");
    }
  };

  const handleCreateAccount = async () => {
    try {
      await api.post("/accounts", {
        account_number: parseInt(newAccount.account_number),
        pin: parseInt(newAccount.pin),
        available_balance: parseFloat(newAccount.available_balance),
        total_balance: parseFloat(newAccount.total_balance),
        is_admin: newAccount.is_admin,
      });
      setMessage("Conta criada com sucesso.");
      setNewAccount({
        account_number: "",
        pin: "",
        available_balance: "",
        total_balance: "",
        is_admin: false,
      });
    } catch (err) {
      console.error(err);
      setMessage("Erro ao criar conta.");
    }
  };

  const handleUpdateAccount = async () => {
    try {
      await api.put(`/accounts/${accountNumber}`, {
        pin: updateAccount.pin ? parseInt(updateAccount.pin) : undefined,
        available_balance: updateAccount.available_balance
          ? parseFloat(updateAccount.available_balance)
          : undefined,
        total_balance: updateAccount.total_balance
          ? parseFloat(updateAccount.total_balance)
          : undefined,
        is_admin: updateAccount.is_admin,
      });
      setMessage("Conta atualizada com sucesso.");
      setUpdateAccount({
        pin: "",
        available_balance: "",
        total_balance: "",
        is_admin: false,
      });
    } catch (err) {
      console.error(err);
      setMessage("Erro ao atualizar conta.");
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">🔐 Menu do Administrador</h1>

      {/* Seção: Buscar e Deletar */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Buscar / Deletar Conta</h2>
        <input
          className="border p-2 rounded mr-2 mb-2"
          placeholder="Número da conta"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
        />
        <div className="mb-2">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
            onClick={handleGetAccount}
          >
            Buscar Conta
          </button>
          <button
            className="bg-red-500 text-white px-4 py-2 rounded mr-2"
            onClick={handleDeleteAccount}
          >
            Deletar Conta
          </button>
        </div>
        {accountInfo && (
          <div className="mt-2 text-sm">
            <p><strong>Conta:</strong> {accountInfo.account_number}</p>
            <p><strong>Saldo Total:</strong> R$ {accountInfo.total_balance}</p>
            <p><strong>Saldo Disponível:</strong> R$ {accountInfo.available_balance}</p>
            <p><strong>Administrador:</strong> {accountInfo.is_admin ? "Sim" : "Não"}</p>
          </div>
        )}
      </div>

      {/* Seção: Criar Conta */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Criar Nova Conta</h2>
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Número da conta"
          value={newAccount.account_number}
          onChange={(e) =>
            setNewAccount({ ...newAccount, account_number: e.target.value })
          }
        />
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="PIN"
          value={newAccount.pin}
          onChange={(e) => setNewAccount({ ...newAccount, pin: e.target.value })}
        />
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Saldo disponível"
          value={newAccount.available_balance}
          onChange={(e) =>
            setNewAccount({ ...newAccount, available_balance: e.target.value })
          }
        />
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Saldo total"
          value={newAccount.total_balance}
          onChange={(e) =>
            setNewAccount({ ...newAccount, total_balance: e.target.value })
          }
        />
        <label className="block mb-2">
          <input
            type="checkbox"
            checked={newAccount.is_admin}
            onChange={(e) =>
              setNewAccount({ ...newAccount, is_admin: e.target.checked })
            }
          />{" "}
          Conta Administrativa
        </label>
        <button
          className="bg-green-600 text-white px-4 py-2 rounded"
          onClick={handleCreateAccount}
        >
          Criar Conta
        </button>
      </div>

      {/* Seção: Atualizar Conta */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Atualizar Conta</h2>
        <p className="text-sm mb-2 text-gray-600">
          Informe os novos valores (deixe campos em branco se não quiser atualizar).
        </p>
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Novo PIN"
          value={updateAccount.pin}
          onChange={(e) =>
            setUpdateAccount({ ...updateAccount, pin: e.target.value })
          }
        />
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Novo saldo disponível"
          value={updateAccount.available_balance}
          onChange={(e) =>
            setUpdateAccount({ ...updateAccount, available_balance: e.target.value })
          }
        />
        <input
          className="border p-2 mr-2 mb-2"
          placeholder="Novo saldo total"
          value={updateAccount.total_balance}
          onChange={(e) =>
            setUpdateAccount({ ...updateAccount, total_balance: e.target.value })
          }
        />
        <label className="block mb-2">
          <input
            type="checkbox"
            checked={updateAccount.is_admin}
            onChange={(e) =>
              setUpdateAccount({ ...updateAccount, is_admin: e.target.checked })
            }
          />{" "}
          Conta Administrativa
        </label>
        <button
          className="bg-yellow-500 text-white px-4 py-2 rounded"
          onClick={handleUpdateAccount}
        >
          Atualizar Conta
        </button>
      </div>

      {/* Mensagens e Sair */}
      {message && <p className="text-red-600 mb-4">{message}</p>}
      <button
        className="bg-gray-500 text-white px-4 py-2 rounded"
        onClick={handleLogout}
      >
        Sair
      </button>
    </div>
  );
}
