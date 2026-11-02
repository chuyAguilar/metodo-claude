"""Hook de rol PreToolUse. Cada agente de `.claude/agents/` lo declara en su frontmatter con su papel como argumento
(`por_rol.py pruebas`) y corre solo mientras ese agente trabaja, ademas de `sin_privados.py`, que vale para todos.

Antes de Edit, MultiEdit, Write, NotebookEdit, Bash y PowerShell niega lo que no es del papel (tabla ROLES):
- `escribe`: si no es None, las unicas rutas que el papel puede escribir (todo lo demas se niega);
- `nunca`: rutas que el papel no escribe nunca;
- `nunca_nombre`: nombres de archivo que no escribe en ningun sitio (p. ej. `spec.md` para planificacion);
- `git_solo_lectura`: todo git que no sea de lectura se niega;
- `sin_suite`: no corre la suite (dos suites a la vez no caben, y planificacion no mide: lo pide como fase).

Con `claude --agent direccion`, los hooks de la direccion corren tambien sobre sus subagentes: si el payload dice que
quien llama es otro papel (`agent_type`), este hook se aparta y decide el del subagente.

Reglas: solo biblioteca estandar; falla cerrado (sin rol, rol desconocido o error = niega).
Lo que no mira hoy: escrituras que hace un programa por dentro (`python guion.py` que escribe en src/). Va al BACKLOG.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sin_privados  # noqa: E402  # el partir comandos vive ahi; aqui solo decido por papel

# --- CONFIGURACION (la rellena iniciar-proyecto) -------------------------------------------------------------------
CODIGO = ["src/", "tests/"]  # lo que escribe solo desarrollo (con su manifiesto: pyproject.toml, package.json...)
MANIFIESTOS = ["pyproject.toml"]
SUITE = [r"\bpytest\b", r"-m\s+pytest\b"]  # patrones que reconocen que un comando corre la suite

ROLES = {
    "direccion": {"escribe": None, "nunca": CODIGO + MANIFIESTOS + ["docs/PRUEBAS.md"]},
    "planificacion": {"escribe": ["specs/"], "nunca_nombre": ["spec.md"], "git_solo_lectura": True,
                      "sin_suite": True},
    "desarrollo": {"escribe": None, "nunca": ["docs/PRUEBAS.md", "Claude outputs/pruebas/", "docs/constitution.md"]},
    "pruebas": {"escribe": ["docs/PRUEBAS.md", "Claude outputs/pruebas/"], "git_solo_lectura": True},
}
# ------------------------------------------------------------------------------------------------------------------

ESCRITURA = ("Edit", "MultiEdit", "Write", "NotebookEdit")
COMANDOS = ("Bash", "PowerShell")
GIT_LECTURA = {"log", "status", "diff", "show", "blame", "rev-parse", "ls-files", "grep", "describe", "shortlog"}
PROGRAMAS_QUE_ESCRIBEN = {"rm", "mv", "cp", "touch", "mkdir", "rmdir", "tee", "truncate", "ln",
                          "remove-item", "move-item", "copy-item", "new-item", "set-content", "add-content",
                          "out-file"}
SEPARADORES = {";", "&&", "||", "|", "&", "(", ")"}


def raiz(payload: dict) -> str:
    return (os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()).replace("\\", "/").rstrip("/")


def relativa(ruta: str, base: str) -> str | None:
    """La ruta relativa a la raiz, con / y en minusculas; None si cae fuera del repo o sube con `..`."""
    r = ruta.strip().strip("'\"").replace("\\", "/")
    if re.match(r"^/[a-zA-Z]/", r):  # /c/Dev/... de Git Bash
        r = r[1] + ":" + r[2:]
    b = base
    if re.match(r"^/[a-zA-Z]/", b):
        b = b[1] + ":" + b[2:]
    if re.match(r"^[a-zA-Z]:/", r) or r.startswith("/"):
        if not r.lower().startswith(b.lower() + "/"):
            return None
        r = r[len(b) + 1:]
    partes = []
    for p in r.split("/"):
        if p in ("", "."):
            continue
        if p == "..":
            if not partes:
                return None
            partes.pop()
        else:
            partes.append(p)
    return "/".join(partes).lower()


def cae_en(rel: str, sitio: str) -> bool:
    s = sitio.replace("\\", "/").lower()
    if s.endswith("/"):
        return rel.startswith(s) or rel + "/" == s
    return rel == s


def prohibida(rol: str, ruta: str, base: str) -> bool:
    reglas = ROLES[rol]
    rel = relativa(ruta, base)
    if rel is None:  # fuera del repo
        return reglas.get("escribe") is not None
    if any(rel.split("/")[-1] == n.lower() for n in reglas.get("nunca_nombre", [])):
        return True
    if any(cae_en(rel, s) for s in reglas.get("nunca", [])):
        return True
    permitidas = reglas.get("escribe")
    return permitidas is not None and not any(cae_en(rel, s) for s in permitidas)


def tramos(comando: str) -> list[list[str]]:
    """El comando partido en tramos por `;`, `&&`, `|`..., cada uno como lista de tokens."""
    salida, actual = [], []
    for t in sin_privados.tokens(comando):
        if t in SEPARADORES:
            if actual:
                salida.append(actual)
            actual = []
        else:
            actual.append(t)
    if actual:
        salida.append(actual)
    return salida


def destinos(comando: str) -> list[str]:
    """Las rutas que un comando parece escribir: redirecciones, `sed -i`, rm/mv/cp/tee/... y sus equivalentes en PS."""
    salida = []
    for tramo in tramos(comando):
        for i, t in enumerate(tramo):
            if t in (">", ">>") and i + 1 < len(tramo) and tramo[i + 1] not in ("&1", "&2", "/dev/null", "$null"):
                if not tramo[i + 1].startswith("&"):
                    salida.append(tramo[i + 1])
        programa = os.path.basename(tramo[0]).lower() if tramo else ""
        if programa in ("timeout",) and len(tramo) > 2:
            programa = os.path.basename(tramo[2]).lower()
        args = [a for a in tramo[1:] if not a.startswith("-") and a not in (">", ">>")]
        if programa in PROGRAMAS_QUE_ESCRIBEN:
            salida += args
        if programa == "sed" and any(a.startswith("-i") for a in tramo):
            salida += args[1:]
    return salida


def git_subcomandos(comando: str) -> list[str]:
    subs = []
    for tramo in tramos(comando):
        for i, t in enumerate(tramo):
            if os.path.basename(t).lower() in ("git", "git.exe"):
                resto = tramo[i + 1:]
                j = 0
                while j < len(resto) and resto[j].startswith("-"):
                    j += 2 if resto[j] in ("-C", "-c") else 1
                subs.append(resto[j].lower() if j < len(resto) else "")
                break
    return subs


def corre_suite(comando: str) -> bool:
    return any(re.search(p, comando) for p in SUITE)


def quien_llama(payload: dict) -> str | None:
    return payload.get("agent_type") or None


def decide(rol: str | None, payload: dict) -> str | None:
    if rol not in ROLES:
        return f"Hook de rol sin papel valido ({rol!r}); papeles: {', '.join(ROLES)}."
    llama = quien_llama(payload)
    if llama in ROLES and llama != rol:
        return None  # es un subagente: decide su propio hook
    herramienta = payload.get("tool_name", "")
    entrada = payload.get("tool_input") or {}
    base = raiz(payload)
    if herramienta in ESCRITURA:
        ruta = entrada.get("file_path") or entrada.get("notebook_path") or ""
        if prohibida(rol, ruta, base):
            return f"`{ruta}` no es del papel de {rol}."
        return None
    if herramienta in COMANDOS:
        comando = str(entrada.get("command", ""))
        reglas = ROLES[rol]
        if reglas.get("git_solo_lectura"):
            for sub in git_subcomandos(comando):
                if sub not in GIT_LECTURA:
                    return f"{rol} usa git solo de lectura (`git {sub}` no lo es)."
        if reglas.get("sin_suite") and corre_suite(comando):
            return f"{rol} no corre la suite: lo que haya que medir se pide como fase de desarrollo."
        for d in destinos(comando):
            if prohibida(rol, d, base):
                return f"El comando escribe `{d}`, que no es del papel de {rol}."
    return None


def main() -> int:
    try:
        rol = sys.argv[1] if len(sys.argv) > 1 else None
        payload = json.loads(sys.stdin.read() or "{}")
        motivo = decide(rol, payload)
    except Exception as exc:  # falla cerrado
        motivo = f"por_rol.py fallo ({type(exc).__name__}): se niega la herramienta."
    if motivo:
        sin_privados.niega(motivo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
