# Decisões do Projeto — Log Cronológico

> Cada vez que decidirmos algo, mudarmos de ideia, ou resolvermos um debate, entra aqui com data.
> Formato: `## YYYY-MM-DD — Título da decisão`

---

## 2026-05-30 — Setup inicial e reconhecimento

**Contexto:** Primeira sessão. Agente leu o projeto completo.

**Decisões:**
1. Criar pasta `docs/` como cérebro do projeto — toda decisão vai aqui
2. O projeto tem dois HTMLs distintos: `nolan-city-playable.html` (protótipo polido) e `gta2d.html` (engine completa)
3. Não criar do zero — evoluir em cima do que existe

**Próxima sessão deve responder:**
- Qual HTML vira o arquivo principal?
- Merge dos dois ou escolher um?

---

## 2026-05-30 — Avaliação visual do nolan-city-playable.html

**Contexto:** Servidor Python rodando em http://localhost:3030. Jogo aberto no Chrome e testado manualmente.

**O que foi observado:**
- Jogo completamente funcional: movimento, câmera, HUD, minimapa, missão ativa, NPCs, veículos, rádio, controles touch
- Visual muito polido — paleta midnight neon coesa, sprites gerados por IA com boa qualidade
- Zero erros no console

**Conclusão provisória:**
- `nolan-city-playable.html` = **base principal de desenvolvimento** — mais polido visualmente
- `gta2d.html` = **referência de mecânicas** — armas, missões, IA de polícia

**Pendente para próxima sessão:**
- Testar `gta2d.html` visualmente
- Decidir: merge ou dois arquivos?
- Testar interações (NPCs, veículos, missões) no nolan-city

---

## 2026-05-30 — Repositório no GitHub + 6 features grandes

**Repositório criado:** https://github.com/lemon-aid/gta-clone (branch master).
`nolan-city-playable.html` confirmado como **arquivo principal de desenvolvimento**.

**Features implementadas (todas em nolan-city-playable.html):**

1. **Dinheiro inicial = $2.000** (antes $12.840). HUD agora atualiza dinâmico via `updateHUD()`.

2. **Sistema de loja (shop)** — ao chegar perto da entrada de um prédio-loja e apertar E,
   abre overlay fullscreen com fundo gradiente + retrato do NPC vendedor + menu de itens
   (comprar via UI). Lojas: store (Sara), cafe (Bia), mechanic (Rato), flower (Lis),
   hospital (Dra. Ana), arcade (Zé). Itens curam HP / cosméticos. Fecha com botão Sair ou Esc.
   - `SHOPS` define cada loja; `openShop()`/`buyItem()`/`closeShop()`.

3. **Quests + conversa com NPCs** — 9 NPCs com nomes próprios (Luna, Mia, Dani, Niko, Theo,
   Bit, Rui, Cláudia, Vince) e falas curtas multi-linha (avança com E/clique).
   Sistema de quest sequencial: Primeiro Contato → Mãos ao Volante → Test Drive → Primeiras Compras.
   Cada quest dá recompensa em dinheiro. `QUESTS[]`, `questEvent()`, `questDrive()`, `completeQuest()`.

4. **Física de carro com freio e ré** — carro agora tem velocidade/momentum (inércia).
   - Acelera com WASD/setas/joystick.
   - **Freio: H (teclado) / B (controle)** — desaceleração forte.
   - **Ré: K (teclado) / Y (controle)** — anda pra trás mantendo a frente virada.
   - Colisão do carro com prédios/props via `carBlocked()`.

5. **Save/Load** — `localStorage` chave `nolan_city_save_v1`. Botões "Salvar Jogo" e
   "Carregar Jogo" no menu da engrenagem (settings). Salva player, carros, quest.

**Validação:** testado via JS no browser — quest avança e paga recompensa, loja abre/compra/cura,
carro acelera/freia/dá ré, save/load restaura estado. Zero erros no console.

**Notas técnicas:**
- O arquivo NÃO tem cache-busting. Ao editar, abrir com `?v=N` no fim da URL pra evitar cache.
- Botão Y de toque agora está ligado (era inerte antes) → usado pra ré.
- Botão B de toque (touch.b) agora usado pra freio.

