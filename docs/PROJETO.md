# GTA Clone — Documentação do Projeto

> **Cérebro do projeto.** Toda decisão, mudança de ideia, debate e resolução fica registrada aqui.
> A cada sessão de trabalho, atualizar este arquivo com o que foi decidido/mudado.

---

## Visão Geral

Jogo top-down 2D estilo GTA clássico (GTA 1/2), rodando 100% no browser sem build step.

- **Nome provisório:** Nolan City (visto no arquivo `nolan-city-playable.html`)
- **Linguagem:** JavaScript puro + Canvas 2D API
- **Sem dependências externas** — nada de npm, bundler, framework
- **Idioma do jogo:** Português Brasileiro (pt-BR)

---

## Arquivos Principais

| Arquivo | Descrição |
|---|---|
| `gta2d.html` | Engine completa (1331 linhas) — mundo 128×128, armas, missões, IA |
| `nolan-city-playable.html` | Protótipo jogável (508 linhas) — mapa 44×32, NPCs, veículos, diálogos |
| `assets/` | Sprites, tilesets e assets gerados por IA |
| `assets/imagegen/` | Guias de geração de imagem + exemplos |
| `assets/generated/` | Assets PNG já gerados (manifest.json lista tudo) |
| `pixel art/` | Assets legados de pixel art |
| `docs/` | **Esta pasta** — cérebro do projeto |

---

## Dois Protótipos — Estado Atual

### `nolan-city-playable.html` ← **Protótipo mais polido**
- Mapa: 44×32 tiles (64px cada) = mundo 2816×2048px
- 6 veículos dirigíveis
- 9 NPCs com diálogos
- 7 edifícios interativos
- Sistema de câmera com follow suave
- Minimapa circular
- UI: status, missões, inventário, diálogos
- Assets: usa sprites gerados por IA (`assets/imagegen/`)

### `gta2d.html` ← **Engine mais completa**
- Mapa: 128×128 tiles, gerado proceduralmente
- 9 armas com mecânicas distintas
- 7 tipos de veículo com física
- IA de NPCs (civis, gangues, polícia)
- Sistema de procurado (5 estrelas)
- Framework de missões
- Save/load (localStorage)
- Áudio sintético (Web Audio API)

---

## Stack Técnica

```
- Canvas 2D API (renderização)
- Web Audio API (áudio sintético)
- localStorage (save)
- Keyboard + Mouse + Touch (input)
- Zero dependências externas
```

---

## Assets

### Tilesets
- `building_facades_96_sheet.png` — fachadas 96×96px
- `park_street_props_sheet.png` — props de parque/rua
- `roads_sidewalks_sheet.png` — estradas e calçadas
- `sidewalk_overlay_sheet.png` — overlays de calçada

### Sprites (assets/imagegen/)
**Personagens (256×256, RGBA):**
- `main_boy_imagegen.png`, `main_girl_imagegen.png`
- `hacker_girl_imagegen.png`, `food_courier_boy_imagegen.png`
- `street_magician_imagegen.png`, `skate_kid_imagegen.png`

**Carros (256×256, RGBA):**
- `yellow_taxi_imagegen.png`
- `blue_electric_compact_imagegen.png`
- `green_street_hatchback_imagegen.png`
- `black_blue_police_cruiser_imagegen.png`
- `white_cyan_ambulance_van_imagegen.png`
- `purple_delivery_van_imagegen.png`

**UI Sheets (256×256, grid 4×4, células 64×64):**
- `touch_controls_sheet.png`
- `hud_status_mission_sheet.png`
- `inventory_items_sheet.png`
- `panels_slots_frames_sheet.png`

### Regras de Assets
- Personagens: apenas calçadas, parques, entradas de edifícios
- Carros: apenas faixas válidas, direção correspondente à faixa
- Estacionamento: mínimo 70×78px por vaga
- Fachadas: 96×96px nativos (não esticar)

---

## Design Visual

**Paleta "Midnight Neon":**
- Fundo: `#1a0035`, `#0a0015` (roxo escuro/azul noite)
- Primário UI: `#ff80ff`, `#c040ff` (neon pink)
- Secundário: `#3cdeff` (cyan)
- Saúde: `#80ff80` (verde)
- Perigo/morte: `#ff4040` (vermelho)

**Estilo:**
- Neo-retro brutalista
- Grid de 4px pixel-strict
- Cantos afiados (sem arredondamento)
- Bordas 2px
- Efeito de profundidade escalonado

---

## Controles

| Input | Ação |
|---|---|
| WASD | Movimento |
| Mouse (aim) | Mirar |
| Click | Atirar |
| E/F | Interagir / Entrar em veículo |
| Shift | Correr |
| 1–9 | Slots de arma/inventário |
| R | Rádio |
| Esc | Pause |
| Touch (joystick BL) | Mover |
| Touch (botões BR) | A/B/X/Y ações |

---

## Sessões de Trabalho

### Sessão 2026-05-30 — Reconhecimento inicial
**O que foi feito:**
- Leitura completa do projeto pela primeira vez
- Mapeamento de todos os arquivos e sua função
- Identificados dois protótipos com níveis diferentes de completude
- Criada esta pasta `docs/` como cérebro do projeto

**Estado ao encerrar:**
- Projeto lido, documentado, servidor sendo iniciado
- Próximo passo: rodar e avaliar visualmente o estado atual dos dois HTMLs

**Decisões tomadas:**
- Pasta `docs/` será o único local de decisões — não usar README espalhados
- Trabalhar em cima de um dos dois protótipos, não criar do zero

---

## Perguntas Abertas / Próximas Decisões

- [ ] Qual dos dois HTMLs será o arquivo principal de desenvolvimento?
- [ ] Fundir `gta2d.html` (engine) + `nolan-city-playable.html` (polish)?
- [ ] Qual feature tem maior prioridade: mapa maior, missões, ou polish visual?
- [ ] Nome final do jogo?
