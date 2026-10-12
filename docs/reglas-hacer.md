# Reglas: qué hacer

Reglas de trabajo para el agente constructor del paquete, extraídas del [encargo](../PLAN_PAQUETE_FLUJO_IA.md). La sección del encargo de la que sale cada regla va entre paréntesis. Complemento: [reglas-no-hacer.md](reglas-no-hacer.md).

## Al iniciar y al cerrar cada sesión

- **H-01** Al iniciar, leer el encargo, el [tablero](tablero.md), las decisiones vigentes y el estado real del repositorio. Identificar la tarea preparada y consultar solo las fuentes necesarias. (§13)
- **H-02** Antes de modificar, confirmar entradas, límites, comportamiento esperado y comprobaciones. (§13)
- **H-03** Al cerrar, registrar cambios, evidencia, pendientes, fuentes adaptadas y checkpoint, y actualizar el tablero. (§13)
- **H-04** Informar al usuario qué aprendimos, qué falta y qué decisión concreta requiere su criterio, en español y con explicaciones comprensibles. (§3, §13)
- **H-05** Continuar automáticamente con las tareas técnicas preparadas dentro del alcance autorizado. Plantear al usuario solo las decisiones de producto o bloqueos que no se resuelvan con las fuentes, y seguir mientras tanto con trabajo independiente. (§1, §4)

## Tablero y tareas

- **H-06** Trabajar desde el tablero en orden de dependencias, empezando por B01. Solo empezar tareas con dependencias verificadas. (§8)
- **H-07** Registrar en cada tarea: responsable, requisitos cubiertos, evidencia, checkpoint y siguiente actividad. (§8)
- **H-08** Descomponer un hito en unidades concretas antes de ejecutarlo si tiene varios objetivos o dudas determinantes. (§8, R09)
- **H-09** Convertir una incertidumbre técnica en una investigación con pregunta y condición de cierre. (§8)
- **H-10** Registrar explícitamente en el tablero cualquier dependencia descubierta. (§8)
- **H-11** Mantener separados tres ámbitos: documentos para construir el paquete, recursos que el paquete instala y documentos que genera en proyectos de usuario. (§5)

## Fuentes de referencia

- **H-12** Seguir el procedimiento de extracción **una pieza por vez** (§7): verificar versión, obtener sin ejecutar instaladores (sparse checkout si conviene), leer la carpeta completa y sus dependencias, registrar la ficha mínima, vincular con R01–R20, clasificar, proponer su incorporación al contrato y probarla con un caso que cubre la necesidad y otro que debe fallar.
- **H-13** Usar la ficha mínima: `fuente, commit, ruta, licencia, requisito cubierto, entradas, salidas, dependencias, mecanismo de control, evidencia, limitaciones, adaptación, prueba de integración, decisión`. (§7)
- **H-14** Fijar cada fuente al commit del inventario y registrarlo en `docs/fuentes.md` y `sources.lock.json`. Revisar la licencia raíz y también los avisos y licencias específicos de la pieza que se reutilice. (§7)
- **H-15** Guardar las copias en `.reference-sources/`, separadas de las instrucciones activas, y excluirlas del paquete distribuido. (§5, §7)
- **H-16** Antes de clonar, comprobar que el destino no existe. Si existe, comprobar su identidad y estado. (§7)
- **H-17** Detectar los supuestos del entorno original de cada fuente y convertirlos en dependencias visibles del paquete. (§12)
- **H-18** Registrar en `THIRD_PARTY_NOTICES.md` la procedencia de cada adaptación. (§5)

## Diseño

