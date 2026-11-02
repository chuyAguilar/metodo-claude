# CLAUDE.md — instrucciones para Claude Code en {{PROYECTO}}

Instrucción de herramienta: cómo se trabaja en este repo. No es documentación del proyecto ni repite sus principios.
Los principios están en `docs/constitution.md`, que manda sobre este archivo; aquí se remite a ellos por su número.
Lo leen todos los papeles; lo que es de uno solo está en su archivo de `.claude/agents/`.

## 1. Al arrancar

En este orden:

1. Lee completos `docs/constitution.md` y `memory.md` (y `docs/CONTEXT.md`, si existe).
2. Lee completos, del spec activo, `spec.md` y `tasks.md`. El spec activo es el que nombra `memory.md`, siempre con las mismas palabras: «Spec activo: `specs/NNN-nombre/`».
   `clarify.md` y `plan.md` no se leen al arrancar: los leen `planear`, que los escribe, y `fase`, que los ejecuta.
3. Consulta `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/BACKLOG.md` y `docs/PRUEBAS.md` por sección: primero su índice, después solo la sección que haga falta.
4. `docs/history/` solo cuando haga falta saber cómo se llegó a algo. Es copia literal y no se edita.

Lo que se lee al arrancar, con el spec activo, no pasa de 48 KB. `cerrar-fase` lo mide.

Antes de escribir código, lee el que ya existe. No reinventes lo que hay.

## 2. El flujo de una meta

Quién hace cada cosa está en el principio 2 de la constitución. Los pasos:

1. **El spec.** `specs/NNN-nombre/spec.md` trae el qué, el porqué y el criterio de cierre medible, y lo escribe la dirección desde `specs/_plantilla/`.
2. **El plan.** La dirección lanza a `planificacion` con «/planear NNN-nombre». Escribe `plan.md`: archivos, funciones con firma, fases con su criterio, lo que irá al BACKLOG y las preguntas abiertas. Sin código.
3. **Las respuestas.** Van en `clarify.md`: la pregunta, las opciones, la respuesta del autor y la fecha. Las escribe la dirección.
4. **La autorización.** Cuando el autor autoriza el plan, la primera línea de `tasks.md` dice «Plan autorizado por el autor el AAAA-MM-DD». Sin esa línea no se implementa nada.
5. **Las fases.** La dirección lanza a `desarrollo` con «/fase n»; implementa solo esa fase, marca la casilla con el número obtenido, deja el reporte en el disco y devuelve el resumen de seis líneas (§6).
6. **El commit.** Uno por fase, y lo hace el autor con el título y el `git add` que propone el reporte. La fase siguiente empieza después de su commit.
7. **Las pruebas.** Por fase si el spec lo pide, y si no al cerrar la meta, siempre sobre HEAD commiteado y con el árbol limpio: la dirección escribe `Claude outputs/pruebas/<fase>/encargo.md` y lanza a `pruebas`. Un fallo alto es una fase nueva que el autor autoriza; lo demás va al BACKLOG.
8. **El cierre.** `cerrar-fase` pone al día el estado y los índices (§3).

Una decisión que no es trivial se propone como ADR en `plan.md`; el ADR lo escribe la dirección.
Una dependencia nueva se propone en el plan con su porqué.

## 3. Cerrar una fase

En el mismo cambio que la fase, antes de que el autor haga el commit:

- **`memory.md`:** la meta y la fase, lo siguiente, lo abierto y los pendientes del autor. Como máximo 12 KB.
- **`docs/BACKLOG.md`:** la entrada se escribe cuando se decide no hacerlo ahora, no después. Cada entrada dice qué es, por qué queda, de dónde viene y qué haría falta. Prioridades: alta, puede dar un resultado equivocado o impide usar el producto; media, mejora clara sin riesgo; baja, espera datos o solo si estorba. Lo cerrado pasa a «Cerrados» con la fecha y qué lo cerró.
- **Los índices:** quien añade, cierra o cambia una entrada de `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` o `docs/BACKLOG.md` actualiza su índice en el mismo cambio.
- **Las líneas:** ninguna línea de `docs/`, `memory.md`, `specs/`, `.claude/agents/` ni `.claude/skills/` pasa de 2 000 caracteres, porque el lector de archivos las corta.

## 4. Reglas de operación

- **Los papeles.** En `.claude/agents/`: `direccion` (la sesión principal; el autor la abre con `claude --agent direccion`) y `planificacion`, `desarrollo` y `pruebas`, subagentes que solo lanza la dirección, con su propio contexto. Cada uno lleva en su frontmatter sus herramientas y su hook de rol, que niega lo que no es de su papel. Las rutinas son skills en `.claude/skills/`: `planear`, `fase` y `cerrar-fase`.
- **Git.** Ningún agente ejecuta `git commit` ni `git push`: deja los cambios en el árbol. Desde la shell, `git` va con `--no-optional-locks` y solo de lectura. No se toca `.git` ni se reescribe el historial.
- **Verificación.** Antes de dar una fase por terminada: `{{SUITE}}` en verde, con tiempo límite (`timeout {{TIMEOUT_S}}`) y con su tiempo; y {{COMPROBACION_NO_CAMBIO}}. Lo que la suite no puede probar se verifica con el criterio numérico del spec, y se reporta el número.
- **Alcance.** Lo que convendría hacer y no se pidió va al BACKLOG o a las sugerencias del reporte, no al código.
- **Las negaciones.** Un hook o un permiso que niega no se rodea: se dice en el reporte.
- **Sin memoria privada.** Lo que haya que recordar va a `memory.md` o a `docs/`, nunca a la memoria privada de Claude Code.
- **Los nombres.** Cada meta, fase y entrada del BACKLOG va con su nombre descriptivo («B12 · El login no recuerda la sesión»), nunca un número solo.

## 5. Entorno

- {{SISTEMA}}. {{LENGUAJE_Y_VERSION}}. El intérprete de los hooks: `{{PYTHON}}`.
- Instalar dependencias: `{{INSTALAR}}`. Correr: `{{CORRER}}`. Pruebas: `{{SUITE}}`; cuántas son y cuánto tardan, en `memory.md`.
- En un subagente no hace falta `cd`: el directorio ya es la raíz del repo. Lo largo va a un archivo con la herramienta de escritura, no en un heredoc.

## 6. Cómo reportar

Al final de cada fase, el reporte completo va a `Claude outputs/fases/<NNN>/<fase>.md`, fuera de git. Corto y sin adjetivos:

- qué archivos cambiaron;
- qué criterio se verificó y con qué número;
- la suite con su tiempo, y que lo que no debía cambiar no cambió;
- qué quedó pendiente o dudoso, y qué se anotó en el BACKLOG;
- las sugerencias fuera de alcance;
- el título del commit (en {{IDIOMA}}, en imperativo, corto y sin coautor) y el `git add` exacto.

Lo que `desarrollo` devuelve a la dirección es un resumen de seis líneas como mucho: «Fase N.N: hecha» (o «parcial: qué falta»); el criterio clave con su número; la suite (cuántas, cuánto) y la comprobación de «no cambió»; lo que fue al BACKLOG, si hay; el título del commit y el `git add`; «Reporte: `Claude outputs/fases/<NNN>/<fase>.md`».