**Pendente / próximas ideias:**
- Sistema de HP do carro / dano em colisão
- Combustível?
- NPCs andando sozinhos (IA simples)
- Mais quests com objetivos espaciais (ir a um local)
- Trazer combate/armas do gta2d.html

---

## 2026-05-30 — Regra: carros só na estrada + mão única

**Regra de design definida pelo usuário:**
- Carros (NPC e jogador) **NÃO podem andar fora da estrada**.
- Cada rua tem uma **mão** (direção). Os NPCs sempre seguem a mão da sua via.
- **Apenas o carro do jogador pode andar na contramão.**

**Como o mapa funciona (importante p/ entender):**
- Vias horizontais em pares: rows [5,6], [15,16], [25,26]. No par, a 1ª row é mão 'right',
  a 2ª é 'left' (faixa de duas mãos = duas "ruas" de mão única lado a lado).
- Vias verticais em pares: cols [8,9], [22,23], [35,36]. 1ª col 'down', 2ª col 'up'.
- As vias são contínuas de ponta a ponta do mapa. `map.lanes` guarda a mão de cada tile.

**Mudanças feitas:**
1. `carBlocked()` agora exige que os 4 cantos do carro estejam sobre tiles de **estrada**
   (`isRoad`). Isso prende o carro do jogador na via — não invade calçada/grama/prédio.
   O jogador AINDA pode ir na contramão (não há checagem de direção, só de estrada).
2. **Bug corrigido:** o loop de tráfego no topo do `update()` movia TODOS os carros (incl. o
   do jogador) por `c.dir` sem checar estrada e com wrap-around → o carro do jogador era movido
   2x e saía da pista. Agora `if(c===player.inCar)continue;` exclui o carro do jogador desse loop.
3. NPCs nascem já com a `dir` correta da mão da via + vias contínuas → nunca saem da estrada
   nem andam na contramão. (Tentei derivar a mão por `laneAt` a cada frame, mas isso fazia o
   NPC virar nos cruzamentos — revertido.)

**Validado:** carro do jogador para nas bordas da via (y=4.8/6.2 na faixa 5-6), anda na
contramão (esquerda numa via 'right'), e os 5 NPCs seguem na estrada após 400 frames.

---

## 2026-05-30 — Autonomia total + cache-busting de assets

**Decisão do usuário:** autonomia total no projeto GTA clone — nunca pedir permissão
(editar, commitar, push, rodar). Registrado também na memória persistente.

**Sprites atualizados:** o usuário corrigiu a transparência de 2 sprites (mesmos nomes de arquivo):
- `assets/imagegen/cars/black_blue_police_cruiser_imagegen.png` (polícia)
- `assets/imagegen/cars/white_cyan_ambulance_van_imagegen.png` (ambulância)

Como os nomes não mudaram, o navegador servia a versão antiga em cache.

**Solução — cache-busting de assets:** adicionado `const ASSET_VER` + função `cb(src)` que anexa
`?v=N`. Aplicado em `loadImage`, `uiBg` e `setKeeperPortrait`. **Ao trocar/atualizar qualquer
sprite PNG mantendo o nome, incrementar `ASSET_VER`** para forçar o reload.

**Validado:** as 2 sprites novas carregam (256×256, cantos com alpha=0 = transparente correto,
centro opaco) e renderizam limpas no jogo. Zero erros no console.

---

## 2026-05-30 — Correção: carros NPC saindo da pista

**Sintoma:** carros NPC apareciam andando fora das pistas (na calçada/quadras).

**Causa raiz:** ao entrar num carro NPC, dirigir e SAIR em outro lugar, o carro ficava fora da
sua pista original. A IA de tráfego então retomava o movimento na `dir` fixa a partir dessa
posição errada → atravessava a calçada. Os campos `path`/`lane` existiam mas não eram usados.

**Correção (2 partes):**
1. **Trava de pista:** no loop de tráfego, `if(c.path==='h')c.y=c.lane; else if(c.path==='v')c.x=c.lane;`
   antes de mover. Como toda lane é uma via contínua, o NPC nunca sai da rua — e qualquer carro
   deslocado é puxado de volta à pista no frame seguinte.