- **H-19** Diseñar las especificaciones antes de implementar. Cada una explica qué la inicia, qué produce, cómo se revisa y qué permite avanzar. (§1, §9)
- **H-20** Exigir a cada incorporación una necesidad, un contrato y una prueba. Mantener un único modelo de estado, un único registro de decisiones y una única interfaz de continuación. (§12)
- **H-21** Si dos fuentes resuelven lo mismo, elegir una o sintetizar explícitamente un procedimiento y documentar las diferencias. (§7, §12)
- **H-22** Preferir una skill coordinadora con procedimientos cargados según la actividad. Las skills auxiliares, si existen, comparten los mismos contratos y se usan a través del coordinador. (§5)
- **H-23** Dar a cada artefacto identificador, versión, estado, entradas, decisiones que lo condicionan y comprobación requerida. (§5)
- **H-24** Comprobar que cada documento puede usarse como entrada del siguiente sin reinterpretaciones contradictorias. (§9)
- **H-25** Elegir para los scripts propios el runtime mínimo apropiado según el entorno confirmado. (§12)
- **H-26** Resolver en los adaptadores lo que no es portable (metadatos exclusivos, hooks, agentes secundarios, importación de archivos). Mantener un modo secuencial funcional. (§6)
- **H-27** Usar validadores o mecanismos comprobados del host cuando un control deba impedir una transición inválida. (§6)
- **H-28** Ajustar la profundidad al riesgo: menos detalle para un cambio pequeño, más análisis y revisión para un sistema incierto o de mayor impacto. (R17)

## Decisiones y apuntes

- **H-29** Dar a cada propuesta identificador, alternativas, consecuencias y estado (propuesta, aceptada, rechazada, aplazada, sustituida). (R05)
- **H-30** Si hay varias propuestas activas, aclarar a cuál se refiere el usuario antes de cambiar su estado. (§4, E03)
- **H-31** Conservar el motivo de cada rechazo. (§4)
- **H-32** Asociar cada apunte del usuario a la pregunta, decisión o requisito que comenta. (R06)
- **H-33** Al reabrir una decisión, conservar la anterior, proponer un reemplazo, analizar el impacto y marcar para revisión las tareas y la evidencia afectadas. (§5, R11)

## Verificación y evidencia

- **H-34** Distinguir comprobaciones deterministas del paquete de observaciones del comportamiento del agente. (§10)
- **H-35** Informar de las pruebas omitidas o bloqueadas, y declarar pendiente cada requisito o host no probado. (R14, §6)
- **H-36** Marcar explícitamente los datos simulados y la falta de credenciales. (§5, R10)
- **H-37** Registrar si una revisión se hizo en un contexto independiente. (§6)
- **H-38** En la evaluación del agente: conservar entradas, versión, acciones, salidas y evidencia; registrar variaciones; repetir ante resultados contradictorios o inestables; fijar el umbral por escenario y riesgo. (§10)
- **H-39** Incluir fixtures sin defectos para comprobar que el agente no inventa problemas. (E15)
- **H-40** Probar los dos hosts reales y registrar sus versiones antes de publicar compatibilidad. (§6)

## Estado, git y recuperación

- **H-41** Actualizar el estado con escrituras atómicas donde corresponda y un único responsable de escritura. (§5)
- **H-42** Al retomar, contrastar estado, eventos, documentos y árbol de trabajo antes de ejecutar tareas nuevas. (§5)
- **H-43** Recuperar en una rama o worktree creado desde un commit comprobado, preservando el trabajo posterior. (§5, R12)
- **H-44** Si se pide revertir en la rama activa, analizar dependencias y proteger los cambios propios y del usuario. (§5)
- **H-45** Registrar en cada checkpoint: nombre comprensible, commit, versión del paquete, documentos asociados, comprobaciones ejecutadas, pendientes y dependencias externas. (§5)
- **H-46** Para sistemas desplegados, seguir un procedimiento específico de datos, infraestructura e integraciones. (§5, E18)

## Instalación y versiones

- **H-47** Instalar solo archivos del paquete, detectar conflictos y permitir retirar únicamente los archivos propios. (R16)
- **H-48** Materializar una sola copia activa por host. (§6)
- **H-49** Registrar en cada versión los cambios de contrato y cómo migrar proyectos de la versión anterior. (R20)
