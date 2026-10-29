import {NavBar} from '../components/NavBar';
import {PawIcon} from '../components/PawIcon';
import {CheckIcon} from '../components/CheckIcon';
import { Link } from 'react-router-dom';

const vantagens = [
    'Cadastro de pets',
    'Agendamento online',
    'Assistente virtual',
];

export function Login(){
    return (
        <>
            <div className="flex flex-col min-h-screen w-full">
                <NavBar />
                <div className="flex flex-1 w-full">
                    {/*lado esquerdo: verde*/}
                    <div className="w-1/2 bg-primaria flex flex-col justify-center px-12 lg:px-24 py-16 text-superficie">
                        <div className="max-w-md">
                            {/*icone da patinha */}
                            <PawIcon size={56} className="text-clara mb-8"/>
                            {/*titulo principal */}
                            <h1 className="text-4xl lg:text-5xl font-bold tracking-tight mb-5">
                                Bem-vindo de volta
                            </h1>
                            {/**subtitulo  */}
                            <p className="text-clara text-lg lg:text-xl font-normal mb-4">
                                Pets e agendamentos em um só lugar
                            </p>
                            {/*uma unica linha de <li> que se repete para todos os itens */}
                            <ul className="space-y-4">
                                {vantagens.map((texto) => (
                                    <li key={texto} className="flex items-center gap-3.5 text-base font-medium">
                                        <CheckIcon size={20} className="text-clara" />
                                        <span>{texto}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>                        
                    </div>
                    {/*lado direito */}
                    <div className="w-1/2 min-h-full bg-fundo flex items-center justify-center p-8 sm:p-12">
                        <div className="w-full max-w-[420px] bg-superficie rounded-cartoes_e_pilulas border border-borda p-8 sm:p-10 shadow-sm">
                            {/*cabecalho do cartao */}
                            <h2 className="text-2xl font-bold text-slate-800 mb-1">
                                Entrar
                            </h2>
                            <p className="text-sm text-textoSuave mb-8">
                                Informe suas credenciais para acessar sua conta.
                            </p>
                            {/* Formulário */}
                            <form className="flex flex-col gap-5">
                                {/* Campo E-mail */}
                                <div className="flex flex-col gap-1.5">
                                    <label className="text-sm font-medium text-slate-700">
                                    E-mail
                                    </label>
                                    <input
                                    type="email"
                                    placeholder="exemplo@email.com"
                                    className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-textoSuave/50 focus:outline-none focus:ring-2 focus:ring-foco_borda focus:border-transparent transition-all text-sm"
                                    />
                                </div>

                                {/* Campo Senha */}
                                <div className="flex flex-col gap-1.5">
                                    <label className="text-sm font-medium text-slate-700">
                                    Senha
                                    </label>
                                    <input
                                    type="password"
                                    placeholder="••••••••"
                                    className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-textoSuave/50 focus:outline-none focus:ring-2 focus:ring-foco_borda focus:border-transparent transition-all text-sm"
                                    />
                                </div>

                                {/* Botão Entrar */}
                                <button
                                    type="submit"
                                    className="w-full py-3 mt-2 bg-acao hover:bg-[#14532d] text-superficie text-sm font-semibold rounded-campos_e_botoes transition-colors shadow-xs cursor-pointer flex items-center justify-center"
                                >
                                    Entrar
                                </button>
                            </form>
                            {/* Link para Cadastro */}
                            <div className="mt-8 text-center text-sm text-textoSuave">
                                Não tem conta?{' '}
                                <Link 
                                    to="/cadastro" 
                                    className="text-primaria font-semibold hover:underline transition-colors">                                    
                                    Cadastre-se
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            
        </>
    )
}