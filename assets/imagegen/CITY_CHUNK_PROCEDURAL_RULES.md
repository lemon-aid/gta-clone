# Regras Procedurais Para Chunks Da Cidade

Este documento define como usar os sprites gerados para montar chunks jogáveis da cidade. Ele deve ser seguido pela IA/agente que estiver codando o jogo.

## Objetivo

Gerar chunks top-down 2D com:

- ruas sempre conectadas;
- tráfego coerente;
- carros no sentido correto;
- prédios próximos das ruas, mas separados por calçada;
- overlays como semáforos/luzes sem ocupar tiles de terreno;
- parques, props e NPCs posicionados em áreas válidas;
- uso consistente dos sprites já gerados.

## Tamanho Base

- Tile base: `64x64`.
- Chunks recomendados: múltiplos de `64`.
- Exemplo atual: `20x14` tiles = `1280x896`.
- Todos os posicionamentos devem ser feitos em coordenadas de tile, com offset em pixels apenas para overlays pequenos.

## Pastas De Assets

Use estes diretórios:

- Pessoas: `GTA clone/assets/imagegen/people`
- Carros: `GTA clone/assets/imagegen/cars`
- UI: `GTA clone/assets/imagegen/ui`
- Tilesets: `GTA clone/assets/imagegen/tilesets`
- Exemplos: `GTA clone/assets/imagegen/examples`

## Spritesheets De Personagens

Cada personagem usa sheet `256x256`, grid `4x4`, frame `64x64`.

Ordem das linhas:

1. `Down`
2. `Left`
3. `Right`
4. `Up`

Ordem das colunas:

1. `Idle`
2. `Step Left`
3. `Idle`
4. `Step Right`

Regras:

- Use personagens somente em calçadas, parques, praças, entradas de prédios ou áreas pedonais.
- Nunca coloque NPC em faixa ativa de rua.
- Personagens devem estar centralizados no tile ou levemente deslocados dentro de calçada/praça.
- Para NPC parado, use coluna `0` ou `2`.
- Para caminhada, alterne colunas `0,1,2,3`.
- Não redimensione personagens.

## Spritesheets De Carros

Cada carro usa sheet `256x256`, grid `4x4`, frame `64x64`.

Ordem esperada das linhas:

1. `Down`
2. `Left`
3. `Right`
4. `Up`

Regras:

- Carros devem estar sempre em uma faixa válida.
- Carros devem apontar na direção da faixa.
- Carros não devem ficar centralizados na rua inteira; devem ficar centralizados na faixa.
- Ruas de duas mãos devem ter ao menos duas faixas lado a lado.
- Carros estacionados devem ficar apenas em vagas, acostamento/parking tile ou estacionamento.
- Não coloque carro atravessado em cruzamento, exceto para eventos/colisão planejados.

### Asset Problemático

O arquivo abaixo está com direções incorretas e não deve ser usado até ser refeito:

- `GTA clone/assets/imagegen/cars/red_neon_sports_car_imagegen.png`

Problema: a linha que deveria representar `Right` ainda renderiza visualmente como carro vertical. Regerar este spritesheet antes de usar no tráfego.

## Modelo De Rua

Use ruas de duas faixas como padrão.

Modelo recomendado:

- Estrada horizontal:
  - tile/faixa superior: sentido `Right`
  - tile/faixa inferior: sentido `Left`
- Estrada vertical:
  - tile/faixa esquerda: sentido `Down`
  - tile/faixa direita: sentido `Up`

Exemplo:

```json
{
  "lane_rules": {
    "horizontal_top_lane": "right",
    "horizontal_bottom_lane": "left",
    "vertical_left_lane": "down",
    "vertical_right_lane": "up"
  }
}
```

Regras:

- Não desenhe setas no chão para indicar direção. Direção é metadado do grafo/path.
- Use linhas centrais ou marcas discretas se necessário, mas sem setas.
- Toda rua deve pertencer a um grafo conectado.
- Evite ruas isoladas ou fragmentos que não levam a lugar nenhum.
- Cada corredor de rua deve comportar dois carros lado a lado, um por sentido.
- Cruzamentos devem conectar as faixas sem quebrar continuidade.
- Crosswalks devem atravessar a largura inteira da rua e ligar calçada a calçada.

## Grafo Procedural De Ruas

Antes de posicionar sprites, gere uma estrutura lógica:

