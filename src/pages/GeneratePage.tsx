import { useEffect, useMemo, useState } from "react";
import { apiFetch, ApiError } from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card } from "../components/ui/card";

type Univers = { id: number; name: string };
type Categorie = { id: number; name: string; universId: number };
type Culture = { id: number; name: string };
type Concept = { id: number; valeur: string; categorieId: number | null };

type NpcResult = unknown;

type GenerateWhat = "npcs" | "lieux" | "nomPersonnages" | "fragmentsHistoire" | "titres" | "concepts";

export function GeneratePage() {
  const [loadingInit, setLoadingInit] = useState(true);
  const [loading, setLoading] = useState(false);

  const [univers, setUnivers] = useState<Univers[]>([]);
  const [categories, setCategories] = useState<Categorie[]>([]);
  const [cultures, setCultures] = useState<Culture[]>([]);
  const [concepts, setConcepts] = useState<Concept[]>([]);

  const [universId, setUniversId] = useState<number | "">("");
  const [categorieId, setCategorieId] = useState<number | "">("");
  const [cultureId, setCultureId] = useState<number | "">("");
  const [conceptId, setConceptId] = useState<number | "">("");

  const [generateWhat, setGenerateWhat] = useState<GenerateWhat>("nomPersonnages");

  const [count, setCount] = useState(10);
  const [genre, setGenre] = useState<string>("");
  const [prefixe, setPrefixe] = useState("");

  const [result, setResult] = useState<NpcResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const supportsGenre = useMemo(() => {
    return (
      generateWhat === "npcs" ||
      generateWhat === "nomPersonnages" ||
      generateWhat === "fragmentsHistoire" ||
      generateWhat === "titres"
    );
  }, [generateWhat]);

  const supportsCulture = useMemo(() => {
    return (
      generateWhat === "npcs" ||
      generateWhat === "nomPersonnages" ||
      generateWhat === "fragmentsHistoire" ||
      generateWhat === "titres"
    );
  }, [generateWhat]);

  const filteredCategories = useMemo(() => {
    if (universId === "") return categories;
    return categories.filter((c) => c.universId === universId);
  }, [categories, universId]);

  const filteredConcepts = useMemo(() => {
    if (categorieId === "") return concepts;
    return concepts.filter((c) => c.categorieId === categorieId);
  }, [concepts, categorieId]);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoadingInit(true);
      setError(null);
      try {
        const [u, cats, cults, conc] = await Promise.all([
          apiFetch<Univers[]>("/univers"),
          apiFetch<Categorie[]>("/categories"),
          apiFetch<Culture[]>("/cultures"),
          apiFetch<Concept[]>("/concepts"),
        ]);

        if (cancelled) return;
        setUnivers(u);
        setCategories(cats);
        setCultures(cults);
        setConcepts(conc);
      } catch (e) {
        if (cancelled) return;
        setError(e instanceof ApiError ? `${e.message} (HTTP ${e.status})` : String(e));
      } finally {
        if (!cancelled) setLoadingInit(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    setCategorieId("");
    setConceptId("");
  }, [universId]);

  useEffect(() => {
    setConceptId("");
  }, [categorieId]);
  
  async function onGenerate() {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const endpointByWhat: Record<GenerateWhat, string> = {
        npcs: "/generate/npcs",
        lieux: "/generate/lieux",
        // L'intention UX: un personnage = nom + courte biographie.
        nomPersonnages: "/generate/npcs",
        fragmentsHistoire: "/generate/fragments-histoire",
        titres: "/generate/titres",
        concepts: "/generate/concepts",
      };

      const endpoint = endpointByWhat[generateWhat];

      const qs = new URLSearchParams();
      qs.set("count", String(count));
      if (prefixe.trim()) qs.set("seed", prefixe.trim());

      if (supportsGenre && genre) qs.set("genre", genre);

      if (cultureId !== "" && supportsCulture) qs.set("cultureId", String(cultureId));
      if (categorieId !== "") qs.set("categorieId", String(categorieId));

      // Si on génère des concepts, la catégorie sert de filtre principal.
      // (Sans catégorie, l'API retourne des concepts tous univers confondus.)

      const url = `${endpoint}?${qs.toString()}`;
      const data = await apiFetch<NpcResult>(url);
      setResult(data);
    } catch (e) {
      setError(e instanceof ApiError ? `${e.message} (HTTP ${e.status})` : String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-6 bg-gradient-to-b from-[#f8f6fc] to-white">
      <h1 className="text-3xl text-[#2d1b4e] mb-6" style={{ fontFamily: "Cinzel, serif" }}>
        Génération
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Formulaire à gauche */}
        <Card className="p-4 border-[#d4c5f9] h-fit">
          <div className="grid gap-4">
            {loadingInit ? <p>Chargement des listes…</p> : null}

            <div>
              <label className="text-sm text-[#2d1b4e]">Univers Thématique</label>
              <select
                value={universId}
                onChange={(e) => setUniversId(e.target.value ? Number(e.target.value) : "")}
                className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
              >
                <option value="">— Tous —</option>
                {univers.map((u) => (
                  <option key={u.id} value={u.id}>{u.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm text-[#2d1b4e]">Catégorie</label>
              <select
                value={categorieId}
                onChange={(e) => setCategorieId(e.target.value ? Number(e.target.value) : "")}
                className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
              >
                <option value="">— Toutes —</option>
                {filteredCategories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm text-[#2d1b4e]">Quelle Culture</label>
              <select
                value={cultureId}
                onChange={(e) => setCultureId(e.target.value ? Number(e.target.value) : "")}
                className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
              >
                <option value="">— Toutes —</option>
                {cultures.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            {generateWhat === "concepts" ? (
              <div>
                <label className="text-sm text-[#2d1b4e]">Quel Concept</label>
                <select
                  value={conceptId}
                  onChange={(e) => setConceptId(e.target.value ? Number(e.target.value) : "")}
                  className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
                >
                  <option value="">— Tous —</option>
                  {filteredConcepts.map((c) => (
                    <option key={c.id} value={c.id}>{c.valeur}</option>
                  ))}
                </select>
              </div>
            ) : null}

            <div>
              <label className="text-sm text-[#2d1b4e]">Que voulez-vous générer ?</label>
              <select
                value={generateWhat}
                onChange={(e) => setGenerateWhat(e.target.value as GenerateWhat)}
                className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
              >
                <option value="npcs">🧙 Biographie (PNJ complet)</option>
                <option value="nomPersonnages">👤 Personnage (nom + courte biographie)</option>
                <option value="lieux">🏛️ Lieux</option>
                <option value="concepts">💡 Concepts</option>
                <option value="fragmentsHistoire">📜 Fragments d'histoire</option>
                <option value="titres">👑 Titres</option>
              </select>
            </div>

            {supportsGenre ? (
              <div>
                <label className="text-sm text-[#2d1b4e]">Genre (optionnel)</label>
                <select
                  value={genre}
                  onChange={(e) => setGenre(e.target.value)}
                  className="mt-2 w-full h-9 rounded-md border border-[#d4c5f9] bg-white px-3 text-sm"
                >
                  <option value="">— Tous —</option>
                  <option value="masculin">Masculin</option>
                  <option value="feminin">Féminin</option>
                  <option value="nb">Non-binaire</option>
                </select>
              </div>
            ) : null}

            <div>
              <label className="text-sm text-[#2d1b4e]">Nombre</label>
              <Input type="number" value={count} min={1} max={200} onChange={(e) => setCount(Number(e.target.value))} />
            </div>

            <div>
              <label className="text-sm text-[#2d1b4e]">Préfixe (optionnel)</label>
              <Input value={prefixe} onChange={(e) => setPrefixe(e.target.value)} placeholder="Ex: Ael / Nova / Val" />
            </div>

            <Button onClick={onGenerate} disabled={loading || loadingInit} className="bg-[#7b3ff2] hover:bg-[#a67be8] text-white">
              {loading ? "Génération…" : "Générer (API)"}
            </Button>

            {error ? <p className="text-red-700">{error}</p> : null}
          </div>
        </Card>

        {/* Résultats à droite */}
        <div>
          {result ? (
            <div className="bg-white border border-[#d4c5f9] rounded-lg p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-[#2d1b4e] mb-2" style={{ fontFamily: "Cinzel, serif" }}>
                ✨ Vos créations narratives
              </h3>
              <p className="text-sm text-[#6b5aa3] mb-4">
                Découvrez les éléments générés pour enrichir votre univers
              </p>
              
              <div className="flex flex-wrap gap-3 mb-4 p-3 bg-[#f8f6fc] rounded-md">
                {(result as any).seed && (
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-[#7b3ff2]">🎲 Préfixe:</span>
                    <code className="text-xs bg-white px-2 py-1 rounded border border-[#d4c5f9] text-[#2d1b4e]">
                      {(result as any).seed}
                    </code>
                  </div>
                )}
                {(result as any).count !== undefined && (
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-[#7b3ff2]">📊 Générés:</span>
                    <span className="text-xs font-bold text-[#2d1b4e]">{(result as any).count}</span>
                  </div>
                )}
              </div>

              {(result as any).warning && (
                <div className="bg-orange-50 border-l-4 border-orange-400 text-orange-800 px-4 py-3 rounded-r-md mb-4 flex items-start gap-3">
                  <span className="text-xl">⚠️</span>
                  <div>
                    <p className="font-medium">Attention</p>
                    <p className="text-sm">{(result as any).warning}</p>
                  </div>
                </div>
              )}

              {(result as any).items && Array.isArray((result as any).items) && (result as any).items.length > 0 ? (
                <div className="space-y-4 max-h-[calc(100vh-350px)] overflow-y-auto pr-2">
                  {(result as any).items.map((item: any, idx: number) => {
                    const isLieu = item.value !== undefined;
                    const isPersonnage = item.name !== undefined;
                    const isConcept = item.valeur !== undefined && !item.name;
                    
                    return (
                      <div key={idx} className="bg-gradient-to-br from-[#f8f6fc] to-white border border-[#e8e0f5] rounded-lg p-5 hover:shadow-md transition-shadow">
                        <div className="mb-3">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="flex items-center justify-center w-6 h-6 bg-[#7b3ff2] text-white text-xs font-bold rounded-full">
                              {idx + 1}
                            </span>
                            {isPersonnage && item.name && (
                              <h4 className="text-[#2d1b4e] font-bold text-xl" style={{ fontFamily: "Cinzel, serif" }}>
                                {item.name}
                              </h4>
                            )}
                            {isLieu && item.value && (
                              <h4 className="text-[#2d1b4e] font-bold text-xl" style={{ fontFamily: "Cinzel, serif" }}>
                                {item.value}
                              </h4>
                            )}
                            {isConcept && item.valeur && (
                              <h4 className="text-[#2d1b4e] font-bold text-xl" style={{ fontFamily: "Cinzel, serif" }}>
                                {item.valeur}
                              </h4>
                            )}
                          </div>
                          
                          {isPersonnage && (
                            <p className="text-sm text-[#a67be8] italic pl-8">
                              Un personnage qui marquera votre récit...
                            </p>
                          )}
                          {isLieu && item.type && (
                            <p className="text-sm text-[#a67be8] italic pl-8">
                              {item.type === 'ville' && 'Une cité qui respire la vie et les secrets...'}
                              {item.type === 'region' && 'Une région aux horizons infinis...'}
                              {item.type === 'lieu' && 'Un endroit chargé d\'histoire...'}
                              {!['ville', 'region', 'lieu'].includes(item.type) && 'Un lieu singulier dans votre monde...'}
                            </p>
                          )}
                          {isConcept && (
                            <p className="text-sm text-[#a67be8] italic pl-8">
                              Un concept qui enrichira votre narration...
                            </p>
                          )}
                        </div>

                        {item.backstory && (
                          <div className="bg-white/60 border-l-4 border-[#a67be8] pl-4 py-3 mb-3 rounded-r">
                            <p className="text-[#4a3a6a] text-sm leading-relaxed">
                              <span className="text-[#7b3ff2] font-semibold">📖 Son histoire : </span>
                              <span className="italic">"{item.backstory}"</span>
                            </p>
                          </div>
                        )}
                        
                        {isLieu && !item.backstory && (
                          <div className="bg-white/60 border-l-4 border-[#a67be8] pl-4 py-3 mb-3 rounded-r">
                            <p className="text-[#4a3a6a] text-sm leading-relaxed">
                              <span className="text-[#7b3ff2] font-semibold">🗺️ Description : </span>
                              {item.type === 'oasis' && <span>Au cœur des étendues arides, {item.value} offre un havre de paix où l'eau claire attire voyageurs et créatures du désert.</span>}
                              {item.type === 'plaine' && <span>Les vastes étendues de {item.value} s'étendent à perte de vue, balayées par les vents et parsemées de traces d'anciennes civilisations.</span>}
                              {item.type === 'fjord' && <span>Entre les falaises abruptes, {item.value} découpe la côte de ses eaux profondes et mystérieuses.</span>}
                              {item.type === 'region' && <span>La région de {item.value} s'étend sur des territoires variés, chacun portant les marques de son histoire unique.</span>}
                              {item.type === 'desert' && <span>Les dunes infinies de {item.value} cachent des secrets sous leurs sables mouvants.</span>}
                              {!['oasis', 'plaine', 'fjord', 'region', 'desert'].includes(item.type || '') && 
                                <span>Dans votre univers, {item.value} occupe une place singulière qui ne demande qu'à être explorée.</span>}
                            </p>
                          </div>
                        )}

                        {item.texte && (
                          <div className="bg-amber-50/50 border-l-4 border-amber-400 pl-4 py-3 mb-3 rounded-r">
                            <p className="text-[#4a3a6a] text-sm leading-relaxed">
                              <span className="text-amber-700 font-semibold">✍️ Fragment narratif : </span>
                              {item.texte}
                            </p>
                          </div>
                        )}

                        {isConcept && (item.mood || item.keywords) ? (
                          <div className="bg-white/60 border-l-4 border-[#a67be8] pl-4 py-3 mb-3 rounded-r">
                            <p className="text-[#4a3a6a] text-sm leading-relaxed">
                              <span className="text-[#7b3ff2] font-semibold">💡 Détails : </span>
                              {item.mood ? <span className="italic">Ambiance: {item.mood}</span> : null}
                              {item.mood && item.keywords ? <span> — </span> : null}
                              {item.keywords ? <span>Mots‑clés: {item.keywords}</span> : null}
                            </p>
                          </div>
                        ) : null}

                        <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-[#e8e0f5]">
                          {item.genre && (
                            <span className="inline-flex items-center gap-1 text-xs bg-purple-100 text-purple-700 px-3 py-1 rounded-full font-medium">
                              <span>⚧</span> Genre {item.genre}
                            </span>
                          )}
                          {item.type && (
                            <span className="inline-flex items-center gap-1 text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
                              <span>🏷️</span> Type : {item.type}
                            </span>
                          )}
                          {item.cultureId && (
                            <span className="inline-flex items-center gap-1 text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                              <span>🌍</span> Culture #{item.cultureId}
                            </span>
                          )}
                          {item.categorieId && (
                            <span className="inline-flex items-center gap-1 text-xs bg-amber-100 text-amber-700 px-3 py-1 rounded-full font-medium">
                              <span>📂</span> Catégorie #{item.categorieId}
                            </span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">📭</div>
                  <p className="text-[#6b5aa3] font-medium">Aucun récit à raconter pour l'instant</p>
                  <p className="text-sm text-[#c5bfd9] mt-1">Ajustez vos filtres et lancez la magie narrative</p>
                </div>
              )}

              <details className="mt-6 border-t border-[#d4c5f9] pt-4">
                <summary className="text-sm text-[#7b3ff2] cursor-pointer hover:text-[#a67be8] font-medium flex items-center gap-2">
                  <span>🔧</span> Mode développeur : voir le JSON brut
                </summary>
                <pre className="bg-gray-900 text-green-400 p-4 rounded-md overflow-auto text-xs mt-3 border border-gray-700 max-h-96 font-mono">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </details>
            </div>
          ) : (
            <div className="bg-gradient-to-br from-white to-[#f8f6fc] border-2 border-dashed border-[#d4c5f9] rounded-lg p-8 shadow-sm text-center">
              <div className="text-5xl mb-4">✨</div>
              <h3 className="text-lg font-semibold text-[#2d1b4e] mb-2" style={{ fontFamily: "Cinzel, serif" }}>
                Prêt à créer ?
              </h3>
              <p className="text-[#6b5aa3] text-sm">
                Configurez vos filtres et lancez la génération.<br />
                Les résultats apparaîtront ici comme par magie.
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}