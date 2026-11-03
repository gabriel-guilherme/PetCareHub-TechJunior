import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { NavBar } from '../components/NavBar';
import { PawIcon } from '../components/PawIcon';
import { CheckIcon } from '../components/CheckIcon';

const vantagens = [
  'Cadastro de pets',
  'Agendamento online',
  'Assistente virtual',
];

export function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro(null);
    setCarregando(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, senha }),
      });

      if (!response.ok) {
        let mensagemErro = 'E-mail ou senha incorretos.';
        try {
          const dadosErro = await response.json();
          if (dadosErro.message) mensagemErro = dadosErro.message;
          else if (dadosErro.error) mensagemErro = dadosErro.error;
        } catch {
          // Mantém mensagem padrão
        }
        throw new Error(mensagemErro);
      }

      const data = await response.json();

      // Salva o token retornado para o Pets.tsx conseguir ler
      const token = data.token || data.accessToken || data.jwt || (typeof data === 'string' ? data : null);
      if (token) {
        localStorage.setItem('token', token);
      }

      // Direciona para a tela de pets
      navigate('/pets');
    } catch (err: any) {
      setErro(err.message || 'Erro ao conectar com o servidor.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full font-sans bg-fundo text-slate-800">
      <NavBar />
      <div className="flex flex-1 w-full">
        {/* Lado esquerdo: verde */}
        <div className="w-1/2 bg-primaria flex flex-col justify-center px-12 lg:px-24 py-16 text-superficie">
          <div className="max-w-md">
            <PawIcon size={56} className="text-clara mb-8" />
            <h1 className="text-4xl lg:text-5xl font-bold tracking-tight mb-5">
              Bem-vindo de volta
            </h1>
            <p className="text-clara text-lg lg:text-xl font-normal mb-4">
              Pets e agendamentos em um só lugar
            </p>
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

        {/* Lado direito: formulário */}
        <div className="w-1/2 min-h-full bg-fundo flex items-center justify-center p-8 sm:p-12">
          <div className="w-full max-w-[420px] bg-superficie rounded-cartoes_e_pilulas border border-borda p-8 sm:p-10 shadow-sm">
            <h2 className="text-2xl font-bold text-slate-800 mb-1">
              Entrar
            </h2>
            <p className="text-sm text-textoSuave mb-8">
              Informe suas credenciais para acessar sua conta.
            </p>

            {erro && (
              <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                {erro}
              </div>
            )}

            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  E-mail
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  disabled={carregando}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="exemplo@email.com"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-60"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  Senha
                </label>
                <input
                  type="password"
                  required
                  value={senha}
                  disabled={carregando}
                  onChange={(e) => setSenha(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-60"
                />
              </div>

              <button
                type="submit"
                disabled={carregando}
                className="w-full py-3 mt-2 bg-acao hover:bg-[#14532d] disabled:opacity-60 text-superficie text-sm font-semibold rounded-campos_e_botoes transition-colors cursor-pointer"
              >
                {carregando ? 'Entrando...' : 'Entrar'}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-textoSuave">
              Não tem uma conta?{' '}
              <Link
                to="/cadastro"
                className="text-primaria font-semibold hover:underline transition-colors cursor-pointer"
              >
                Cadastre-se
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;