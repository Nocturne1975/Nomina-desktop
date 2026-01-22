import { Button } from "./ui/button";
import { Sparkles, ArrowRight } from "lucide-react";
import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";

export function Hero() {
  const [kind, setKind] = useState<"character" | "place" | "creature">(
    "character",
  );
  const [genre, setGenre] = useState<"fantasy" | "scifi" | "mythic">("fantasy");
  const [seed, setSeed] = useState("");
  const [withBio, setWithBio] = useState(true);

  const [result, setResult] = useState<{ name: string; bio?: string } | null>(
    null,
  );

  const dictionaries = useMemo(
    () => ({
      character: {
        fantasy: {
          first: ["Ael", "Lys", "Kael", "Mira", "Ery", "Soren"],
          last: ["d'Or", "Nuit", "Brume", "Val", "Lune", "Cendre"],
          bio: [
            "un voyageur discret au passé trouble",
            "une archiviste fascinée par les noms anciens",
            "un duelliste réputé dans les ruelles de la cité",
          ],
        },
        scifi: {
          first: ["Nova", "Kai", "Zed", "Aria", "Orion", "Vex"],
          last: ["-7", "Prime", "Kappa", "Helix", "Sable", "Vector"],
          bio: [
            "un pilote de cargo qui ne fait confiance qu’à ses capteurs",
            "une analyste de données qui parle en probabilités",
            "un ingénieur qui répare tout, sauf ses regrets",
          ],
        },
        mythic: {
          first: ["Théo", "Iris", "Nyx", "Astra", "Eos", "Atlas"],
          last: ["d'Éther", "des Vents", "du Serment", "des Oracles", "d'Aube"],
          bio: [
            "un messager au service d’un pacte oublié",
            "une prêtresse qui lit les signes dans la fumée",
            "un gardien lié à une étoile mourante",
          ],
        },
      },
      place: {
        fantasy: {
          first: ["Val", "Mont", "Brise", "Roc", "Sombre", "Aube"],
          last: ["-clair", "-noir", "-d'Azur", "-des-Épines", "-sur-Lune"],
          bio: [
            "un hameau perché où le vent raconte des légendes",
            "une cité portuaire aux lanternes éternelles",
            "des ruines dont les murs chuchotent des noms",
          ],
        },
        scifi: {
          first: ["Station", "Dôme", "Nexus", "Colonie", "Port"],
          last: ["Epsilon", "Delta", "Oméga", "Astra", "Kepler"],
          bio: [
            "un avant-poste minier au bord de la ceinture",
            "un hub commercial où chaque porte a un prix",
            "une base de recherche sous surveillance constante",
          ],
        },
        mythic: {
          first: ["Sanctuaire", "Temple", "Grotte", "Île", "Forêt"],
          last: ["des-Échos", "des-Serments", "du-Zéphyr", "des-Miroirs"],
          bio: [
            "un lieu sacré qui change avec la lune",
            "un passage caché entre deux mythes",
            "un domaine interdit où l’on perd son nom",
          ],
        },
      },
      creature: {
        fantasy: {
          first: ["Grif", "Syl", "Drak", "Umbra", "Fae", "Morn"],
          last: ["-aile", "-crocs", "-brume", "-écaille", "-ombre"],
          bio: [
            "une créature nocturne attirée par les promesses",
            "un gardien des clairières interdites",
            "un prédateur silencieux aux yeux d’ambre",
          ],
        },
        scifi: {
          first: ["Xeno", "Bio", "Cryo", "Nano", "Proto"],
          last: ["forme", "drone", "hôte", "spectre", "organisme"],
          bio: [
            "un organisme adaptatif qui apprend en observant",
            "une entité qui perturbe les communications",
            "un échantillon échappé d’un labo clandestin",
          ],
        },
        mythic: {
          first: ["Chim", "Serp", "Harp", "Cér", "Ném"],
          last: ["-ère", "-entine", "-ie", "-bère", "-ésis"],
          bio: [
            "une bête liée à un ancien interdit",
            "un esprit qui protège les noms vrais",
            "un symbole vivant d’un destin brisé",
          ],
        },
      },
    }),
    [],
  );

  function randomPick<T>(arr: T[]) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function generate() {
    const dict = dictionaries[kind][genre];
    const left = seed.trim() ? seed.trim() : randomPick(dict.first);
    const right = randomPick(dict.last);
    const name = `${left}${right}`;
    const bio = withBio ? `C’est ${randomPick(dict.bio)}.` : undefined;
    setResult({ name, bio });
  }

  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-[#2d1b4e] via-[#1a0f33] to-[#2d1b4e] py-20 md:py-32">
      {/* Decorative elements */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 left-10 w-72 h-72 bg-[#7b3ff2] rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-[#a67be8] rounded-full blur-3xl"></div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-[#7b3ff2]/20 border border-[#7b3ff2]/30 rounded-full mb-6">
            <Sparkles className="w-4 h-4 text-[#e8b4f0]" />
            <span className="text-sm text-[#d4c5f9]">API de génération narrative</span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl text-white mb-6" style={{ fontFamily: 'Cinzel, serif' }}>
            Créez, Nommez, Racontez
          </h1>

          {/* Description */}
          <p className="text-lg md:text-xl text-[#d4c5f9] mb-8 max-w-2xl mx-auto">
            Une API innovante dédiée à la narration et à la génération de noms. 
            Créez des personnages, des lieux et des créatures avec des histoires captivantes.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Button size="lg" className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white px-8 gap-2">
              Commencer gratuitement
              <ArrowRight className="w-5 h-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-[#7b3ff2] text-[#d4c5f9] hover:bg-[#7b3ff2]/20">
              Voir la documentation
            </Button>
          </div>

          {/* Mini UI: Générateur */}
          <Card className="bg-[#f8f6fc] border-[#d4c5f9] shadow-xl shadow-[#7b3ff2]/10 max-w-2xl mx-auto text-left">
            <CardHeader>
              <CardTitle className="text-[#2d1b4e]" style={{ fontFamily: "Cinzel, serif" }}>
                Générer un nom
              </CardTitle>
              <p className="text-sm text-[#c5bfd9]">
                Un aperçu UI (sans code affiché). Tu brancheras l’API ensuite.
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm text-[#2d1b4e]">Type</label>
                  <select
                    value={kind}
                    onChange={(e) => setKind(e.target.value as typeof kind)}
                    className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
                  >
                    <option value="character">Personnage</option>
                    <option value="place">Lieu</option>
                    <option value="creature">Créature</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm text-[#2d1b4e]">Genre</label>
                  <select
                    value={genre}
                    onChange={(e) => setGenre(e.target.value as typeof genre)}
                    className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
                  >
                    <option value="fantasy">Fantasy</option>
                    <option value="scifi">Sci‑Fi</option>
                    <option value="mythic">Mythique</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm text-[#2d1b4e]">Préfixe (optionnel)</label>
                  <Input
                    value={seed}
                    onChange={(e) => setSeed(e.target.value)}
                    placeholder="Ex: Ael / Nova / Val"
                    className="mt-2 border-[#d4c5f9] bg-white"
                  />
                </div>
              </div>

              <label className="mt-4 flex items-center gap-2 text-sm text-[#2d1b4e]">
                <input
                  type="checkbox"
                  checked={withBio}
                  onChange={(e) => setWithBio(e.target.checked)}
                />
                Ajouter une mini-description
              </label>

              <div className="mt-5 flex flex-col sm:flex-row items-start sm:items-center gap-3">
                <Button
                  onClick={generate}
                  className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white"
                >
                  Générer
                </Button>
                {result ? (
                  <div>
                    <div className="text-[#2d1b4e] font-semibold">{result.name}</div>
                    {result.bio ? (
                      <div className="text-sm text-[#6b5aa3]">{result.bio}</div>
                    ) : null}
                  </div>
                ) : (
                  <div className="text-sm text-[#c5bfd9]">
                    Clique sur “Générer” pour voir un exemple.
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
