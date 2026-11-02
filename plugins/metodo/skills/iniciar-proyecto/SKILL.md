---
name: iniciar-proyecto
description: Monta en el proyecto actual nuestra forma de trabajo con Claude Code — constitución, CLAUDE.md, memory.md, specs con plan autorizado, BACKLOG, agentes por papel (dirección, planificación, desarrollo, pruebas), skills planear/fase/cerrar-fase y hooks que niegan lo que no es de cada papel. Úsala cuando el autor pida «inicia el proyecto con nuestro método», «monta la forma de trabajo» o la invoque por nombre. Va por etapas y para en cada una hasta que el autor autoriza. Trae todas las plantillas: no necesita ningún otro proyecto.
---

# Iniciar un proyecto con nuestro método

Vas a montar en este proyecto la forma de trabajo del equipo. El método se aplica a sí mismo: **primero el plan, después la autorización del autor, después el trabajo.** No escribas nada en el proyecto antes de que el autor autorice la etapa.

Todo lo que necesitas está en esta skill: las plantillas viven en `plantillas/`, junto a este archivo (`${CLAUDE_SKILL_DIR}/plantillas/` si la variable existe; si no, la carpeta donde está este `SKILL.md`). No busques ni leas otros proyectos del disco.

## La idea, para que no la pierdas

- **El autor decide y hace todos los commits.** Ningún agente ejecuta `git commit` ni `git push`. Hay dos paradas del autor que nadie salta: autoriza cada plan y hace cada commit.
- **Cada papel es un agente con su propio contexto.** Quien escribe el código no lo prueba; quien planea no implementa.
- **La memoria vive en archivos del repo,** no en la conversación ni en la memoria privada de Claude Code. Lo que no está escrito no existe.
- **Las reglas importantes están dos veces:** en el texto, para que se entiendan, y en un hook, para que no se salten.
- **Medir antes de decidir.** «Se ve bien» no cierra nada; un número que coincide con lo esperado, sí.
- **Una sola fuente por cosa.** Si dos archivos dicen lo mismo, acaban diciendo cosas distintas.

## Paso 0 · Conocer el proyecto (sin escribir nada)

1. Mira lo que ya hay: lenguaje, cómo se instalan las dependencias, cómo se corren las pruebas y cuánto tardan, si es repo git (si no, propón `git init`), si ya existe `CLAUDE.md` o `.claude/` (si existen, no los pises: propón cómo fusionarlos).
2. Pregunta al autor (con `AskUserQuestion` lo cerrado, en el chat lo abierto), solo lo que no puedas averiguar:
   - ¿De qué trata el proyecto y qué no se puede romper nunca? (Base de los principios del dominio.)
   - ¿Hay datos privados o carpetas que ningún agente debe leer ni subir a git? ¿Cuáles? (Puede no haber.)
   - ¿En qué idioma van los documentos y los commits? (Por defecto: español para personas, inglés para identificadores.)
   - ¿Qué comprobación dice «no cambió lo que ya funcionaba»? (Una prueba de regresión, comparar una salida de referencia, un snapshot… si no hay, «la suite en verde».)
   - ¿Qué modelo quiere para cada agente? (Referencia: dirección `opus`, planificación `opus`, desarrollo el más fuerte disponible, pruebas `sonnet`.)
   - ¿Hay Python en el equipo para los hooks? (`.venv\Scripts\python.exe` del proyecto, `python` del sistema, o ninguno: entonces la etapa 3 queda solo con `permissions.deny`.)
3. Con las respuestas, arma la tabla de marcadores (abajo) y enséñasela al autor junto con la propuesta de la etapa 1: qué archivos crearás y qué dirá cada uno en una línea. Espera «autorizado».

## Los marcadores

Las plantillas llevan `{{MARCADOR}}`. Rellénalos todos al copiar; al terminar cada etapa, `grep -rn "{{" ` sobre lo creado tiene que dar 0.

| Marcador | Qué va | Ejemplo |
| --- | --- | --- |
| `{{PROYECTO}}` | El nombre del proyecto | `facturador` |
| `{{FECHA}}` | Hoy, AAAA-MM-DD | `2026-11-02` |
| `{{IDIOMA}}` | Idioma de documentos y commits | `español` |
| `{{CARPETA_PRIVADA}}` | La carpeta privada, relativa a la raíz | `datos` |
| `{{SUITE}}` | El comando de la suite | `pytest -q`, `npm test` |
| `{{TIMEOUT_S}}` / `{{TIMEOUT_MS}}` | Tope de una corrida (con holgura sobre lo que tarda) | `600` / `600000` |
| `{{COMPROBACION_NO_CAMBIO}}` | La comprobación de «no cambió» | `la suite en verde y el snapshot igual` |
| `{{PYTHON}}` | Intérprete de los hooks | `$CLAUDE_PROJECT_DIR/.venv/Scripts/python.exe` o `python` |
| `{{SISTEMA}}`, `{{LENGUAJE_Y_VERSION}}`, `{{INSTALAR}}`, `{{CORRER}}` | El entorno, para `CLAUDE.md` §5 | `Windows 11 con Git Bash`, `Python 3.12 en .venv`… |
| `{{MODELO_DIRECCION}}`, `{{MODELO_PLANIFICACION}}`, `{{MODELO_DESARROLLO}}`, `{{MODELO_PRUEBAS}}` | Modelo de cada agente | `opus`, `sonnet` |
| `{{PRINCIPIO_DEL_DOMINIO}}` | Uno o más principios propios (constitución, del 7 en adelante) | — |

