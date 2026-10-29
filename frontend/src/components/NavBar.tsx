import React from 'react';
import { Link } from 'react-router-dom';

function LogoIcon(){
    return(
        <svg viewBox="32 13 34 34" 
            fill = "none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-7 h-7 shrink-0"
            >
                <path 
                    d="M37.3141 18.3142L43.6882 22.5639H54.3116L60.6857 18.3142V37.4379C60.6857 40.9793 56.7904 42.75 48.9999 42.75C41.2094 42.75 37.3141 40.9793 37.3141 37.4379V18.3142Z"
                    stroke="white"
                    strokeWidth="2.65625"
                    strokeLinejoin="round"
                />
        </svg>
    );
}


export function NavBar () {
    return (
         <>
             <header className="bg-primaria text-superficie sticky top-0 z-50 w-full">
                <div className="w-full max-w-[1440px] mx-auto px-10 h-[60px] flex items-center justify-between">
                    {/* Lado Esquerdo: Logo PetCareHub */}
                    <div className="flex items-center gap-3.5 cursor-pointer">
                        <LogoIcon />
                        <span className="text-xl font-bold tracking-tight text-superficie">
                            PetCareHub
                        </span>
                    </div>

                    {/* Lado Direito: Link e Botões */}
                    <div className="flex items-center gap-6">
                        <a href="#serviços"
                        className="text-superficie hover:text-clara text-sm font-medium transition-colors whitespace-nowrap">
                            Serviços
                        </a>
                        {/* Botão Entrar */}
                        <Link 
                            to="/"
                            className="py-2.5 px-3 rounded-campos_e_botoes bg-superficie/18 hover:bg-superficie/28 text-sm font-semibold transition-colors flex items-center justify-center whitespace-nowrap cursor-pointer">
                            Entrar
                        </Link>
                        {/*Botão cadastrar*/}
                        <Link
                            to="/cadastro"
                            className="py-2.5 px-3 rounded-campos_e_botoes border border-superficie hover:bg-superficie/10 text-superficie text-sm font-medium transition-colors flex items-center justify-center whitespace-nowrap cursor-pointer">
                            Cadastrar
                        </Link>
                    </div>
                </div>
             </header>
             
         </>
    );
}