# PRUEBAS.md — {{PROYECTO}}

Registro de la verificación independiente de cada fase: qué se probó, por qué, cómo, qué salió y qué se concluyó. Lo escribe el **agente de pruebas**, que no escribe código, y lo commitea el autor.

**Aditivo.** Una entrada por fase, añadida al final. Lo anterior no se reescribe: si una conclusión cambia, se añade una nota fechada a esa entrada.

**Lo que no va aquí:** lo pendiente, que está en `BACKLOG.md`. Un fallo se describe una vez: aquí qué falló, y el commit que lo arregló o la entrada del BACKLOG donde quedó.

## Índice

*Una línea por entrada: fase · fecha · conclusión.*

## Formato de cada entrada

```
### Fase <n> — <título> · <fecha> · <commit probado>

- Qué cambió: una línea.
- Por qué se prueba así: qué podía romperse.
- Pruebas: tabla con qué, cómo, resultado (pasa / falla) y evidencia (el número).
- Fallos: cada uno con su gravedad, y el commit que lo arregló o la entrada de BACKLOG donde quedó.
- Prueba del autor: qué juzgó y qué dijo.
- Conclusión: se cierra / se cierra con pendientes (cuáles) / no se cierra.
```

---
