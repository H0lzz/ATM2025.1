import { useNavigate } from "react-router-dom";

export default function AdminMenu() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4 bg-gray-100">
      <h1 className="text-3xl font-bold">Menu do Administrador</h1>

      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={() => alert("Função ainda não implementada")}
      >
        Gerenciar Contas
      </button>

      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={() => alert("Função ainda não implementada")}
      >
        Ver Transações
      </button>

      <button
        className="text-red-500 underline"
        onClick={() => navigate("/")}
      >
        Sair
      </button>
    </div>
  );
}
