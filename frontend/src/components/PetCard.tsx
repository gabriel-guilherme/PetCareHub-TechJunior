import { PawIcon } from './PawIcon';

export interface Pet {
    id: string;
    nome: string;
    especie: 'cão' | 'gato' | 'outro';
    raca?: string;
    idade: number; //0 a 40 anos (RN04) Talvez seja interessante mudar para permitir pets com maior tempo de vida
}

export interface PetCardProps {
  pet: Pet;
  onEditar?: (pet: Pet) => void;
  onExcluir?: (id: string) => void;
}

export function PetCard({ pet, onEditar, onExcluir }: PetCardProps) {
  // Badges visuais sutis para cada espécie
  const badgeEspecie = {
    cão: { label: 'Cão 🐶', bg: 'bg-emerald-50 text-emerald-800 border-emerald-200' },
    gato: { label: 'Gato 🐱', bg: 'bg-teal-50 text-teal-800 border-teal-200' },
    outro: { label: 'Outro 🐾', bg: 'bg-slate-100 text-slate-800 border-slate-200' },
  }[pet.especie] || { label: pet.especie, bg: 'bg-slate-100 text-slate-800 border-slate-200' };

  return (
    <article className="bg-superficie rounded-cartoes_e_pilulas border border-borda p-6 shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between">
      <div>
        {/* Cabeçalho do Card: Círculo com a Patinha e Badge */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="w-12 h-12 rounded-full bg-clara/50 flex items-center justify-center text-primaria">
            <PawIcon size={24} className="text-primaria" />
          </div>
          <span
            className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${badgeEspecie.bg}`}
          >
            {badgeEspecie.label}
          </span>
        </div>

        {/* Informações Principais */}
        <h3 className="text-xl font-bold text-slate-800 mb-1 tracking-tight">
          {pet.nome}
        </h3>

        <div className="text-sm text-textoSuave flex flex-col gap-1 mb-6">
          <p>
            <span className="font-medium text-slate-600">Raça:</span>{' '}
            {pet.raca && pet.raca.trim() !== '' ? pet.raca : 'Não informada'}
          </p>
          <p>
            <span className="font-medium text-slate-600">Idade:</span>{' '}
            {pet.idade === 0
              ? 'Menos de 1 ano (filhote)'
              : pet.idade === 1
              ? '1 ano'
              : `${pet.idade} anos`}
          </p>
        </div>
      </div>

      {/* Botões de Ação (RF06 Editar / RF07 Excluir) */}
      <div className="pt-4 border-t border-borda flex items-center gap-3">
        {/* Botão Editar */}
        <button
          type="button"
          onClick={() => onEditar?.(pet)}
          className="min-w-[80px] px-5 py-2 rounded-campos_e_botoes border border-borda text-slate-700 hover:bg-slate-50 text-sm font-semibold transition-colors cursor-pointer text-center"
        >
          Editar
        </button>

        {/* Botão Excluir */}
        <button
          type="button"
          onClick={() => onExcluir?.(pet.id)}
          className="min-w-[80px] px-5 py-2 rounded-campos_e_botoes border border-red-500 text-red-600 hover:bg-red-50 text-sm font-semibold transition-colors cursor-pointer text-center"
        >
          Excluir
        </button>
      </div>
    </article>
  );
}

export default PetCard;