import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { NavBar } from '../components/NavBar';
import { PetCard } from '../components/PetCard';
import type { Pet } from '../components/PetCard';
import { PetModal } from '../components/PetModal';

export function Pets() {
  const navigate = useNavigate();
  const [pets, setPets] = useState<Pet[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [petEmEdicao, setPetEmEdicao] = useState<Pet | null>(null);

  // 1. Carrega os pets do usuário logado assim que a tela abre
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }
    carregarPets(token);
  }, []);

  const carregarPets = async (tokenParam?: string) => {
    const token = tokenParam || localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      setCarregando(true);
      setErro(null);

      // Swagger oficial: GET /api/pets/ (com a barra no final)
      const response = await fetch('/api/pets/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Se o token expirou ou for inválido
      if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('token');
        navigate('/');
        return;
      }

      if (!response.ok) {
        throw new Error('Não foi possível carregar os pets.');
      }

      const dados = await response.json();
      
      const petsNormalizados: Pet[] = dados.map((p: any) => ({
        ...p,
        id: String(p.id),
        idade: Number(p.idade ?? 0),
      }));

      setPets(petsNormalizados);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErro(err.message);
      } else {
        setErro('Erro ao buscar pets.');
      }
    } finally {
      setCarregando(false);
    }
  };

  const handleAbrirNovoPet = () => {
    setPetEmEdicao(null);
    setIsModalOpen(true);
  };

  const handleAbrirEditar = (pet: Pet) => {
    setPetEmEdicao(pet);
    setIsModalOpen(true);
  };

  // 2. Exclusão no banco de dados (Swagger: DELETE /api/pets/{id})
  const handleExcluir = async (id: string) => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    const confirmar = window.confirm('Deseja realmente remover este pet?');
    if (!confirmar) return;

    try {
      const response = await fetch(`/api/pets/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Falha ao excluir o pet no servidor.');
      }

      setPets((prev) => prev.filter((p) => p.id !== id));
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert(err.message);
      } else {
        alert('Erro ao excluir pet.');
      }
    }
  };

  // 3. Salvar (Criar ou Editar) no banco de dados
  const handleSalvarPet = async (dados: Omit<Pet, 'id'>, idParaEditar?: string) => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      // POST com barra no final (/api/pets/), PUT sem barra (/api/pets/{id})
      const url = idParaEditar ? `/api/pets/${idParaEditar}` : '/api/pets/';
      const metodo = idParaEditar ? 'PUT' : 'POST';

      // Swagger exige dataNascimento (YYYY-MM-DD). Calculamos a partir da idade informada:
      const anos = Number(dados.idade) || 0;
      const dataCalculada = new Date();
      dataCalculada.setFullYear(dataCalculada.getFullYear() - anos);
      const dataNascimento = dataCalculada.toISOString().split('T')[0];

      const response = await fetch(url, {
        method: metodo,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          nome: dados.nome.trim(),
          especie: dados.especie,
          raca: dados.raca?.trim() || '',
          dataNascimento,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const detalhe = errorData.message || errorData.error || `Erro HTTP ${response.status}`;
        throw new Error(detalhe);
      }

      // Recarrega a lista sincronizando com o banco
      await carregarPets(token);
      setIsModalOpen(false);
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert(`Erro ao salvar: ${err.message}`);
      } else {
        alert('Erro ao salvar pet.');
      }
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col bg-fundo text-slate-800">
      <NavBar />

      {/* Faixa do Cabeçalho */}
      <div className="w-full bg-clara/25 border-b border-borda py-8">
        <div className="max-w-[1440px] mx-auto px-6 sm:px-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
                Meus Pets
              </h1>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-clara text-primariaEscura">
                {pets.length} {pets.length === 1 ? 'cadastrado' : 'cadastrados'}
              </span>
            </div>
            <p className="text-sm text-textoSuave">
              Gerencie os pets cadastrados na sua conta.
            </p>
          </div>

          <button
            type="button"
            onClick={handleAbrirNovoPet}
            className="self-start sm:self-auto py-2.5 px-5 bg-acao hover:bg-[#14532d] text-superficie text-sm font-semibold rounded-campos_e_botoes transition-colors shadow-xs cursor-pointer flex items-center gap-2"
          >
            <span className="text-base font-bold leading-none">+</span>
            <span>Cadastrar pet</span>
          </button>
        </div>
      </div>

      {/* Grid Principal */}
      <main className="flex-1 w-full max-w-[1440px] mx-auto px-6 sm:px-10 py-10">
        {erro && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
            {erro}
          </div>
        )}

        {carregando ? (
          <div className="flex items-center justify-center py-20 text-textoSuave text-sm">
            Carregando seus pets do banco de dados...
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Cards reais do banco de dados */}
            {pets.map((pet) => (
              <PetCard
                key={pet.id}
                pet={pet}
                onEditar={handleAbrirEditar}
                onExcluir={handleExcluir}
              />
            ))}

            {/* Card tracejado para adicionar novo pet */}
            <button
              type="button"
              onClick={handleAbrirNovoPet}
              className="bg-clara/15 hover:bg-clara/30 rounded-cartoes_e_pilulas border-2 border-dashed border-primaria/40 p-6 flex flex-col items-center justify-center min-h-[220px] transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-clara flex items-center justify-center text-primaria text-2xl font-light mb-3 group-hover:scale-110 transition-transform">
                +
              </div>
              <span className="text-sm font-bold text-primaria tracking-tight">
                Cadastrar novo pet
              </span>
            </button>
          </div>
        )}
      </main>

      {/* Modal de cadastro/edição */}
      <PetModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSalvar={handleSalvarPet}
        petParaEditar={petEmEdicao}
      />
    </div>
  );
}

export default Pets;