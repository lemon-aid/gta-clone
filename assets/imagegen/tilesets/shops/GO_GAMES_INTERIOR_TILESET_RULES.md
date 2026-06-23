# Go Games Interior Tileset

## Arquivos

- `go_games_interior_tileset.png`: atlas RGBA de 512x512.
- `go_games_interior_tileset.manifest.json`: índice de cada célula e comportamento.
- `go_games_interior_preview.png`: exemplo de composição, não deve ser carregado como tileset.

## Grade

- Célula: 64x64 px.
- Grade: 8 colunas por 8 linhas.
- Índice: `index = row * 8 + column`.
- Origem: canto superior esquerdo.

## Organização

- Índices `0-7`: pisos, paredes e carpetes; desenhar na camada de terreno.
- Índices `8-15`: máquinas de arcade; objetos sólidos com interação pela frente.
- Índices `16-23`: balcão, caixa, terminal e prateleira de prêmios.
- Índices `24-31`: mesa do bolo, bolos, presentes, balões e guirlandas.
- Índices `32-39`: mesas de jogos, sofá, console, doces e velas.
- Índices `40-44`: decoração suspensa; sem collider.
- Índices `56-63`: cópias dos terrenos para facilitar o editor.

## Regras Procedurais

1. Preencher toda a sala com um terreno dos índices `0-7` antes de colocar objetos.
2. Colocar máquinas junto às paredes, com pelo menos um tile caminhável livre na frente.
3. Não encostar duas máquinas no mesmo ponto de interação.
4. Montar o balcão com módulos consecutivos `16-20`; o índice `20` é o caixa/interação.
5. Manter pelo menos dois tiles livres diante do caixa para fila e conversa com atendente.
6. Usar collider nos índices `8-29` e `32-37`, conforme o manifesto.
7. Balões, guirlandas e itens marcados como `overlay-no-collision` devem ficar na camada superior e nunca bloquear o jogador.
8. A mesa do bolo (`24`) deve ficar em uma área aberta, com caminho livre em pelo menos três lados.
9. Presentes (`27`) podem ficar próximos da mesa, mas não podem bloquear a saída ou o balcão.
10. A entrada da loja deve permanecer conectada ao balcão e à área da festa por caminhos de pelo menos um tile de largura.

## Camadas Recomendadas

1. `terrain`: piso, parede e carpete.
2. `objects_back`: máquinas, balcão, mesas e presentes.
3. `characters`: jogador, atendente e convidados.
4. `objects_front`: partes frontais que devem cobrir os pés do personagem.
5. `overlays`: balões, guirlandas, luzes e efeitos.

Todos os objetos devem usar âncora inferior central, exceto terrenos e overlays suspensos.
