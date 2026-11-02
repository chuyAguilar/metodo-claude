# metodo-claude

Nuestra forma de trabajo con Claude Code, como plugin. Pasos para Windows: los comandos van en **PowerShell**, salvo donde dice «dentro de Claude Code».

## 1. Instalar Git for Windows

Descárgalo de <https://git-scm.com/downloads/win> e instálalo con las opciones por defecto. Comprueba:

```powershell
git --version
```

## 2. Instalar Python (opcional, solo para los hooks)

Descárgalo de <https://www.python.org/downloads/> y marca **«Add python.exe to PATH»**. Comprueba:

```powershell
python --version
```

## 3. Instalar Claude Code

```powershell
irm https://claude.ai/install.ps1 | iex
```

Cierra la terminal, abre una nueva y comprueba:

```powershell
claude --version
```

**Si dice «claude no se reconoce…»:** agrega la carpeta al PATH, recárgalo y vuelve a comprobar:

```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$env:USERPROFILE\.local\bin", "User")
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
claude --version
```

**Si dice «la ejecución de scripts está deshabilitada…»:** permite los scripts para tu usuario (responde S o Y) y repite este paso:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 4. Iniciar sesión

```powershell
claude
```

Se abre el navegador. Entra con tu cuenta de Claude (Pro, Max o Team) y vuelve a la terminal.

## 5. Solo si el repo es privado: acceso a GitHub

- Pide que te añadan como colaborador del repo.
- Instala GitHub CLI y autentícate:

```powershell
winget install GitHub.cli
gh auth login
```

## 6. Instalar el método

Dentro de Claude Code:

```text
/plugin marketplace add chuyAguilar/metodo-claude
/plugin install metodo@metodo-claude
```

Sal con `/exit` y vuelve a abrir con `claude`.

## 7. Usarlo en un proyecto

```powershell
cd C:\ruta\de\tu\proyecto
git init
claude
```

Dentro de Claude Code:

```text
/metodo:iniciar-proyecto
```

Claude te hará preguntas y te propondrá cada etapa. Respondes **«autorizado»**, haces el commit que te propone y respondes **«commiteado»**.

## 8. El día a día (a partir de la etapa 2)

```powershell
claude --agent direccion
```

## 9. Cuando haya cambios del método

Dentro de Claude Code:

```text
/plugin marketplace update metodo-claude
```

## Si algo falla

```powershell
claude doctor
claude update
```

---

**Para quien mantiene el repo:** la skill está en `plugins/metodo/skills/iniciar-proyecto/`. En cada cambio, sube `version` en `plugins/metodo/.claude-plugin/plugin.json` y en `.claude-plugin/marketplace.json`, y valida con `claude plugin validate .`.
