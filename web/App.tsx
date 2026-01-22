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
        <Hero />
        <Features />
        <UseCases />
        <ApiDemo />
        <Pricing />
        <Documentation />
      </main>
      <Footer />
    </div>
  );
}
