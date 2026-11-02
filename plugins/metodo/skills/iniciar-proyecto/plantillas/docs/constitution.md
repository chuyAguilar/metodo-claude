# Constitución de {{PROYECTO}}

Lo que no se negocia. No crea reglas: junta las que ya existen, cada una con su fuente. Cambiar un principio exige un ADR. Si un spec, un prompt o un comando choca con este archivo, gana este archivo y se avisa al autor.

Aprobada por el autor el {{FECHA}}.

<!-- iniciar-proyecto: los principios 1 a 6 son del método y valen para cualquier proyecto. Añade a partir del 7 los del dominio (lo que «no se puede romper nunca» del Paso 0), cada uno con su fuente. Entre 5 y 10 en total; borra este comentario. -->

1. **Los datos privados no salen de su sitio.**
   - `{{CARPETA_PRIVADA}}/` nunca entra en git, y ningún agente la lee ni la nombra.
   - Lo privado no aparece en logs, commits, pruebas, ADR ni notas.

   *Fuente: el autor, {{FECHA}}.*

2. **Cada quien su papel.**
   - **El autor** decide, autoriza cada plan y hace todos los commits: títulos cortos, sin coautor.
   - **La sesión de dirección** escribe specs y ADR, lanza a los agentes con su encargo, revisa y propone cada commit. No escribe código ni pruebas.
   - **El agente de planificación** escribe el plan de la meta, sin código. Solo toca `plan.md`, `clarify.md` y `tasks.md` del spec.
   - **El agente de desarrollo** implementa solo con un plan autorizado. No hace commits ni push.
   - **El agente de pruebas** verifica sin escribir código, con su propio contexto y sobre el commit probado. Escribe solo `docs/PRUEBAS.md` y sus reportes.

   *Fuente: el método; `CLAUDE.md` §4.*

3. **Plan antes de código, y nada fuera del alcance.**
   - Se trabaja fase por fase.
   - Lo que se deja para después va a `docs/BACKLOG.md` en el momento.
   - En medio de una meta solo se arregla lo de prioridad alta.

   *Fuente: el método.*

4. **Medir antes de decidir.** «Se ve bien» no cierra nada: un número que coincide con lo esperado, sí. Lo que ya funcionaba se comprueba con {{COMPROBACION_NO_CAMBIO}}.

   *Fuente: el método.*

5. **Una sola fuente por cosa:**
   - `docs/ARCHITECTURE.md`: el qué. `docs/DECISIONS.md`: el porqué (aditivo; un ADR nunca se reescribe).
   - `docs/BACKLOG.md`: lo que falta. `docs/PRUEBAS.md`: lo que se probó.
   - `memory.md`: el estado. `docs/history/`: lo hecho.

   *Fuente: el método.*

6. **Nada que deje el equipo o el árbol en mal estado.** Toda corrida lleva tiempo límite y ninguna espera es sin tope. Las pruebas destructivas se hacen en una copia.

   *Fuente: el método.*

7. **{{PRINCIPIO_DEL_DOMINIO}}**

   *Fuente: el autor, {{FECHA}}.*
