# metodo-claude

La forma de trabajo del equipo con Claude Code, empaquetada como plugin. Trae la skill **`iniciar-proyecto`**, que monta en cualquier proyecto, por etapas y con tu autorización en cada una:

- `docs/constitution.md`, `CLAUDE.md`, `memory.md`, `docs/BACKLOG.md` y la plantilla de specs;
- cuatro agentes por papel: **dirección**, **planificación**, **desarrollo** y **pruebas**;
- las skills `planear`, `fase` y `cerrar-fase`;
- hooks que niegan lo que no es de cada papel y cualquier `git commit` o `git push` de un agente.

La regla de oro: **primero el plan, después tu autorización, después el trabajo. Los commits los haces tú.**

Esta guía es el guion de la llamada. Está pensada para **Windows**.

---

## 1. Lo que necesitas antes de empezar

| Qué | Para qué | Cómo comprobarlo |
| --- | --- | --- |
| Cuenta de Claude **Pro, Max, Team o Enterprise** | El plan gratuito no incluye Claude Code | Entra a claude.ai |
| **Git for Windows** — <https://git-scm.com/downloads/win> | Git, y Git Bash, que Claude Code usa como shell y con el que corren los hooks del método | `git --version` |
| **Python 3.10+** (opcional) | Solo para los hooks de la etapa 3 | `python --version` |
| Acceso al repo de GitHub de este plugin | Para instalarlo | Abre el repo en el navegador |

> Instala Git for Windows **antes** que Claude Code. Deja las opciones por defecto del instalador.

## 2. Instalar Claude Code

1. Abre **PowerShell** (la línea empieza con `PS C:\...`). No hace falta como administrador.
2. Pega:

   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

   No muestra progreso mientras descarga; espera a que vuelva el prompt.
3. **Cierra y abre una terminal nueva**, y comprueba:

   ```powershell
   claude --version
   ```

   Tiene que imprimir algo como `2.1.xxx (Claude Code)`.
4. Entra a una carpeta cualquiera y arranca:

   ```powershell
   cd C:\Dev
   claude
   ```

   La primera vez abre el navegador para iniciar sesión con tu cuenta de Claude. Sigue los pasos y vuelve a la terminal.

Si algo falla: `claude doctor` da un diagnóstico sin abrir sesión.

| Síntoma | Qué pasa | Arreglo |
| --- | --- | --- |
| `claude` no se reconoce | La carpeta de instalación no está en el PATH todavía | Abre una terminal nueva; si sigue, añade `%USERPROFILE%\.local\bin` al PATH |
| `'irm' is not recognized` | Estás en CMD, no en PowerShell | Usa PowerShell, o en CMD: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |
| Claude no encuentra Git Bash | Git se instaló en otra ruta | En `~/.claude/settings.json`: `"env": {"CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"}` |

## 3. Lo básico de la consola (5 minutos)

| Atajo / comando | Qué hace |
| --- | --- |
| Escribir y Enter | Le hablas en lenguaje natural |
| `Shift+Tab` | Cambia de modo: normal → aceptar ediciones → **plan** (solo planea, no toca nada) |
| `/help` | Lista de comandos |
| `/model` | Elegir modelo |
| `/resume` | Retomar una conversación anterior |
| `!comando` | Corre un comando de shell y deja la salida en la conversación (p. ej. `!git status`) |
| `Esc` | Interrumpe lo que está haciendo |
| `Esc Esc` | Vuelve atrás en la conversación |
| `/exit` o `Ctrl+C` dos veces | Salir |

Cuando Claude pida permiso para algo (editar un archivo, correr un comando), **lee qué es antes de aceptar**.

## 4. Instalar el método

Dentro de `claude`:

```text
/plugin marketplace add chuyAguilar/metodo-claude
/plugin install metodo@metodo-claude
```

