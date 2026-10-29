import { useState } from 'react';
import { Login } from './screens/Login';
import { Cadastro } from './screens/Cadastro';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

export default function App() {
  const [telaAtual, setTelaAtual] = useState<'login' | 'cadastro'>('login');

  return (
    <BrowserRouter>
      <Routes>
        {/* Define a rota raiz (/) para abrir direto na tela de login */}
        <Route path="/" element={<Login />} />

        {/* Define a rota para a tela de login */}
        <Route path="/login" element={<Login />} />
        
        {/* Define a rota para a tela de cadastro */}
        <Route path="/cadastro" element={<Cadastro />} />
      </Routes>
    </BrowserRouter>
  );

  /*if (telaAtual === 'cadastro') {
    return <Cadastro onIrParaLogin={() => setTelaAtual('login')} />;
  }

  return <Login onIrParaCadastro={() => setTelaAtual('cadastro')} />;*/
}


