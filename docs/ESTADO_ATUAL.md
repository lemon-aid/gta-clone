# Estado Visual e Funcional — Avaliação em 2026-05-30

## `nolan-city-playable.html` — O que está funcionando

### ✅ Funcionando perfeitamente
- **Tela inicial** — "Nolan City" com botão "Jogar", fundo roxo escuro, visual limpo
- **Movimento do personagem** — WASD responsivo, câmera segue suavemente
- **Câmera com follow** — centraliza no player, revelando o mundo ao redor
- **Mapa da cidade** — ruas, calçadas, faixas de pedestre, semáforos, parque verde
- **Edifícios** — fachadas coloridas e distintas (discoteca neon, banco, loja, delegacia, etc.)
- **NPCs** — personagens espalhados pelo mapa com sprites bem distintos
- **Veículos** — carros nas ruas (táxi amarelo, carro azul, verde, polícia)
- **HUD topo-esquerda** — coração + HP (100), dinheiro ($12.840), estrelas de procurado (3 estrelas)
- **Painel de missão** — "Fuga da Cidade" com descrição e checklist de objetivos
- **Minimapa circular** — canto superior esquerdo, mostra o layout da cidade
- **Rádio** — "Radio Los Santos / Synthwave 88.3 FM" no rodapé
- **Controles touch** — joystick (baixo-esquerda) e botões A/B/X/Y (baixo-direita)
- **Pause / Settings** — ícones visíveis no canto superior direito
- **Zero erros no console**

### ⚠️ Não testado ainda
- Entrar em veículos (tecla E ou F)
- Diálogos com NPCs (interação)
- Sistema de missões (completar objetivos)
- Painel de pause
- Comportamento das estrelas de procurado

### 🔴 Problemas visíveis
- Nenhum identificado visualmente nesta sessão

---

## `gta2d.html` — Não testado ainda
- Engine mais completa com armas, missões, IA de polícia
- A ser avaliado em próxima sessão

---

## Impressão geral
O `nolan-city-playable.html` está **muito polido visualmente**. Os assets gerados por IA ficaram bem, a paleta de cores é coesa (midnight neon), e o gameplay básico de movimentação funciona. É claramente o protótipo mais pronto para ser expandido.

A decisão principal que resta: **usar o `nolan-city-playable.html` como base e trazer mecânicas do `gta2d.html`**, ou manter dois arquivos separados com propósitos distintos.
