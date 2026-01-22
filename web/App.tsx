import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { Features } from "./components/Features";
import { UseCases } from "./components/UseCases";
import { ApiDemo } from "./components/ApiDemo";
import { Pricing } from "./components/Pricing";
import { Documentation } from "./components/Documentation";
import { Footer } from "./components/Footer";

export default function App() {
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
