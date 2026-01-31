import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { Features } from "./components/Features";
import { UseCases } from "./components/UseCases";
import { ApiDemo } from "./components/ApiDemo";
import { Pricing } from "./components/Pricing";
import { Documentation } from "./components/Documentation";
import { Footer } from "./components/Footer";
import { useEffect } from "react";
import { flushOutbox } from "./lib/api";
import { Routes, Route, Navigate } from "react-router-dom";
import { GeneratePage } from "./pages/GeneratePage";
import { UsersPage } from "./pages/UsersPage";
import { AdminPage } from "./pages/AdminPage";

export default function App() {
  useEffect(() => {
    // Tente une synchro au démarrage (si des requêtes offline existent).
    flushOutbox().catch(() => undefined);

    const onOnline = () => {
      flushOutbox().catch(() => undefined);
    };
    window.addEventListener('online', onOnline);
    return () => window.removeEventListener('online', onOnline);
  }, []);

  return (
    <div className="min-h-screen">
      <Header />
      <main>      
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Hero />
                <Features />
                <UseCases />
                <ApiDemo />
                <Pricing />
                <Documentation />
              </>
            }
          />
          <Route path="/features" element={<Features />} />
          <Route path="/usecases" element={<UseCases />} />
          <Route path="/demo" element={<ApiDemo />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/docs" element={<Documentation />} />
          <Route path="/generate" element={<GeneratePage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>   
      </main>
      <Footer />
    </div>
  );
}
