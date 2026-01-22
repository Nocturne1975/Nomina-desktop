import { Button } from "./ui/button";
import { Feather, Menu, X } from "lucide-react";
import { useState } from "react";

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-[#2d1b4e] border-b border-[#7b3ff2]/20">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#7b3ff2] to-[#a67be8] rounded-lg flex items-center justify-center">
              <Feather className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl text-white" style={{ fontFamily: 'Cinzel, serif' }}>
              Nomina
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
              Fonctionnalités
            </a>
            <a href="#usecases" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
              Cas d'usage
            </a>
            <a href="#pricing" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
              Tarifs
            </a>
            <a href="#docs" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
              Documentation
            </a>
          </nav>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-4">
            <Button variant="ghost" className="text-[#d4c5f9] hover:text-white hover:bg-[#7b3ff2]/20">
              Connexion
            </Button>
            <Button className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white">
              Commencer
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-[#7b3ff2]/20">
            <nav className="flex flex-col gap-4">
              <a href="#features" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
                Fonctionnalités
              </a>
              <a href="#usecases" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
                Cas d'usage
              </a>
              <a href="#pricing" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
                Tarifs
              </a>
              <a href="#docs" className="text-[#d4c5f9] hover:text-[#e8b4f0] transition-colors">
                Documentation
              </a>
              <div className="flex flex-col gap-2 pt-2">
                <Button variant="outline" className="border-[#7b3ff2] text-[#d4c5f9]">
                  Connexion
                </Button>
                <Button className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white">
                  Commencer
                </Button>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
