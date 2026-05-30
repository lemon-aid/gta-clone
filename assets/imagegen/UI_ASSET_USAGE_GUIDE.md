# Guia De Uso Dos Assets De UI

Este guia define como usar os spritesheets de UI gerados para o jogo top-down 2D.

## Arquivos

Todos os sheets estão em:

`GTA clone/assets/imagegen/ui`

Arquivos principais:

- `touch_controls_sheet.png`
- `hud_status_mission_sheet.png`
- `inventory_items_sheet.png`
- `panels_slots_frames_sheet.png`

Cada sheet tem:

- tamanho `256x256`;
- grid `4x4`;
- célula `64x64`;
- PNG `RGBA`;
- fundo transparente real.

## Indexação Padrão

Cada célula deve ser acessada por índice `0..15`.

```ts
const UI_CELL_SIZE = 64;

function getCellRect(index: number) {
  return {
    x: (index % 4) * 64,
    y: Math.floor(index / 4) * 64,
    width: 64,
    height: 64
  };
}
```

## Touch Controls Sheet

Arquivo:

`ui/touch_controls_sheet.png`

Índices:

| Índice | Elemento |
|---:|---|
| 0 | joystick outer ring |
| 1 | joystick inner knob |
| 2 | up arrow button |
| 3 | down arrow button |
| 4 | left arrow button |
| 5 | right arrow button |
| 6 | A button |
| 7 | B button |
| 8 | X button |
| 9 | Y button |
| 10 | pause button |
| 11 | play button |
| 12 | mouse icon |
| 13 | keyboard directional cluster |
| 14 | touch tap icon |
| 15 | settings gear |

Uso recomendado:

- Mobile:
  - joystick no canto inferior esquerdo;
  - botões `A/B/X/Y` no canto inferior direito;
  - pause/settings no topo direito.
- Desktop:
  - esconder joystick e botões grandes por padrão;
  - usar teclado/mouse apenas em tela de controles ou tutorial.
- Não desenhar controles dentro do mundo. Eles são camada de HUD.
- Manter escala estável. Recomendado: `64x64` a `96x96` conforme tela.
- Para joystick:
  - base usa índice `0`;
  - knob usa índice `1`;
  - knob pode se mover dentro de um raio limitado, mas a base fica fixa.

## HUD Status And Mission Sheet

Arquivo:

`ui/hud_status_mission_sheet.png`

Índices:

| Índice | Elemento |
|---:|---|
| 0 | heart health |
| 1 | wanted star active |
| 2 | wanted star empty |
| 3 | cash stack |
| 4 | coin |
| 5 | weapon/ammo |
| 6 | map pin objective |
| 7 | exclamation mission marker |
| 8 | checkmark complete |
| 9 | skull danger |
| 10 | radio/music note |
| 11 | minimap player arrow |
| 12 | police badge |
| 13 | car/garage icon |
| 14 | magic explosion/effect |
| 15 | reward gift |

Uso recomendado:

- Vida:
  - ícone `0` próximo ao valor numérico de HP.
- Dinheiro:
  - ícone `3` ou `4` próximo ao contador de dinheiro.
- Wanted level:
  - desenhar cinco ícones em linha;
  - usar índice `1` para estrela ativa;
  - usar índice `2` para estrela vazia.
- Missão:
  - usar índice `6` para objetivo no HUD/minimapa;
  - usar índice `7` para missão disponível;
  - usar índice `8` para objetivo concluído.
- Minimap:
  - player arrow usa índice `11`;
  - o aro/mapa em si deve ser desenhado por código ou frame separado.

## Inventory Items Sheet

Arquivo:

`ui/inventory_items_sheet.png`

Índices:

| Índice | Elemento |
|---:|---|
| 0 | blaster/weapon |
| 1 | health kit |
| 2 | star token |
| 3 | burger |
| 4 | energy potion |
| 5 | magic wand |
| 6 | fuel bottle |
| 7 | cash bundle |
| 8 | wooden bat |
| 9 | key card |
| 10 | police radio |
| 11 | neon gem |
| 12 | backpack |
| 13 | car key fob |
| 14 | donut |
| 15 | shield pickup |

Uso recomendado:

- Itens do inventário devem ser desenhados dentro de slots do `panels_slots_frames_sheet.png`.
- Item não deve carregar o fundo do slot.
- Quantidades, cooldowns e seleção devem ser desenhados por código.
- Não editar o PNG para incluir números.
- Itens coletáveis no mundo podem reutilizar esses sprites, mas devem ser escalados com cuidado:
  - mundo: `32x32` a `48x48`;
  - inventário/HUD: `48x48` a `64x64`.

## Panels, Slots And Frames Sheet

Arquivo:

`ui/panels_slots_frames_sheet.png`

Índices:

