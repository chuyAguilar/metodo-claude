"""Pruebas de los hooks. Se corren con: <python> -m unittest discover -s .claude/hooks -p "test_*.py" -v
Usan la configuracion por defecto de arriba de cada hook; si la cambias, ajusta los casos que nombran carpetas."""
import json
import os
import subprocess
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import por_rol  # noqa: E402
import sin_privados  # noqa: E402

BASE = "C:/proyecto"
PRIV = sin_privados.CARPETAS_PRIVADAS[0] if sin_privados.CARPETAS_PRIVADAS else None


def cmd(c, **extra):
    return {"tool_name": "Bash", "tool_input": {"command": c}, "cwd": BASE, **extra}


def escribe(ruta, **extra):
    return {"tool_name": "Write", "tool_input": {"file_path": ruta}, "cwd": BASE, **extra}


class SinPrivados(unittest.TestCase):
    def test_git_commit_y_push_se_niegan_escritos_como_sea(self):
        for c in ["git commit -m x", "git --no-optional-locks commit -m x", "git -C . push", "bash -c 'git push'",
                  "echo hola && git commit -am y", "GIT commit"]:
            self.assertIsNotNone(sin_privados.decide(cmd(c)), c)

    def test_git_de_lectura_pasa(self):
        for c in ["git --no-optional-locks log --oneline -3", "git status --short", "git diff --stat"]:
            self.assertIsNone(sin_privados.decide(cmd(c)), c)

    @unittest.skipUnless(PRIV, "sin carpeta privada configurada")
    def test_carpeta_privada_en_rutas_y_comandos(self):
        for ruta in [f"{PRIV}/a.txt", f"C:\\proyecto\\{PRIV}\\b", f"./{PRIV}", f"{PRIV[:4]}*/x"]:
            self.assertIsNotNone(sin_privados.decide({"tool_name": "Read", "tool_input": {"file_path": ruta}}), ruta)
        self.assertIsNotNone(sin_privados.decide({"tool_name": "Grep", "tool_input": {"path": PRIV}}))
        for c in [f"ls {PRIV}", f"cat '{PRIV}/x'", f"python -c \"open('{PRIV}/x')\""]:
            self.assertIsNotNone(sin_privados.decide(cmd(c)), c)

    def test_lo_normal_pasa(self):
        self.assertIsNone(sin_privados.decide({"tool_name": "Read", "tool_input": {"file_path": "src/app.py"}}))
        self.assertIsNone(sin_privados.decide({"tool_name": "Glob", "tool_input": {"pattern": "**/*.py"}}))
        self.assertIsNone(sin_privados.decide(cmd("pytest -q")))

    def test_falla_cerrado(self):
        r = subprocess.run([sys.executable, os.path.join(AQUI, "sin_privados.py")], input="no es json",
                           capture_output=True, text=True, timeout=30)
        self.assertIn('"deny"', r.stdout)


class PorRol(unittest.TestCase):
    def test_rol_desconocido_o_ausente_niega(self):
        self.assertIsNotNone(por_rol.decide(None, escribe("README.md")))
        self.assertIsNotNone(por_rol.decide("nadie", escribe("README.md")))

    def test_direccion_no_escribe_codigo_ni_pruebas(self):
        self.assertIsNotNone(por_rol.decide("direccion", escribe("src/app.py")))
        self.assertIsNotNone(por_rol.decide("direccion", escribe(f"{BASE}/tests/test_x.py")))
        self.assertIsNotNone(por_rol.decide("direccion", escribe("docs/PRUEBAS.md")))
        self.assertIsNone(por_rol.decide("direccion", escribe("specs/001-x/spec.md")))
        self.assertIsNone(por_rol.decide("direccion", escribe("Claude outputs/pruebas/1.1/encargo.md")))

    def test_planificacion_solo_specs_sin_spec_md(self):
        self.assertIsNone(por_rol.decide("planificacion", escribe("specs/001-x/plan.md")))
        self.assertIsNotNone(por_rol.decide("planificacion", escribe("specs/001-x/spec.md")))
        self.assertIsNotNone(por_rol.decide("planificacion", escribe("specs/../src/a.py")))
        self.assertIsNotNone(por_rol.decide("planificacion", escribe("memory.md")))
        self.assertIsNotNone(por_rol.decide("planificacion", cmd("git stash")))
        self.assertIsNotNone(por_rol.decide("planificacion", cmd("timeout 600 pytest -q")))
        self.assertIsNone(por_rol.decide("planificacion", cmd("git --no-optional-locks log --oneline -3")))

    def test_desarrollo_no_toca_lo_de_pruebas_ni_la_constitucion(self):
        self.assertIsNone(por_rol.decide("desarrollo", escribe("src/app.py")))
        self.assertIsNotNone(por_rol.decide("desarrollo", escribe("docs/PRUEBAS.md")))
        self.assertIsNotNone(por_rol.decide("desarrollo", escribe("docs/constitution.md")))
        self.assertIsNotNone(por_rol.decide("desarrollo", cmd("echo x >> docs/PRUEBAS.md")))
        self.assertIsNone(por_rol.decide("desarrollo", cmd("pytest -q 2>&1 | tail -5")))

    def test_pruebas_solo_su_registro_y_git_de_lectura(self):
        self.assertIsNone(por_rol.decide("pruebas", escribe("docs/PRUEBAS.md")))
        self.assertIsNone(por_rol.decide("pruebas", escribe("Claude outputs/pruebas/1.1/ronda.md")))
        self.assertIsNotNone(por_rol.decide("pruebas", escribe("src/app.py")))
        self.assertIsNotNone(por_rol.decide("pruebas", escribe("C:/otro/sitio.txt")))
        self.assertIsNotNone(por_rol.decide("pruebas", cmd("git checkout -- src")))
        self.assertIsNotNone(por_rol.decide("pruebas", cmd("rm -rf src/modulo")))
        self.assertIsNone(por_rol.decide("pruebas", cmd("pytest -q")))

    def test_el_hook_de_direccion_se_aparta_ante_un_subagente(self):
        self.assertIsNone(por_rol.decide("direccion", escribe("src/app.py", agent_type="desarrollo")))
        self.assertIsNotNone(por_rol.decide("pruebas", escribe("src/app.py", agent_type="pruebas")))

    def test_falla_cerrado_sin_argumento(self):
        r = subprocess.run([sys.executable, os.path.join(AQUI, "por_rol.py")], input=json.dumps(escribe("a.md")),
                           capture_output=True, text=True, timeout=30)
        self.assertIn('"deny"', r.stdout)


if __name__ == "__main__":
    unittest.main()