```ts
type Direction = "up" | "down" | "left" | "right";

type RoadLane = {
  tileX: number;
  tileY: number;
  direction: Direction;
  roadId: string;
};

type RoadNode = {
  tileX: number;
  tileY: number;
  openEdges: Array<"N" | "S" | "E" | "W">;
};
```

Validação obrigatória:

- Toda rua conectada precisa ter vizinho compatível.
- Se um tile abre para `E`, o vizinho à direita deve abrir para `W`.
- Se um tile abre para `N`, o vizinho acima deve abrir para `S`.
- Não posicionar carro em tile sem `RoadLane`.
- Não posicionar prédio em tile de rua.

Pseudocódigo:

```ts
for (const roadTile of roadTiles) {
  for (const edge of roadTile.openEdges) {
    const neighbor = getNeighbor(roadTile, edge);
    assert(neighbor && neighbor.openEdges.includes(opposite(edge)));
  }
}

for (const car of cars) {
  const lane = laneAt(car.tileX, car.tileY);
  assert(lane);
  assert(car.direction === lane.direction);
}
```

## Calçadas E Pavimento

Regra principal:

- Todo prédio deve estar separado da rua por pelo menos `1 tile` completo de calçada/pavimento.

Isso significa:

```text
[PREDIO] [CALCADA/PAVIMENTO] [RUA]
```

Não usar:

```text
[PREDIO] [RUA]
```

Regras:

- Calçadas devem formar faixas contínuas ao longo das ruas.
- Entradas de prédios devem apontar para calçada, praça ou pavimento, nunca direto para asfalto.
- O pavimento do quarteirão pode ser usado como área pedonal.
- O pavimento próximo à rua deve ter borda/curb visível.

## Prédios

Os sprites atuais de prédios são bons como fachadas pequenas, mas são pequenos para edifícios principais.

Regras:

- Não esticar sprites de prédios. Evitar scaling não uniforme.
- Se precisar de prédio grande, usar módulos nativos maiores ou compor vários sprites lado a lado.
- Prédios devem ficar próximos da rua, com exatamente `1 tile` de calçada quando possível.
- Prédios importantes devem ser módulos maiores:
  - café: `2x1` ou `2x2`;
  - hospital: `2x2` ou maior;
  - polícia: `2x2` ou maior;
  - estacionamento/garagem: `2x2` ou maior;
  - prédio comercial: `2x2`, `3x2` ou maior.
- Não colocar prédios soltos em grandes vazios de pavimento.
- Prefira formar quarteirões com fachadas alinhadas.

Recomendação importante:

- Gerar novos assets de prédios em módulos nativos `2x2`, `3x2` e `4x2`. Os sprites atuais de fachada `64x64` são pequenos demais para uma cidade mais convincente.

## Estacionamento

Regra:

- A vaga deve ser dimensionada pelo maior carro disponível.

No exemplo atual:

- maior bbox de carro detectado: `56x64`;
- vaga usada: `70x78`.

Procedimento:

```ts
slotWidth = maxCarBBoxWidth + paddingX;
slotHeight = maxCarBBoxHeight + paddingY;
paddingX >= 14;
paddingY >= 14;
```

Regras:

- Estacionamento deve ter entrada/saída conectada à rua por driveway.
- Vagas não devem ser menores que o maior carro.
- Carros estacionados devem respeitar a orientação da vaga.
- Parking garage deve ter ligação visual/lógica com o estacionamento ou driveway.

## Parques E Grama

Regras:

- Parques devem ocupar blocos claros, não tiles aleatórios.
- Grama precisa de transição/borda para pavimento.
- Evite retângulos crus de grama contra pavimento.
- Use tiles de borda:
  - grama centro;
  - grama borda superior;
  - grama borda inferior;
  - grama borda esquerda;
  - grama borda direita;
  - cantos de grama.
- Props de parque ficam dentro de parque/praça:
  - árvores;
  - bancos;
  - fonte;
  - arbustos;
  - mesas.

## Props E Overlays

Divida em dois tipos:

### Props De Tile

Ocupam ou dominam um tile `64x64`.

Exemplos:

- árvores grandes;
- fonte;
- banco;
- mesa;
- arbusto;
- caixa/lixeira grande.

Regras:

- Devem ficar em calçadas, parques, praças ou áreas de estacionamento.
- Não colocar em faixa ativa de rua.
- Podem bloquear caminhada se marcados como colisão.

### Overlays Pequenos

