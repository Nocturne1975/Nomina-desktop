const http = require('http');
const { URL } = require('url');

function hashStringToSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function mulberry32(seed) {
  let t = seed >>> 0;
  return function next() {
    t += 0x6D2B79F5;
    let x = Math.imul(t ^ (t >>> 15), 1 | t);
    x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleWithoutReplacement(arr, k, rnd) {
  const copy = arr.slice();
  const out = [];
  for (let i = 0; i < k && copy.length > 0; i++) {
    const idx = Math.floor(rnd() * copy.length);
    out.push(copy[idx]);
    copy.splice(idx, 1);
  }
  return out;
}

function parseCount(raw) {
  const n = Number(raw);
  return Number.isFinite(n) ? Math.min(Math.max(n, 1), 200) : 10;
}

const universList = [
  "Mythologies & Religions anciennes",
  "Civilisations & Cultures historiques",
  "Merveilles & Mystères",
  "Fantasy & Surnaturel",
  "Science-fiction & Futur",
  "Mystère, Occulte & Étrange",
  "Nature & Mondes organiques",
  "Technologie & Mondes industriels",
  "Exploration & Aventure",
  "Concepts abstraits & symboliques",
  "Empires disparus",
  "Mondes féeriques",
  "Royaumes draconiques",
  "Mondes post-apocalyptiques",
  "Civilisations stellaires",
  "Futurs dystopiques",
  "Univers transhumanistes",
  "Mondes cybernétiques",
  "Dimensions parallèles",
  "Horreur cosmique",
  "Folklore sombre",
  "Mondes oniriques",
  "Cités perdues",
  "Ruines antiques",
  "Artefacts mystérieux",
  "Sites interdits",
  "Mondes désertiques",
  "Archipels tropicaux",
  "Forêts primordiales",
  "Montagnes sacrées",
  "Mondes polaires",
  "Écosystèmes étranges",
  "Mondes fongiques",
  "Sociétés robotisées",
  "Révolutions steampunk",
  "Mondes mécaniques",
  "Ingénieries perdues",
  "Laboratoires secrets",
  "Architectures colossales",
  "Routes anciennes",
  "Expéditions lointaines",
  "Cartographies impossibles",
  "Ports exotiques",
  "Frontières sauvages",
  "Esthétiques anciennes",
  "Arts rituels",
  "Symbolismes universels",
  "Langages oubliés",
  "Théâtres mythiques",
  "Musiques sacrées",
  "Forces cosmiques",
  "Paradoxes temporels",
  "Archétypes universels",
  "Énergies primordiales",
  "Mondes conceptuels",
  "Sciences anciennes",
  "Alchimie",
  "Astronomie mythique",
  "Savoirs interdits",
  "Archives universelles",
  "Âges mythiques",
  "Époques alternatives",
  "Futurs possibles",
  "Passés réinventés",
  "Boucles temporelles",
  "Mondes uchroniques",
  "Royaumes tribaux",
  "Sociétés nomades",
  "Cultures maritimes",
  "Civilisations désertiques",
  "Mondes féodaux",
  "Cultures artisanales",
  "Cosmologies primitives",
  "Traditions chamaniques",
  "Cultes ésotériques",
  "Spiritualités syncrétiques",
  "Panthéons oubliés",
  "Mondes élémentaires",
  "Terres maudites",
  "Ordres mystiques",
  "Bestiaires imaginaires",
  "Magies anciennes",
  "Réalités simulées",
  "Mondes terraformés",
  "Futurs rétrofuturistes",
  "Sociétés secrètes",
  "Phénomènes inexpliqués",
  "Lieux hantés",
  "Zones anormales",
  "Reliques sacrées",
  "Mondes marins",
  "Déserts vivants",
  "Mondes volcaniques",
  "Mondes souterrains",
  "Royaumes célestes",
  "Mondes fractals",
  "Univers miniatures",
  "Mondes cristallins",
  "Mondes organo‑mécaniques",
  "Univers labyrinthiques",
  "Mondes suspendus",
  "Mondes engloutis",
  "Mondes de brume",
  "Mondes de lumière",
  "Mondes d’ombre",
  "Mondes silencieux",
  "Mondes chantants",
  "Mondes en ruine",
  "Mondes renaissants",
];

const categoriesList = [
  "Mythologie nordique",
  "Mythologie grecque",
  "Mythologie égyptienne",
  "Mythologie mésopotamienne",
  "Mythologie maya",
  "Mythologie aztèque",
  "Mythologie hindoue",
  "Mythologie celte",
  "Mythologie japonaise (shinto)",
  "Mythologie inuit",
  "Civilisation maya",
  "Civilisation inca",
  "Civilisation aztèque",
  "Empire romain",
  "Empire byzantin",
  "Dynasties chinoises",
  "Royaumes africains anciens",
  "Civilisations mésopotamiennes",
  "Tribus nomades des steppes",
  "Europe médiévale",
  "Merveilles du monde oubliées",
  "Cités perdues",
  "Ruines cyclopéennes",
  "Artefacts impossibles",
  "Lieux maudits ou sacrés",
  "Monuments mégalithiques",
  "Royaumes elfiques",
  "Terres naines",
  "Contrées démoniaques",
  "Forêts enchantées",
  "Ordres de mages",
  "Bestiaires fantastiques",
  "Panthéons inventés",
];

const conceptsSeed = [
  { valeur: "Mémoire Volée", type: "hybrid", mood: "mélancolique", keywords: "souvenir,identité,quête,magie" },
  { valeur: "Oracles Mécaniques", type: "hybrid", mood: "mystique-tech", keywords: "machine,prophétie,engrenage,culte" },
  { valeur: "Cité à Étages Infinis", type: "hybrid", mood: "vertigineux", keywords: "verticalité,exploration,société,niveaux" },
  { valeur: "Pacte de Sang Éternel", type: "hybrid", mood: "sombre", keywords: "contrat,immortalité,secret,trahison" },
  { valeur: "Réalité Fragmentée", type: "hybrid", mood: "instable", keywords: "glitch,dimension,anomalie,fracture" },
];

function buildData() {
  const univers = universList
    .map((name, i) => ({ id: i + 1, name: String(name).trim() }))
    .filter((u) => u.name.length > 0 && u.name.toLowerCase() !== 'tous');

  const categories = categoriesList
    .map((name, i) => ({
      id: i + 1,
      name: String(name).trim(),
      universId: univers[i % univers.length].id,
    }))
    .filter((c) => c.name.length > 0);

  const concepts = conceptsSeed.map((c, i) => ({
    id: i + 1,
    valeur: c.valeur,
    type: c.type ?? null,
    mood: c.mood ?? null,
    keywords: c.keywords ?? null,
    categorieId: categories[i % categories.length].id,
  }));

  const cultures = [
    { id: 1, name: "Générique" },
    { id: 2, name: "Nordique" },
    { id: 3, name: "Impériale" },
  ];

  return { univers, categories, concepts, cultures };
}

function sendJson(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, If-None-Match, Cache-Control, Pragma',
  });
  res.end(payload);
}

