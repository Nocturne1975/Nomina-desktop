import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { BookOpen, Code, Puzzle, Rocket } from "lucide-react";

const docSections = [
  {
    icon: Rocket,
    title: "Démarrage rapide",
    description: "Configurez votre première requête en moins de 5 minutes",
    link: "#"
  },
  {
    icon: Code,
    title: "Référence API",
    description: "Documentation complète de tous les endpoints et paramètres",
    link: "#"
  },
  {
    icon: Puzzle,
    title: "SDK & Bibliothèques",
    description: "Intégrations pour JavaScript, Python, Ruby et plus",
    link: "#"
  },
  {
    icon: BookOpen,
    title: "Guides & Tutoriels",
    description: "Exemples pratiques et cas d'usage détaillés",
    link: "#"
  }
];

export function Documentation() {
  return (
    <section id="docs" className="py-20 bg-gradient-to-b from-[#f8f6fc] to-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl text-[#2d1b4e] mb-4" style={{ fontFamily: 'Cinzel, serif' }}>
            Documentation
          </h2>
          <p className="text-lg text-[#c5bfd9] max-w-2xl mx-auto">
            Tout ce dont vous avez besoin pour intégrer Nomina
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {docSections.map((section, index) => (
            <Card
              key={index}
              className="bg-white border-[#d4c5f9] p-6 hover:shadow-lg hover:shadow-[#7b3ff2]/10 transition-all duration-300 hover:border-[#7b3ff2] cursor-pointer group"
            >
              <div className="w-12 h-12 bg-gradient-to-br from-[#7b3ff2] to-[#a67be8] rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <section.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg text-[#2d1b4e] mb-2">
                {section.title}
              </h3>
              <p className="text-sm text-[#c5bfd9]">
                {section.description}
              </p>
            </Card>
          ))}
        </div>

        {/* Code Examples */}
        <div className="max-w-4xl mx-auto">
          <Card className="bg-[#2d1b4e] border-[#7b3ff2]/30 p-8">
            <h3 className="text-2xl text-white mb-6" style={{ fontFamily: 'Cinzel, serif' }}>
              Exemples de code
            </h3>

            <div className="space-y-6">
              {/* JavaScript Example */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-[#d4c5f9]">JavaScript / Node.js</span>
                  <Button size="sm" variant="ghost" className="text-[#d4c5f9] hover:text-white hover:bg-[#7b3ff2]/20">
                    Copier
                  </Button>
                </div>
                <div className="bg-[#1a0f33] rounded-lg p-4 overflow-x-auto">
                  <pre>
                    <code className="text-sm text-[#a67be8]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
{`import Nomina from '@nomina/sdk';

const nomina = new Nomina('YOUR_API_KEY');

const character = await nomina.generate({
  type: 'character',
  genre: 'fantasy',
  withBio: true
});

console.log(character.name); // "Éléandra Brumeveil"`}
                    </code>
                  </pre>
                </div>
              </div>

              {/* Python Example */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-[#d4c5f9]">Python</span>
                  <Button size="sm" variant="ghost" className="text-[#d4c5f9] hover:text-white hover:bg-[#7b3ff2]/20">
                    Copier
                  </Button>
                </div>
                <div className="bg-[#1a0f33] rounded-lg p-4 overflow-x-auto">
                  <pre>
                    <code className="text-sm text-[#a67be8]" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
{`from nomina import NominaClient

client = NominaClient(api_key='YOUR_API_KEY')

character = client.generate(
    type='character',
    genre='fantasy',
    with_bio=True
)

print(character.name)  # "Éléandra Brumeveil"`}
                    </code>
                  </pre>
                </div>
              </div>
            </div>

            <div className="mt-8 text-center">
              <Button className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white">
                Voir la documentation complète
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
}