Não ocupam um tile inteiro. São desenhados com offset em pixels.

Exemplos:

- semáforo;
- placa pequena;
- poste fino;
- luz;
- hidrante;
- medidor de estacionamento;
- pequenos cones;
- brilhos/neon decorativos.

Regras:

- Overlays ficam ancorados em cantos, bordas de calçada ou curb.
- Semáforo deve ficar no canto do cruzamento, nunca no centro de um tile vazio.
- Semáforo não deve consumir um tile inteiro.
- Luzes e postes podem ficar entre tiles, com offsets.
- Overlays não devem bloquear a faixa do carro.
- Se tiver colisão, usar hitbox menor que o sprite visual.

Exemplo de overlay:

```ts
type Overlay = {
  spriteId: string;
  tileX: number;
  tileY: number;
  offsetX: number;
  offsetY: number;
  anchor: "curb" | "corner" | "sidewalk" | "park";
  blocksCars: false;
  blocksPedestrians?: boolean;
};
```

## Ordem De Renderização

Renderizar em camadas:

1. Fundo/base.
2. Terreno: pavimento, grama, estrada.
3. Bordas/curbs/transições.
4. Marcas de rua e crosswalks.
5. Prédios.
6. Props grandes.
7. Carros.
8. Personagens/NPCs.
9. Overlays pequenos acima dos personagens se necessário.
10. UI/HUD.

## Colisão

Regras sugeridas:

- Estrada: carros podem passar, pedestres só atravessam em crosswalk ou se permitido.
- Calçada/pavimento: pedestres podem andar.
- Grama/parque: pedestres podem andar se não houver prop bloqueador.
- Prédios: bloqueiam.
- Props grandes: geralmente bloqueiam.
- Overlays pequenos: normalmente não bloqueiam carros; podem bloquear pedestres com hitbox pequena.
- Carros: bloqueiam pedestres e outros carros.

## Validação De Chunk

Antes de aceitar um chunk, rodar estas checagens:

- Todas as ruas fazem parte de um grafo conectado.
- Não há rua isolada.
- Toda rua tem largura compatível com duas faixas quando for via principal.
- Todo carro está em uma faixa válida.
- Todo carro aponta para o sentido da faixa.
- Nenhum carro usa spritesheet inválido.
- Prédios não encostam diretamente na rua.
- Todo prédio tem ao menos `1 tile` de calçada/pavimento até a rua.
- Prédios importantes têm tamanho visual adequado.
- Estacionamento tem vagas maiores que o maior carro.
- Estacionamento conecta à rua.
- Crosswalks atravessam a rua inteira.
- Semáforos são overlays em cantos de cruzamento.
- Props não bloqueiam faixas ativas.
- Grama tem borda/transição para pavimento.

## Assets Que Precisam Ser Refeitos Ou Melhorados

### Recriar

- `cars/red_neon_sports_car_imagegen.png`
  - Motivo: linhas/direções do spritesheet estão incorretas.

### Recomendado Criar

- Prédios nativos maiores:
  - café `2x2`;
  - hospital `3x2` ou `3x3`;
  - estação de polícia `3x2`;
  - estacionamento/garagem `3x2`;
  - lojas `2x1`;
  - apartamentos/escritórios `2x2`, `3x2`.

- Tiles nativos de cidade:
  - pavimento cheio;
  - pavimento com curb norte/sul/leste/oeste;
  - grama centro;
  - grama bordas;
  - grama cantos;
  - driveway;
  - estacionamento modular;
  - cruzamento 2-lane limpo sem setas.

### Recomendado Separar

- Semáforos como sprites pequenos/overlay, não tile completo.
- Postes/luzes como overlay.
- Sinais de trânsito como overlay.
- Cones podem existir em duas versões:
  - overlay pequeno;
  - obstáculo de construção.

## Exemplo Atual Mais Recente

Arquivos:

- `GTA clone/assets/imagegen/examples/city_chunk_rules_v4.png`
- `GTA clone/assets/imagegen/examples/city_chunk_rules_v4.layout.json`
- `tools/build_city_chunk_rules_v4.py`

Observações:

- O exemplo v4 já remove setas e usa semáforos como overlay.
- O carro vermelho foi removido porque o sheet está inválido.
- O estacionamento usa vaga calculada pelo maior carro.
- Os prédios não são esticados, mas ainda precisam de assets maiores nativos para ficarem visualmente melhores.
