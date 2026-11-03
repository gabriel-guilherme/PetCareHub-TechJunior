import React, { useState, useEffect } from 'react';
import type { Pet } from './PetCard';

export interface PetModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSalvar: (dados: Omit<Pet, 'id'>, idParaEditar?: string) => void;
  petParaEditar?: Pet | null;
}

export function PetModal({
  isOpen,
  onClose,
  onSalvar,
  petParaEditar,
}: PetModalProps) {
  const [nome, setNome] = useState('');
  const [especie, setEspecie] = useState<'cão' | 'gato' | 'outro'>('cão');
  const [raca, setRaca] = useState('');
  const [idade, setIdade] = useState<number | ''>(1);
  const [erro, setErro] = useState<string | null>(null);

  // Preenche os campos se estiver no modo de edição ou limpa se for novo pet
  useEffect(() => {
    if (petParaEditar) {
      setNome(petParaEditar.nome);
      setEspecie(petParaEditar.especie);
      setRaca(petParaEditar.raca || '');
      setIdade(petParaEditar.idade);
    } else {
      setNome('');
      setEspecie('cão');
      setRaca('');
      setIdade(1);
    }
    setErro(null);
  }, [petParaEditar, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!nome.trim()) {
      setErro('Informe o nome do pet.');
      return;
    }

    if (idade === '' || idade < 0 || idade > 40) {
      setErro('A idade deve estar entre 0 e 40 anos (Regra RN04).');
      return;
    }

    onSalvar(
      {
        nome: nome.trim(),
        especie,
        raca: raca.trim() || undefined,
        idade: Number(idade),
      },
      petParaEditar?.id
    );

    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
      <div className="w-full max-w-md bg-superficie rounded-cartoes_e_pilulas border border-borda p-6 sm:p-8 shadow-xl">
        
        {/* Cabeçalho do Modal */}
        <div className="flex items-center justify-between pb-4 border-b border-borda mb-6">
          <h2 className="text-xl font-bold text-slate-800">
            {petParaEditar ? 'Editar Pet' : 'Cadastrar Novo Pet'}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="text-textoSuave hover:text-slate-800 text-lg w-8 h-8 rounded-full flex items-center justify-center hover:bg-slate-100 transition-colors cursor-pointer"
          >
            ✕
          </button>
        </div>

        {/* Mensagem de Erro (se houver) */}
        {erro && (
          <div className="mb-4 p-3 rounded-campos_e_botoes bg-red-50 border border-red-200 text-erro text-sm">
            {erro}
          </div>
        )}

        {/* Formulário */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {/* Nome */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-slate-700">
              Nome do Pet *
            </label>
            <input
              type="text"
              required
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              placeholder="Ex: Pipoca, Thor, Mia..."
              className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-textoSuave/50 focus:outline-none focus:ring-2 focus:ring-foco_borda text-sm"
            />
          </div>

          {/* Espécie */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-slate-700">
              Espécie *
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['cão', 'gato', 'outro'] as const).map((esp) => (
                <button
                  key={esp}
                  type="button"
                  onClick={() => setEspecie(esp)}
                  className={`py-2 px-3 text-sm font-medium rounded-campos_e_botoes border capitalize transition-colors cursor-pointer ${
                    especie === esp
                      ? 'bg-primaria text-superficie border-primaria font-semibold'
                      : 'bg-superficie text-slate-700 border-borda hover:bg-slate-50'
                  }`}
                >
                  {esp === 'cão' ? '🐶 Cão' : esp === 'gato' ? '🐱 Gato' : '🐾 Outro'}
                </button>
              ))}
            </div>
          </div>

          {/* Raça (Opcional) */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-slate-700">
              Raça <span className="text-textoSuave text-xs font-normal">(opcional)</span>
            </label>
            <input
              type="text"
              value={raca}
              onChange={(e) => setRaca(e.target.value)}
              placeholder="Ex: Golden Retriever, SRD, Poodle..."
              className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-textoSuave/50 focus:outline-none focus:ring-2 focus:ring-foco_borda text-sm"
            />
          </div>

          {/* Idade em anos (RN04: 0 a 40) */}
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-slate-700">
              Idade em anos * <span className="text-textoSuave text-xs font-normal">(0 a 40)</span>
            </label>
            <input
              type="number"
              min={0}
              max={40}
              required
              value={idade}
              onChange={(e) => setIdade(e.target.value === '' ? '' : Number(e.target.value))}
              placeholder="Ex: 3"
              className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-textoSuave/50 focus:outline-none focus:ring-2 focus:ring-foco_borda text-sm"
            />
          </div>

          {/* Botões do Rodapé */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-borda mt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-campos_e_botoes border border-borda text-slate-700 hover:bg-slate-50 text-sm font-medium transition-colors cursor-pointer"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-5 py-2.5 rounded-campos_e_botoes bg-acao hover:bg-[#14532d] text-superficie text-sm font-semibold transition-colors cursor-pointer shadow-xs"
            >
              {petParaEditar ? 'Salvar Alterações' : 'Cadastrar Pet'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}

export default PetModal;