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

- Índices `0-7`: variações do piso laranja; desenhar na camada de terreno.
- Índices `8-15`: máquinas de arcade; objetos sólidos com interação pela frente.
- Índices `16-19`: balcão azul em U, dividido em quatro quadrantes de um módulo `2x2`.
- Índices `20-23`: assento, terminais e prateleira de prêmios.
- Índices `24-31`: mesa do bolo, bolos, presentes, balões e guirlandas.
- Índices `32-39`: mesas de jogos, sofá, console, doces e velas.
- Índices `40-44`: decoração suspensa; sem collider.
- Índices `45-55`: bilheteria, pipoqueira, refrigerantes, snacks, assentos e móveis adicionais.
- Índices `56-63`: pisos escuros e parede do salão.

## Regras Procedurais

1. Preencher a sala com os pisos escuros `56-58`; usar os índices `0-7` como piso laranja da área destacada da festa.
2. Colocar máquinas junto às paredes, com pelo menos um tile caminhável livre na frente.
3. Não encostar duas máquinas no mesmo ponto de interação.
4. Montar o balcão em U como um bloco fixo `2x2`: `16,17` na linha superior e `18,19` na linha inferior.
5. A abertura original do U fica voltada para cima; preservar essa orientação e posicionar a área de atendimento diante dela.
6. Manter pelo menos dois tiles livres diante do balcão para fila e conversa com atendente.
7. Usar collider nos índices `8-29` e `32-37`, conforme o manifesto.
8. Balões, guirlandas e itens marcados como `overlay-no-collision` devem ficar na camada superior e nunca bloquear o jogador.
9. A mesa do bolo (`24`) deve ficar em uma área aberta, com caminho livre em pelo menos três lados.
10. Presentes (`27`) podem ficar próximos da mesa, mas não podem bloquear a saída ou o balcão.
11. A entrada da loja deve permanecer conectada ao balcão e à área da festa por caminhos de pelo menos um tile de largura.
12. Pipoqueira (`46`) e refrigerantes (`47`) devem ficar lado a lado, sobre piso caminhável e com um tile livre diante de cada interação.
13. A bilheteria (`45`) funciona como ponto de serviço separado do balcão em U e precisa de acesso frontal livre.
14. Pipoca e bebidas nunca podem ser colocadas diretamente no piso. Usar `48` para mesa vermelha com pipoca e `49` para mesa amarela com bebidas.
15. Os índices `51-52` são as mesmas mesas sem itens e podem receber outros overlays de comida ou prêmios.

## Camadas Recomendadas

1. `terrain`: piso, parede e carpete.
2. `objects_back`: máquinas, balcão, mesas e presentes.
3. `characters`: jogador, atendente e convidados.
4. `objects_front`: partes frontais que devem cobrir os pés do personagem.
5. `overlays`: balões, guirlandas, luzes e efeitos.

Todos os objetos devem usar âncora inferior central, exceto terrenos e overlays suspensos.
