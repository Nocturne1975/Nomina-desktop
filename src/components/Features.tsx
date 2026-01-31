import { Card } from "./ui/card";
import { Wand2, BookOpen, Zap, Globe, Shield, Code } from "lucide-react";

const features = [
  {
    icon: Wand2,
    title: "Génération intelligente",
    description: "Algorithmes avancés pour créer des noms uniques et mémorables adaptés à votre univers narratif."
  },
  {
    icon: BookOpen,
    title: "Narration intégrée",
    description: "Obtenez des mini-biographies et descriptions narratives pour donner vie à vos créations."
  },
  {
    icon: Zap,
    title: "Rapide et fiable",
    description: "API haute performance avec temps de réponse < 100ms et disponibilité de 99.9%."
  },
  {
    icon: Globe,
    title: "Multi-langues",
    description: "Support de plusieurs langues et cultures pour des noms authentiques et diversifiés."
  },
  {
    icon: Shield,
    title: "Sécurisé",
    description: "Infrastructure sécurisée avec authentification robuste et respect de la vie privée."
  },
  {
    icon: Code,
    title: "Facile à intégrer",
    description: "Documentation complète, SDK disponibles et exemples de code pour démarrer rapidement."
  }
];

export function Features() {
  return (
    <section id="features" className="py-20 bg-[#f8f6fc]">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl text-[#2d1b4e] mb-4" style={{ fontFamily: 'Cinzel, serif' }}>
            Fonctionnalités puissantes
          </h2>
          <p className="text-lg text-[#c5bfd9] max-w-2xl mx-auto">
            Tout ce dont vous avez besoin pour créer des noms et des histoires captivantes
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={index}
              className="bg-white border-[#d4c5f9] p-6 hover:shadow-lg hover:shadow-[#7b3ff2]/10 transition-all duration-300 hover:border-[#7b3ff2]"
            >
              <div className="w-12 h-12 bg-gradient-to-br from-[#7b3ff2] to-[#a67be8] rounded-lg flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl text-[#2d1b4e] mb-2">
                {feature.title}
              </h3>
              <p className="text-[#c5bfd9]">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
