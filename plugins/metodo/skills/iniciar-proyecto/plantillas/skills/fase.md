---
name: fase
description: Implementa solo la fase n de tasks.md del spec activo, con la suite en verde, marca su casilla con el número obtenido y devuelve el resumen de seis líneas. La invoca el agente de desarrollo cuando la dirección lo lanza con «/fase n».
argument-hint: "<n>"
---

Implementa la fase $ARGUMENTS del spec activo (el que nombra `memory.md`), y solo esa.

1. **La marca.** La primera línea de `tasks.md` tiene que decir «Plan autorizado por el autor el AAAA-MM-DD». Si no lo dice, no hagas nada: dilo y para.
2. **La casilla.** Busca en `tasks.md` la de la fase $ARGUMENTS. Si no existe o ya está marcada, dilo y para. Si la fase anterior está marcada pero su commit no está en git (`git --no-optional-locks log`), dilo y para: una fase empieza después del commit de la anterior. Si está en git y a su casilla le falta, pon el commit.
3. **Lo que se lee.** De `plan.md`, lo de esta fase; `clarify.md`; y el código que toca.
4. **La implementación.** Solo lo de esta fase. Lo que encuentres y no sea de ella va a `docs/BACKLOG.md` en el momento. Si es de prioridad alta, dilo antes de seguir.
5. **La verificación.**
   - `timeout {{TIMEOUT_S}} {{SUITE}}` en verde, con su tiempo.
   - El criterio de la fase, medido, con su número.
   - {{COMPROBACION_NO_CAMBIO}}, si la fase puede tocar lo que ya funcionaba.
6. **La casilla, marcada:** `[x]`, el número obtenido y la fecha.
7. **El cierre:** lo de la skill `cerrar-fase` (`.claude/skills/cerrar-fase/SKILL.md`).
8. **El reporte,** con el formato de `CLAUDE.md` §6, completo en `Claude outputs/fases/<NNN>/<fase>.md` (fuera de git), con el título del commit y el `git add` exacto, que lleva solo lo de la fase.
   Lo que devuelves es el resumen de seis líneas como mucho: «Fase N.N: hecha» (o «parcial: qué falta»); el criterio clave con su número; la suite (cuántas, cuánto) y la comprobación de «no cambió»; lo que fue al BACKLOG, si hay; el título del commit y el `git add`; «Reporte: `Claude outputs/fases/<NNN>/<fase>.md`». No hagas commit.
   Si algo te para antes (la marca, la casilla, el commit anterior, una prioridad alta fuera de alcance), devuelve una sola línea, «Parado: por qué», y termina: no esperes respuestas.
