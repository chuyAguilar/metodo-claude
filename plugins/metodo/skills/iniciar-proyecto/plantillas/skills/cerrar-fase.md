---
name: cerrar-fase
description: Pone al día memory.md, el BACKLOG y los índices, comprueba las líneas largas y mide el arranque. La corre el agente de desarrollo al final de cada fase, o suelta cuando la dirección se lo pide.
---

Cierra la fase que acaba de terminar. No toques código.

1. **`memory.md`:** la meta y la fase (hecha, pendiente del commit del autor), lo siguiente, las decisiones abiertas y los pendientes del autor. Como máximo 12 KB; si pasa, sale lo cerrado (ya está en `tasks.md` y en git).
2. **`docs/BACKLOG.md`:** lo que la fase dejó para después, con qué es, por qué queda, de dónde viene, qué haría falta y su prioridad. Lo que la fase cerró, en «Cerrados» con la fecha y qué lo cerró. El índice de lo abierto, al día.
3. **`docs/ARCHITECTURE.md`:** si cambió la estructura, un contrato entre módulos o un formato de salida, el cambio en presente, su línea en el índice y la «Última actualización». **`docs/DECISIONS.md`:** si la fase trae un ADR nuevo (lo escribe la dirección), su línea en el índice.
4. **`tasks.md`:** si una casilla marcada no tiene su commit y ya está en git, ponlo.
5. **Las líneas:** cuenta las de más de 2 000 caracteres en `docs/` (fuera de `docs/history/`), `memory.md`, `CLAUDE.md`, `specs/`, `.claude/agents/` y `.claude/skills/`. Tienen que ser 0; si no, pártelas sin cambiar lo que dicen.
6. **El arranque:** una tabla con los bytes de `CLAUDE.md`, `docs/constitution.md`, `memory.md`, `docs/CONTEXT.md` (si existe) y, del spec activo, `spec.md` y `tasks.md`, y el total. Si pasa de 48 KB (49 152 bytes), avísalo al principio del reporte y propón qué recortar.
7. **Al terminar,** propón el título del commit y el `git add` exacto. Si se corre suelta, el reporte va a `Claude outputs/fases/<NNN>/<fase>-cierre.md` y devuelves solo el resumen de `CLAUDE.md` §6. No hagas commit.
