import React from 'react';
import { useNavigate } from 'react-router-dom';
import { NavBar } from '../components/NavBar'; 
import { ServicoCard, type Servico } from '../components/ServicoCard';

// 5 serviços oficiais da clínica descritos no Edital e fidedignos ao Figma
export const SERVICOS_OFICIAIS: Servico[] = [
  {
    id: '1',
    nome: 'Banho',
    descricao: 'Banho completo com secagem.',
    duracaoMinutos: 45,
    preco: 60.0,
    tipoIcone: 'droplet',
  },
  {
    id: '2',
    nome: 'Tosa',
    descricao: 'Tosa higiênica ou na máquina.',
    duracaoMinutos: 60,
    preco: 80.0,
    tipoIcone: 'scissors',
  },
  {
    id: '3',
    nome: 'Consulta veterinária',
    descricao: 'Avaliação geral de saúde.',
    duracaoMinutos: 30,
    preco: 150.0,
    tipoIcone: 'cross',
  },
  {
    id: '4',
    nome: 'Vacinação',
    descricao: 'Vacinas conforme a idade do pet.',
    duracaoMinutos: 20,
    preco: 90.0,
    tipoIcone: 'syringe',
  },
  {
    id: '5',
    nome: 'Hospedagem diurna',
    descricao: 'Cuidado e diversão durante o dia.',
    duracaoMinutos: 480, // Daycare diurno
    preco: 120.0,
    tipoIcone: 'home',
  },
];

export function Servicos() {
  const navigate = useNavigate();

  // Ao clicar em agendar, direciona para o fluxo adequado
  const handleAgendar = (servico: Servico) => {
    navigate('/login', { state: { servicoEscolhido: servico } });
  };

  // Ao clicar para falar com o assistente (Card 6)
  const handleFalarComAssistente = () => {
    const chatWidget = document.getElementById('chat-widget-trigger');
    if (chatWidget) {
      chatWidget.click();
    } else {
      alert('O assistente virtual está pronto para te ajudar com dúvidas e horários!');
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col bg-fundo text-slate-800">
      {/* Barra de Navegação */}
      <NavBar />

      {/* Banner Superior com fundo verde menta suave (Idêntico ao Figma) */}
      <div className="w-full bg-[#E6F4F1] border-b border-borda py-8 px-6 sm:px-10">
        <div className="max-w-[1440px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-1">
              Serviços
            </h1>
            <p className="text-sm text-textoSuave">
              Escolha um serviço e agende em poucos cliques.
            </p>
          </div>

          {/* Horário de Funcionamento */}
          <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-superficie border border-borda text-xs text-slate-700 shadow-2xs self-start sm:self-auto">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-3.5 h-3.5 text-slate-500"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            <span className="font-medium">Seg a sáb · 08h–18h</span>
          </div>
        </div>
      </div>

      {/* Conteúdo Principal: Grade 3x2 com os Serviços + Card do Assistente */}
      <main className="flex-1 w-full max-w-[1440px] mx-auto px-6 sm:px-10 py-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* 5 Cards de Serviços Oficiais */}
          {SERVICOS_OFICIAIS.map((servico) => (
            <ServicoCard
              key={servico.id}
              servico={servico}
              onAgendar={handleAgendar}
            />
          ))}

          {/* 6º Card Especial: Assistente Virtual (RF14 a RF18) */}
          <div className="bg-primaria rounded-cartoes_e_pilulas p-6 flex flex-col justify-between text-superficie shadow-xs">
            <div>
              <h3 className="text-xl font-bold text-superficie mb-2 leading-tight">
                Não sabe qual escolher?
              </h3>
              <p className="text-sm text-clara/90 leading-relaxed">
                Converse com o assistente e tire dúvidas sobre serviços, preços e horários.
              </p>
            </div>

            <button
              type="button"
              onClick={handleFalarComAssistente}
              className="w-full py-2.5 bg-superficie hover:bg-slate-50 text-primariaEscura font-bold text-sm rounded-campos_e_botoes transition-colors shadow-xs cursor-pointer text-center mt-6"
            >
              Falar com o assistente
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Servicos;