function startLocalApi({ port = 3000 } = {}) {
  const data = buildData();

  const server = http.createServer((req, res) => {
    try {
      if (!req.url) return sendJson(res, 400, { error: 'Bad Request' });

      if (req.method === 'OPTIONS') {
        res.writeHead(204, {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, If-None-Match, Cache-Control, Pragma',
          'Cache-Control': 'no-store',
        });
        return res.end();
      }

      const url = new URL(req.url, `http://localhost:${port}`);
      const p = url.pathname;

      if (req.method === 'GET' && p === '/healthz') return sendJson(res, 200, { ok: true, mode: 'offline' });
      if (req.method === 'GET' && p === '/univers') return sendJson(res, 200, data.univers);
      if (req.method === 'GET' && p === '/categories') return sendJson(res, 200, data.categories);
      if (req.method === 'GET' && p === '/concepts') return sendJson(res, 200, data.concepts);
      if (req.method === 'GET' && p === '/cultures') return sendJson(res, 200, data.cultures);

      if (req.method === 'GET' && p === '/generate/npcs') {
        const count = parseCount(url.searchParams.get('count'));
        const seed = (url.searchParams.get('seed') || '').trim() || String(Date.now());
        const rnd = mulberry32(hashStringToSeed(seed));

        const prenoms = ["Ael", "Nova", "Kael", "Mira", "Soren", "Lyra", "Darian", "Iris", "Noé", "Maëlys"];
        const noms = ["Briselame", "Noirbois", "Ventclair", "Cendrefeuille", "Lunargent", "Grisepierre"];
        const roles = ["Mercenaire", "Archiviste", "Forgeron", "Espion", "Prêtresse", "Explorateur", "Cartographe"];
        const traits = ["soupçonneux", "loyal", "imprévisible", "calme", "ambitieux", "rancunier", "curieux"];
        const hooks = ["une dette", "un pacte ancien", "un héritage", "un crime", "un nom volé", "une prophétie"];

        const pool = Array.from({ length: 400 }).map((_, i) => ({
          id: i + 1,
          name: `${prenoms[Math.floor(rnd() * prenoms.length)]} ${noms[Math.floor(rnd() * noms.length)]}`,
          role: roles[Math.floor(rnd() * roles.length)],
          trait: traits[Math.floor(rnd() * traits.length)],
          hook: `Cache ${hooks[Math.floor(rnd() * hooks.length)]}.`,
        }));

        const items = sampleWithoutReplacement(pool, count, rnd);
        return sendJson(res, 200, { seed, count: items.length, items, warning: null });
      }

      if (req.method === 'GET' && p.startsWith('/generate/')) {
        return sendJson(res, 200, {
          seed: url.searchParams.get('seed') ?? null,
          count: 0,
          items: [],
          warning: "Mode offline: dataset non embarqué pour ce type.",
        });
      }

      return sendJson(res, 404, { error: `Route introuvable: ${p}` });
    } catch (e) {
      return sendJson(res, 500, { error: 'Erreur serveur offline', details: String(e) });
    }
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(port, () => resolve({ port, close: () => server.close() }));
  });
}

module.exports = { startLocalApi };