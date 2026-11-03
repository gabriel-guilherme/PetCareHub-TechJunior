import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function LogoIcon() {
  return (
    <svg
      viewBox="32 13 34 34"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-7 h-7 shrink-0"
      aria-hidden="true"
    >
      <path
        d="M37.3141 18.3142L43.6882 22.5639H54.3116L60.6857 18.3142V37.4379C60.6857 40.9793 56.7904 42.75 48.9999 42.75C41.2094 42.75 37.3141 40.9793 37.3141 37.4379V18.3142Z"
        stroke="#FFFFFF"
        strokeWidth="2.65625"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function NavBar() {
  let pathname = '';
  try {
    const location = useLocation();
    pathname = location.pathname;
  } catch {
    pathname = '/';
  }

  const isAuthPage = pathname === '/login' || pathname === '/cadastro';

  return (
    <header className="bg-primaria sticky top-0 z-50 w-full">
      <div className="w-full max-w-[1440px] mx-auto px-6 sm:px-8 h-[60px] flex items-center justify-between">
        
        {/* LADO ESQUERDO: Logo PetCareHub */}
        <Link to="/pets" className="flex items-center gap-2 cursor-pointer select-none">
          <LogoIcon />
          <span className="text-xl font-bold tracking-tight text-superficie">
            PetCareHub
          </span>
        </Link>

        {/* LADO DIREITO */}
        {isAuthPage ? (
          <div className="flex items-center gap-4 sm:gap-5">
            <Link
              to="/servicos"
              className="text-superficie hover:text-clara text-sm font-medium transition-colors whitespace-nowrap"
            >
              Serviços
            </Link>

            <Link
              to="/login"
              className="py-2 px-6 rounded-campos_e_botoes bg-superficie/18 hover:bg-superficie/28 text-superficie text-sm font-semibold transition-colors flex items-center justify-center whitespace-nowrap"
            >
              Entrar
            </Link>

            <Link
              to="/cadastro"
              className="py-2 px-6 rounded-campos_e_botoes border border-superficie hover:bg-superficie/10 text-superficie text-sm font-medium transition-colors flex items-center justify-center whitespace-nowrap"
            >
              Cadastrar
            </Link>
          </div>
        ) : (
          <div className="flex items-center gap-3 sm:gap-5">
            <Link
              to="/agendamentos"
              className={`text-sm font-medium transition-colors whitespace-nowrap ${
                pathname === '/agendamentos'
                  ? 'bg-primariaEscura text-superficie px-3.5 py-1.5 rounded-campos_e_botoes font-semibold'
                  : 'text-superficie/90 hover:text-superficie'
              }`}
            >
              Meus Agendamentos
            </Link>

            <Link
              to="/pets"
              className={`text-sm font-medium transition-colors whitespace-nowrap ${
                pathname === '/pets'
                  ? 'bg-primariaEscura text-superficie px-3.5 py-1.5 rounded-campos_e_botoes font-semibold'
                  : 'text-superficie/90 hover:text-superficie'
              }`}
            >
              Meus Pets
            </Link>

            <Link
              to="/servicos"
              className={`text-sm font-medium transition-colors whitespace-nowrap ${
                pathname === '/servicos'
                  ? 'bg-primariaEscura text-superficie px-3.5 py-1.5 rounded-campos_e_botoes font-semibold'
                  : 'text-superficie/90 hover:text-superficie'
              }`}
            >
              Serviços
            </Link>

            <Link
              to="/login"
              className="py-1.5 px-4 rounded-campos_e_botoes border border-superficie hover:bg-superficie/10 text-superficie text-sm font-medium transition-colors flex items-center justify-center whitespace-nowrap ml-2"
            >
              Sair
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}

export default NavBar;