(El repo: <https://github.com/chuyAguilar/metodo-claude>. Si es privado, necesitas acceso y tener Git autenticado con GitHub; la forma más fácil es `gh auth login`.)

Reinicia Claude Code (`/exit` y `claude`) y comprueba que la skill aparece: escribe `/metodo` y debe sugerirte `/metodo:iniciar-proyecto`.

**Actualizar** cuando publiquemos cambios:

```text
/plugin marketplace update metodo-claude
```

## 5. Montar el método en un proyecto

1. Abre una terminal en la carpeta del proyecto (nuevo o existente). Si no es repo git: `git init`.
2. `claude`
3. `/metodo:iniciar-proyecto` (o dile «inicia el proyecto con nuestro método»).
4. **Paso 0 · Te hace preguntas** — ten las respuestas pensadas:
   - De qué trata el proyecto y **qué no se puede romper nunca**.
   - Si hay **carpetas privadas** (datos de clientes, credenciales…) que ningún agente debe leer ni subir a git.
   - Idioma de documentos y commits.
   - Qué comprobación dice **«no cambió lo que ya funcionaba»** (si no hay otra: la suite de pruebas en verde).
   - Modelo para cada agente (se puede dejar el de referencia).
   - Si hay Python para los hooks.
5. Te enseña la propuesta de la **etapa 1** y espera. Revísala y responde **«autorizado»**.
6. Crea los archivos y te da el **título del commit y el `git add` exacto**. Tú haces el commit:

   ```powershell
   git add <lo que te dio>
   git commit -m "<el título>"
   ```

   y le dices **«commiteado»**.
7. Lo mismo con la **etapa 2** (los agentes y las skills, cuando ya hay código) y la **etapa 3** (los hooks, cuando haga falta).

| Etapa | Qué monta | Cuándo |
| --- | --- | --- |
| 1 · Lo mínimo | Constitución, `CLAUDE.md`, `memory.md`, BACKLOG, plantilla de specs, `.claude/settings.json`, `.gitignore` | Desde el día uno |
| 2 · Los papeles | Los cuatro agentes, `planear`/`fase`/`cerrar-fase`, ARCHITECTURE/DECISIONS/PRUEBAS | Cuando ya hay código de verdad |
| 3 · Las barreras | Hooks que niegan lo que no es de cada papel, con sus pruebas | Cuando el equipo o los datos lo piden |

## 6. El día a día, después de la etapa 2

Se trabaja siempre desde la **sesión de dirección**:

```powershell
claude --agent direccion
```

1. Le cuentas la meta. Escribe el spec en `specs/NNN-nombre/spec.md`.
2. Lanza a **planificación** (`/planear NNN-nombre`). Te trae el plan y las preguntas; las contestas.
3. Lees el plan y dices **«autorizado»**. Sin eso no se escribe código.
4. Lanza a **desarrollo** fase por fase (`/fase 1`, `/fase 2`…). Cada fase vuelve con un resumen de seis líneas y te propone el commit. **Tú commiteas** y dices «commiteado»; solo entonces empieza la siguiente.
5. Al final, lanza a **pruebas** sobre lo commiteado. Lo que falla, tú decides si se arregla ahora (fase nueva) o va al BACKLOG.

Dónde está cada cosa:

| Archivo | Qué guarda |
| --- | --- |
| `docs/constitution.md` | Lo que no se negocia |
| `CLAUDE.md` | Cómo trabaja Claude en este repo |
| `memory.md` | El estado de hoy y el spec activo |
| `docs/BACKLOG.md` | Lo que falta |
| `docs/DECISIONS.md` | El porqué de las decisiones (ADR) |
| `docs/PRUEBAS.md` | Lo que se probó |
| `specs/NNN-nombre/` | Una meta: spec, plan, aclaraciones y tareas |
| `Claude outputs/` | Reportes de los agentes, fuera de git |

## 7. Problemas frecuentes con el método

| Síntoma | Por qué | Qué hacer |
| --- | --- | --- |
| «Ningún agente hace git commit…» | Es a propósito: los commits son tuyos | Copia el comando que te propone y córrelo tú |
| «El hook no pudo correr…: se niega la herramienta» | Los hooks fallan cerrados: falta Python o la ruta del intérprete está mal | Revisa la ruta de Python en `.claude/settings.json` y en los agentes; corre las pruebas de los hooks |
| Un agente devuelve «Parado: …» | Le falta algo para seguir (plan sin autorizar, fase anterior sin commit…) | Lee el motivo y resuélvelo; no le pidas que se lo salte |
| `/metodo:iniciar-proyecto` no aparece | El plugin no se instaló o no se reinició Claude Code | `/plugin` para ver los instalados; reinicia |

---

## Para quien mantiene este repo

```
metodo-claude/
  .claude-plugin/marketplace.json     el catálogo (este repo es un marketplace)
  plugins/metodo/
    .claude-plugin/plugin.json        el plugin; sube "version" en cada cambio
    skills/iniciar-proyecto/
      SKILL.md                        las instrucciones de la skill
      plantillas/                     todo lo que copia a cada proyecto
```

- Validar antes de publicar: `claude plugin validate .` y `claude plugin validate plugins/metodo`.
- Probar los hooks: `python -m unittest discover -s plugins/metodo/skills/iniciar-proyecto/plantillas/hooks -p "test_*.py" -v`.
- Probar en local sin publicar: `/plugin marketplace add C:\Dev\metodo-claude`.
- Cada cambio: sube `version` en `plugin.json` y en `marketplace.json`, commit y push; el equipo corre `/plugin marketplace update metodo-claude`.
