"""Hook global PreToolUse: vale para todos los papeles.

Niega, antes de cada herramienta:
- lo que nombre una carpeta privada (CARPETAS_PRIVADAS), en los campos de ruta y en los tokens de un comando;
- todo `git commit` y `git push`, escrito como sea (con opciones antes, dentro de `bash -c`, en otra linea...).

Reglas: solo biblioteca estandar; falla cerrado (si algo truena, niega); lo que no mira va al BACKLOG.
Lo que no mira hoy: rutas armadas en tiempo de ejecucion (variables, `$(...)`) y un `*` o `**` suelto que el shell
expande despues (`ls *` lista tambien la carpeta privada). Para eso estan ademas `permissions.deny` y el `.gitignore`.

Se registra en `.claude/settings.json`; lee el JSON del hook por stdin y escribe la decision por stdout.
"""
from __future__ import annotations

import fnmatch
import json
import re
import shlex
import sys

# --- CONFIGURACION (la rellena iniciar-proyecto) -------------------------------------------------------------------
# Nombres de carpeta privados, relativos a la raiz del repo. Vacia = no hay datos privados (solo se vigila git).
CARPETAS_PRIVADAS: list[str] = ["datos_privados"]
# ------------------------------------------------------------------------------------------------------------------

CAMPOS_RUTA = ("file_path", "path", "notebook_path", "pattern", "glob")
COMANDOS = ("Bash", "PowerShell")
GIT_PROHIBIDO = re.compile(r"\bgit\b[\s\S]*?\b(commit|push)\b", re.IGNORECASE)


def _segmentos(texto: str) -> list[str]:
    """Parte una ruta en segmentos, con / o con \\, sin comillas y en minusculas (Windows no distingue)."""
    limpio = texto.strip().strip("'\"").replace("\\", "/").lower()
    return [s for s in re.split(r"/+", limpio) if s]


def nombra_privada(texto: str) -> bool:
    """True si algun segmento de la ruta es una carpeta privada (o la empieza: `datos_privados*`)."""
    if not texto:
        return False
    privadas = [p.strip("/\\").lower() for p in CARPETAS_PRIVADAS if p.strip("/\\")]
    for seg in _segmentos(texto):
        seg = seg.strip("'\"")
        comodin = any(c in seg for c in "*?[") and seg.strip("*") != ""  # `*` o `**` solos no cuentan
        for p in privadas:
            if seg == p or (comodin and fnmatch.fnmatchcase(p, seg)):
                return True
    return False


def tokens(comando: str) -> list[str]:
    """Tokens del comando, sin comillas. posix=False para no comerse las \\ de las rutas de Windows.
    Si shlex no puede (comillas sin cerrar), cae a partir por espacios y simbolos."""
    try:
        lex = shlex.shlex(comando, posix=False, punctuation_chars=";&|<>()")
        lex.whitespace_split = True
        crudos = list(lex)
    except ValueError:
        crudos = re.split(r"[\s;&|<>()=]+", comando)
    return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in "'\"" else t for t in crudos if t]


def comando_nombra_privada(comando: str) -> bool:
    if any(nombra_privada(t) for t in tokens(comando)):
        return True
    # tambien dentro de un `bash -c "..."` o con `=` pegado: miro el texto crudo por segmentos
    return any(nombra_privada(t) for t in re.split(r"[\s;&|<>()=\"']+", comando))


def es_git_prohibido(comando: str) -> bool:
    return bool(GIT_PROHIBIDO.search(comando))


def decide(payload: dict) -> str | None:
    """Devuelve el motivo de la negacion, o None si se deja pasar."""
    herramienta = payload.get("tool_name", "")
    entrada = payload.get("tool_input") or {}
    if herramienta in COMANDOS:
        comando = str(entrada.get("command", ""))
        if es_git_prohibido(comando):
            return "Ningun agente hace git commit ni git push: los hace el autor."
        if CARPETAS_PRIVADAS and comando_nombra_privada(comando):
            return "El comando nombra una carpeta privada; ningun agente la lee ni la toca."
        return None
    if CARPETAS_PRIVADAS:
        for campo in CAMPOS_RUTA:
            valor = entrada.get(campo)
            if isinstance(valor, str) and nombra_privada(valor):
                return f"`{campo}` nombra una carpeta privada; ningun agente la lee ni la toca."
    return None


def niega(motivo: str) -> None:
    salida = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                     "permissionDecisionReason": motivo}}
    sys.stdout.write(json.dumps(salida, ensure_ascii=False))


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        motivo = decide(payload)
    except Exception as exc:  # falla cerrado
        motivo = f"sin_privados.py fallo ({type(exc).__name__}): se niega la herramienta."
    if motivo:
        niega(motivo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