2. **Carro estacionado:** ao sair do carro, `c.parked=true`. Carros estacionados não voltam a
   patrulhar (ficam parados onde foram deixados, sempre numa rua). `parked` persiste no save/load.

**Validado:** carro deslocado p/ calçada (y=10) volta à pista (y=6) em 1 frame; todos os 6 NPCs
na estrada após 300 frames; carro estacionado não se move.

---

## 2026-05-30 — Menu unificado, inventário, party, procurado

Substituído o menu/inventário mockado (não funcionava) por um sistema completo.

**Menu overlay (`#menu`)** com 4 abas, aberto pela engrenagem ou tecla **M** (Esc fecha):
- **Inventário** — lista itens com ícone, qtd e botão "Usar". Remédios (heal>0) curam HP.
  Itens começam com 2 Refrigerantes + 1 Kit Médico. Compras nas lojas agora vão para o
  inventário (antes curavam na hora).
- **Missões** — lista TODAS as quests com badge de status (Concluída/Ativa/Bloqueada) e
  filtro (Todas/Ativas/Concluídas). Status derivado de `questIndex`.
- **Procurado** — mostra 0–5 estrelas + descrição do nível.
- **Party** — 4 membros (Nico/boy, Mia/girl, Luna/hacker, Theo/skate) com retrato, barra de HP
  e botão Ativar. Salvar/Carregar/Fechar no rodapé.

**Sistema de Party:** `PARTY[]` + `activeMember`. O personagem ativo é quem anda no mapa
(sprite via `activeChar().kind`). HP do ativo vive em `player.hp`; ao trocar, o HP é guardado
no membro e o do novo é carregado. Troca rápida pelas **teclas 1–4** ou botão Ativar.

**Sistema de Procurado (novo):** `player.wanted` 0–5.
- Ganha: entrar num carro em patrulha = roubo → +1 (carro estacionado pelo jogador não conta).
- Decai: 1 estrela a cada 18s a pé sem crimes.
- HUD e aba Procurado refletem o nível.

**Save/Load:** agora persiste inventory, HP de cada membro da party e activeMember.

**Removido:** painéis `#inventory` (inventário rápido mockado) e `#menuPanel`.

**Validado:** trocar p/ Mia muda sprite; refrigerante cura +15 e decrementa qtd; roubar carro
em patrulha dá +1 procurado e ao sair fica parked; filtros de missão funcionam; 4 abas renderizam.
Zero erros no console.

---

## 2026-05-31 — Garagem: carro ativo, comprar/vender, setinha no mapa

Adicionada aba **Carros** no menu (5ª aba).

**Modelo:** `CAR_CATALOG` (6 modelos compráveis: Compacto Azul, Hatch Verde, Táxi, Van,
Ambulância, Viatura), `ownedCars[]` (garagem; começa com 1 Compacto Azul) e `activeCarIdx`.
Um objeto único `myCar` (sempre `parked:true`, `owned:true`) é empurrado em `cars[]` e só
aparece quando `myCar.active`.

**Aba Carros:**
- "Meus Carros" — cada carro com retrato, Ativar (define ativo) e Vender (50% do preço de volta;
  não deixa vender o último).
- "Loja de Carros" — catálogo com preço e Comprar (debita o dinheiro).

**Carro ativo no mapa:** ao Ativar, `myCar` spawna no tile de rua mais próximo do player
(`nearestRoadTile`), parado, com uma **setinha amarela** desenhada por cima (`drawCarArrow`,
balança com sin do tempo). Entrar nele dá toast "Entrou no seu carro" e **não gera procurado**
(porque `parked` → `roubo=false`). NPCs nunca patrulham o myCar (parked é pulado no loop).

**Guards:** `nearestCar` e o loop de desenho pulam `myCar` quando `!active`.

**Save/Load:** persiste `ownedCars`, `activeCarIdx` e `myCar.kind/active`.

**Validado:** aba renderiza meus carros + loja; ativar coloca o carro com setinha na rua; usar
o carro próprio mantém procurado em 0; comprar Táxi (-$1800) e vender (+$900 = 50%) corretos.
Zero erros no console.
