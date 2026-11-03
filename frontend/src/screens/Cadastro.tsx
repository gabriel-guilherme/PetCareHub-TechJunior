import { NavBar } from '../components/NavBar';
import { PawIcon } from '../components/PawIcon';
import { CheckIcon } from '../components/CheckIcon';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const vantagens = [
  'Cadastro de pets',
  'Agendamento online',
  'Assistente virtual',
];

interface CadastroProps {
  onIrParaLogin?: () => void;
}

export function Cadastro({ }: CadastroProps) {
  const navigate = useNavigate();
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [senha, setSenha] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Impede a tela de reiniciar!
    setErro(null);
    setCarregando(true);

    try {
      // 1. Envia para o Spring Boot via proxy
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: nome.trim(),
          email: email.trim(),
          telefone: telefone.trim(),
          senha: senha,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || errorData.error || 'Erro ao realizar cadastro.');
      }

      // 2. Faz login automático
      const loginRes = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), senha }),
      });

      if (loginRes.ok) {
        const loginData = await loginRes.json();
        if (loginData.token) {
          localStorage.setItem('petcarehub_token', loginData.token);
        }
        navigate('/pets');
      } else {
        navigate('/login');
      }
    } catch (err: any) {
      setErro(err.message || 'Falha ao conectar com o backend.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full">
      <NavBar />

      <div className="flex flex-1 w-full">
        {/* LADO ESQUERDO: Idêntico ao Login (Consistência de Marca) */}
        <div className="w-1/2 bg-primaria flex flex-col justify-center px-12 lg:px-24 py-16 text-superficie">
          <div className="max-w-md flex flex-col gap-6">
            <PawIcon size={56} className="text-clara block" />

            <h1 className="text-4xl lg:text-5xl font-bold tracking-tight">
              Junte-se a nós
            </h1>

            <p className="text-clara text-lg lg:text-xl font-normal">
              Pets e agendamentos em um só lugar
            </p>

            <ul className="flex flex-col gap-4 mt-2">
              {vantagens.map((texto) => (
                <li key={texto} className="flex items-center gap-3.5 text-base font-medium">
                  <CheckIcon size={20} className="text-clara" />
                  <span>{texto}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* LADO DIREITO: Cartão com os 4 campos do RF01 */}
        <div className="w-1/2 min-h-full bg-fundo flex items-center justify-center p-8 sm:p-12">
          <div className="w-full max-w-[440px] bg-superficie rounded-cartoes_e_pilulas border border-borda p-8 sm:p-10 shadow-sm">
            
            <h2 className="text-2xl font-bold text-slate-800 mb-1">
              Criar Conta
            </h2>
            <p className="text-sm text-textoSuave mb-6">
              Cadastre-se para gerenciar seus pets e agendamentos.
            </p>

            <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
              {erro && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-md">
                  {erro}
                </div>
              )}

              {/* 1. Nome Completo */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  Nome completo
                </label>
                <input
                  type="text"
                  required
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  placeholder="Carlos Silva"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria"
                />
              </div>

              {/* 2. E-mail */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  E-mail
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="exemplo@email.com"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria"
                />
              </div>

              {/* 3. Telefone */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  Telefone
                </label>
                <input
                  type="tel"
                  value={telefone}
                  onChange={(e) => setTelefone(e.target.value)}
                  placeholder="(84) 99999-9999"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria"
                />
              </div>

              {/* 4. Senha (minimo 8 caracteres) */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-slate-700">
                  Senha
                </label>
                <input
                  type="password"
                  required
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  placeholder="Mínimo de 8 caracteres"
                  className="w-full px-3.5 py-2.5 rounded-campos_e_botoes border border-borda bg-superficie text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primaria"
                />
              </div>
               {/* Mensagem de Erro (se houver) */}
              {erro && (
                <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                  {erro}
                </div>
              )}
              {/* Botão Cadastrar */}
              <button
                type="submit"
                disabled={carregando}
                className="w-full py-3 mt-2 bg-acao hover:bg-[#14532d] disabled:opacity-60 text-superficie text-sm font-semibold rounded-campos_e_botoes transition-colors cursor-pointer"
              >
                {carregando ? 'Cadastrando...' : 'Cadastrar'}
              </button>
            </form>

            {/* Link para Voltar ao Login */}
            <div className="mt-6 text-center text-sm text-textoSuave">
              Já tem uma conta?{' '}
              <Link
                to='/'
                className="text-primaria font-semibold hover:underline transition-colors cursor-pointer"
              >
                Entrar
              </Link>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default Cadastro;