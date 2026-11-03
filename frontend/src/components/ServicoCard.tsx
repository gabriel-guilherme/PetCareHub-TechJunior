import React from 'react';

export interface Servico {
  id: string;
  nome: string;
  descricao: string;
  duracaoMinutos: number;
  preco: number;
  tipoIcone?: 'droplet' | 'scissors' | 'cross' | 'syringe' | 'home';
}

export interface ServicoCardProps {
  servico: Servico;
  onAgendar: (servico: Servico) => void;
}

// Ícones vetoriais fiéis ao design do Figma
function ServiceIcon({ tipo }: { tipo?: string }) {
  switch (tipo) {
    case 'droplet': // Banho
      return (
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5 text-primaria"
          aria-hidden="true"
        >
          <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
        </svg>
      );
    case 'scissors': // Tosa
      return (
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5 text-primaria"
          aria-hidden="true"
        >
          <circle cx="6" cy="6" r="3" />
          <circle cx="6" cy="18" r="3" />
          <line x1="20" y1="4" x2="8.12" y2="15.88" />
          <line x1="14.47" y1="14.48" x2="20" y2="20" />
          <line x1="8.12" y1="8.12" x2="12" y2="12" />
        </svg>
      );
    case 'cross': // Consulta veterinária
      return (
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5 text-primaria"
          aria-hidden="true"
        >
          <path d="M12 5v14M5 12h14" />
        </svg>
      );
    case 'syringe': // Vacinação
      return (
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5 text-primaria"
          aria-hidden="true"
        >
          <path d="m18 2 4 4" />
          <path d="m17 7 3-3" />
          <path d="M19 9 8.7 19.3c-.4.4-1 .6-1.7.6H3v-4c0-.7.2-1.3.6-1.7L14 3.9" />
          <path d="m9 11 4 4" />
          <path d="m5 19-3 3" />
          <path d="m14 4 6 6" />
        </svg>
      );
    case 'home': // Hospedagem diurna
    default:
      return (
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5 text-primaria"
          aria-hidden="true"
        >
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          <polyline points="9 22 9 12 15 12 15 22" />
        </svg>
      );
  }
}

export function ServicoCard({ servico, onAgendar }: ServicoCardProps) {
  // Formatação em Reais (R$)
  const precoFormatado = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(servico.preco);

  // Formatação de duração (ex: 45 min, 60 min, etc)
  const duracaoFormatada =
    servico.duracaoMinutos >= 60 && servico.duracaoMinutos % 60 === 0
      ? `${servico.duracaoMinutos / 60}h`
      : `${servico.duracaoMinutos} min`;

  return (
    <div className="bg-superficie rounded-cartoes_e_pilulas border border-borda p-6 shadow-xs flex flex-col justify-between hover:border-slate-300 transition-all">
      <div>
        {/* Ícone no quadradinho verde menta */}
        <div className="w-10 h-10 rounded-xl bg-clara flex items-center justify-center mb-4">
          <ServiceIcon tipo={servico.tipoIcone} />
        </div>

        {/* Título do Serviço */}
        <h3 className="text-base font-bold text-slate-900 mb-1">
          {servico.nome}
        </h3>

        {/* Descrição curta e direta conforme o Figma */}
        <p className="text-xs text-slate-500 leading-relaxed mb-6">
          {servico.descricao}
        </p>
      </div>

      <div>
        {/* Linha com Duração e Preço */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-3.5 h-3.5 text-slate-400"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            <span>{duracaoFormatada}</span>
          </div>

          <span className="text-base font-bold text-slate-900">
            {precoFormatado}
          </span>
        </div>

        {/* Botão Agendar ocupando largura total */}
        <button
          type="button"
          onClick={() => onAgendar(servico)}
          className="w-full py-2.5 bg-acao hover:bg-[#14532d] text-superficie text-sm font-semibold rounded-campos_e_botoes transition-colors shadow-xs cursor-pointer text-center"
        >
          Agendar
        </button>
      </div>
    </div>
  );
}

export default ServicoCard;