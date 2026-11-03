import { useState } from 'react';
import { Login } from './screens/Login';
import { Cadastro } from './screens/Cadastro';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Pets } from './screens/Pets';
import { Servicos } from './screens/Servicos';

export default function App() {
  

  return (
    <BrowserRouter>
      <Routes>
        {/* Define a rota raiz (/) para abrir direto na tela de login */}
        <Route path="/" element={<Login />} />

        {/* Define a rota para a tela de login */}
        <Route path="/login" element={<Login />} />
        
        {/* Define a rota para a tela de cadastro */}
        <Route path="/cadastro" element={<Cadastro />} />

        {/* Define a rota para a tela de pets */}
        <Route path="/pets" element={<Pets />} />

        {/* Define a rota para a tela de servicos */}
        <Route path="/servicos" element={<Servicos />} />

      </Routes>
    </BrowserRouter>
  );
  
}