Si no hay carpeta privada: quita sus líneas (`permissions.deny` de `Read`/`Edit`, la del `.gitignore`, el principio 1 de la constitución se reduce a «lo privado no aparece en logs…») y deja `CARPETAS_PRIVADAS = []` en el hook.

## Las etapas

Cada una: propones, el autor autoriza, la haces, le das el título del commit y el `git add` exacto, y esperas a que diga «commiteado» antes de la siguiente.

### Etapa 1 · Lo mínimo que ya funciona

| Plantilla | Destino en el proyecto |
| --- | --- |
| `plantillas/docs/constitution.md` | `docs/constitution.md` (añade los principios del dominio; 5 a 10 en total) |
| `plantillas/CLAUDE.md` | `CLAUDE.md` (cita los principios por número, no los repite) |
| `plantillas/memory.md` | `memory.md` (≤ 12 KB, con la línea exacta «Spec activo: …» o «Ningún spec activo») |
| `plantillas/docs/BACKLOG.md` | `docs/BACKLOG.md` |
| `plantillas/spec/*.md` | `specs/_plantilla/` (los cuatro) |
| `plantillas/settings.json` | `.claude/settings.json` **sin** el bloque `hooks` (llega en la etapa 3) y con `permissions.allow` ajustado a lo que se corre a diario aquí; quita `Skill(...)` y `Agent(...)` hasta la etapa 2 |
| `plantillas/gitignore` | `.gitignore` (fusiona si ya existe) |

Si la suite tarda poco (menos de 2 min), quita el bloque `env` de `settings.json`.

### Etapa 2 · Los papeles (cuando ya hay código de verdad)

| Plantilla | Destino |
| --- | --- |
| `plantillas/agents/{direccion,planificacion,desarrollo,pruebas}.md` | `.claude/agents/` **sin** el bloque `hooks:` del frontmatter (ni su comentario `# ETAPA 3`) |
| `plantillas/skills/planear.md` | `.claude/skills/planear/SKILL.md` |
| `plantillas/skills/fase.md` | `.claude/skills/fase/SKILL.md` |
| `plantillas/skills/cerrar-fase.md` | `.claude/skills/cerrar-fase/SKILL.md` |
| `plantillas/docs/{ARCHITECTURE,DECISIONS,PRUEBAS}.md` | `docs/` (ARCHITECTURE describe lo que ya hay, en presente) |

Y en `.claude/settings.json`, añade a `permissions.allow` los `Skill(planear)`, `Skill(fase)`, `Skill(cerrar-fase)` y `Agent(planificacion)`, `Agent(desarrollo)`, `Agent(pruebas)`.

Regla para los subagentes: no preguntan. Si algo los para, devuelven una sola línea, «Parado: por qué». A partir de aquí el autor trabaja con `claude --agent direccion`.

### Etapa 3 · Las barreras (cuando haga falta)

Solo si hay Python (Paso 0). Si no, explica que las barreras quedan en `permissions.deny` y pasa al final.

1. Copia `plantillas/hooks/{sin_privados.py,por_rol.py,test_hooks.py}` a `.claude/hooks/`.
2. Ajusta el bloque **CONFIGURACION** de arriba de cada hook: `CARPETAS_PRIVADAS` en `sin_privados.py`; `CODIGO`, `MANIFIESTOS` (`pyproject.toml`, `package.json`…) y `SUITE` (patrones que reconocen el comando de la suite) en `por_rol.py`. Si cambias las carpetas, ajusta los casos de `test_hooks.py` que las nombran.
3. Corre las pruebas: `timeout 120 {{PYTHON}} -m unittest discover -s .claude/hooks -p "test_*.py" -v`. Tienen que pasar todas antes de registrar nada.
4. Registra el hook global: el bloque `hooks` de `plantillas/settings.json` en `.claude/settings.json`.
5. Registra el hook de rol: el bloque `hooks:` de la plantilla de cada agente en su frontmatter.
6. Lo que los hooks no miran (lo dicen sus docstrings) va como una entrada baja al BACKLOG.

Reglas de los hooks: fallan cerrados (si no corren, niegan), solo biblioteca estándar, se llaman con el intérprete por su ruta, tienen sus propias pruebas. Con `claude --agent direccion`, los hooks de la dirección corren también sobre sus subagentes; `por_rol.py` mira `agent_type` y deja que decida el hook del subagente.

Más adelante, si hacen falta: un agente `requisitos` (convierte una petición en objetivos medibles con sus preguntas) y uno de `documentacion` (el manual de uso). No vienen en las plantillas: se diseñan con el autor como una meta más.

## Una sola fuente por cosa

| Archivo | Qué guarda |
| --- | --- |
| `docs/constitution.md` | Lo que no se negocia |
| `CLAUDE.md` | Cómo se trabaja |
| `memory.md` | El estado de hoy y el spec activo |
| `docs/CONTEXT.md` | Las reglas del dominio y el entorno (opcional al principio) |
| `docs/ARCHITECTURE.md` | El qué |
| `docs/DECISIONS.md` | El porqué |
| `docs/BACKLOG.md` | Lo que falta |
| `docs/PRUEBAS.md` | Lo que se probó |
| `docs/history/` | Lo hecho, copia literal, no se edita |
| `specs/NNN-nombre/` | Una meta: `spec.md`, `plan.md`, `clarify.md`, `tasks.md` |

## Al terminar cada etapa

- Comprueba que no quedó ningún `{{` en lo creado.
- Lista los archivos creados y su tamaño en bytes.
- Propón el título del commit (en el idioma del proyecto, en imperativo, corto, sin coautor) y el `git add` exacto.
- Di qué queda para la etapa siguiente y espera.
