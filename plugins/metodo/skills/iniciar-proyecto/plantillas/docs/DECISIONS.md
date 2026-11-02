# DECISIONS.md — {{PROYECTO}}

Registro de decisiones de arquitectura (ADR). **Aditivo**: un ADR nunca se reescribe. Si una decisión se reemplaza, el ADR viejo cambia su estado a *superseded por ADR-MMM* y se añade el nuevo. Los escribe la sesión de dirección.

Formato: `ADR-NNN · Título · Fecha · Estado` seguido de **Contexto → Decisión → Consecuencias**.

Estados posibles: `propuesto` · `aceptado` · `superseded por ADR-MMM`

**Índice** (un ADR por línea; quien añade un ADR o cambia un estado actualiza esta lista):

- ADR-001 · Forma de trabajo: el método de papeles con Claude Code · {{FECHA}} · aceptado

---

## ADR-001 · Forma de trabajo: el método de papeles con Claude Code · {{FECHA}} · aceptado

**Contexto.** El proyecto se desarrolla con Claude Code y hace falta que el trabajo sea revisable, repetible y que no dependa de la memoria de una conversación.

**Decisión.** Se adopta el método: constitución, `CLAUDE.md`, `memory.md`, specs con plan autorizado, BACKLOG, agentes por papel (dirección, planificación, desarrollo, pruebas) y hooks que niegan lo que no es de cada papel. El autor autoriza cada plan y hace cada commit.

**Consecuencias.** Más pasos por meta, a cambio de que cada cambio tenga un plan, un criterio medido y un commit del autor. Cambiar un principio de la constitución exige un ADR nuevo.
