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