| Índice | Elemento |
|---:|---|
| 0 | empty inventory slot |
| 1 | selected inventory slot |
| 2 | locked slot |
| 3 | reward/chest slot frame |
| 4 | small nameplate |
| 5 | dialog bubble frame |
| 6 | mission objective card |
| 7 | minimap circular rim |
| 8 | radial menu segment |
| 9 | square cyan button frame |
| 10 | square purple button frame |
| 11 | pill tab frame |
| 12 | warning badge frame |
| 13 | shop/item card frame |
| 14 | quest checkbox frame |
| 15 | bottom menu tile frame |

Uso recomendado:

- Slots:
  - índice `0`: slot vazio;
  - índice `1`: slot selecionado;
  - índice `2`: slot bloqueado.
- Missão:
  - índice `6` pode ser usado como base compacta para objetivo atual.
- Diálogo:
  - índice `4` para nome do personagem;
  - índice `5` para balão/caixa de diálogo.
- Minimap:
  - índice `7` é aro circular;
  - conteúdo do mapa deve ser renderizado por código dentro do aro.
- Botões:
  - índice `9` e `10` são frames de botão genéricos.

## Camadas De Renderização Da UI

Renderizar UI acima do mundo nesta ordem:

1. Gameplay/world.
2. Overlays de mundo, se houver.
3. Painéis escuros/translúcidos desenhados por código.
4. Frames/slots dos spritesheets.
5. Ícones.
6. Texto dinâmico.
7. Cursor/toque/foco.

Texto deve ser sempre renderizado por código, não embutido nos sprites.

## Escala E Responsividade

Regras:

- Nunca distorcer sprites de UI em eixos diferentes.
- Se aumentar, usar escala uniforme.
- Manter padding mínimo de `16px` da borda da tela.
- Em telas pequenas, reduzir opacidade/tamanho dos controles, mas manter área de toque.
- Área mínima de toque recomendada: `56x56`.
- Ícone visual pode ter `48x48`, mas o hitbox deve ter pelo menos `56x56`.

## Layout HUD Recomendado

### Canto Superior Esquerdo

- Vida.
- Dinheiro.
- Wanted level.

### Canto Superior Direito

- Pause.
- Settings.
- Objetivo atual compacto.

### Canto Inferior Esquerdo

- Joystick mobile.

### Canto Inferior Direito

- Botões `A/B/X/Y`.

### Lateral Direita Ou Inferior

- Inventário rápido com 4 a 8 slots.
- O inventário rápido deve ficar oculto por padrão.
- Mostrar o inventário apenas depois que o usuário abrir o menu e clicar em `Inventário`.
- Não deixar o painel de inventário sempre aberto durante gameplay, para não cobrir o mapa.

### Minimap

- Canto superior esquerdo ou inferior esquerdo.
- Não cobrir NPCs importantes ou carros em perseguição.

## Regras De Interação

- Botões devem ter estados:
  - normal;
  - pressed;
  - disabled;
  - highlighted.
- Como só existe um sprite base, estados podem ser feitos por código:
  - `pressed`: reduzir escala para `0.94`;
  - `disabled`: aplicar alpha `0.45`;
  - `highlighted`: adicionar contorno/glow por shader/canvas.
- Inventário selecionado deve usar slot índice `1`.
- Itens bloqueados devem usar slot índice `2`.
- O botão de configurações/menu pode abrir um painel pequeno com a opção `Inventário`.
- Ao clicar em `Inventário`, alternar visibilidade do painel de inventário.

## Overlays De Mundo Versus UI

Não confundir:

- UI HUD: fica fixo na tela.
- Overlay de mundo: fica ancorado em coordenadas do mapa.

Exemplos de overlay de mundo:

- semáforo;
- poste;
- luz;
- placa;
- marcador de missão acima de NPC;
- ícone de interação.

Exemplos de UI HUD:

- botão A/B/X/Y;
- vida;
- dinheiro;
- inventário;
- pause;
- minimap;
- objetivo atual.

## Exemplo De Tipos

```ts
type UISheetId =
  | "touch_controls"
  | "hud_status_mission"
  | "inventory_items"
  | "panels_slots_frames";

type UIElement = {
  sheet: UISheetId;
  index: number;
  x: number;
  y: number;
  scale: number;
  anchor: "top-left" | "top-right" | "bottom-left" | "bottom-right" | "center";
  opacity?: number;
  interactive?: boolean;
  action?: string;
};
```

## Exemplo Atual

Exemplo composto:

- `GTA clone/assets/imagegen/examples/game_ui_final_example.png`
- `GTA clone/assets/imagegen/examples/game_ui_final_example.layout.json`

O exemplo usa o chunk mais recente como fundo e sobrepõe HUD, controles, inventário e missão.

## Próximos Assets Recomendados

Para uma UI mais completa, ainda vale gerar:

- painel largo de missão em `256x96` ou `384x128`;
- caixa de diálogo nativa em `512x160`;
- minimap frame maior em `128x128`;
- variações pressed/disabled dos botões;
- barra de vida horizontal;
- barra de energia/stamina;
- ícones de ação contextuais: entrar no carro, falar, roubar, comprar, coletar.
