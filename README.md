# 🖥️ Sistema Operativo - Simulador de Gestión de Procesos

Un simulador de sistema operativo educativo que implementa un gestor de tareas con planificación de procesos, gestión de recursos y memoria virtual, desarrollado en Python.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Comandos](#-comandos-disponibles)
- [Estados de Procesos](#-estados-de-los-procesos)
- [Ejemplos](#-ejemplos-de-uso)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🎯 Gestión de Procesos
- **Estados de procesos**: NUEVO, LISTO, EJECUTANDO, BLOQUEADO, TERMINADO
- **Planificación por prioridades**: Cola de prioridad (heap) para procesos listos
- **Tiempo de ráfaga**: Simulación de tiempo de ejecución por proceso
- **Quantum de CPU**: Ejecución por tiempos de 2 unidades

### 💾 Gestión de Memoria
- **Memoria RAM**: Capacidad limitada (4 procesos)
- **Memoria Virtual**: Almacenamiento secundario cuando RAM está llena
- **Swapping automático**: Movimiento entre RAM y memoria virtual
- **Balanceo de memoria**: Reasignación automática cuando hay espacio disponible

### 🔧 Recursos del Sistema
- **CPUs**: 2 unidades de procesamiento
- **RAM**: 4 slots de memoria principal
- **Disco**: 2 unidades de almacenamiento
- **Memoria Virtual**: 10 slots de almacenamiento secundario

## 📁 Estructura del Proyecto
SISTEMAS-OPERATIVOS/
├── main.py # Programa principal con interfaz de comandos
├── sistemaoperativo.py # Gestor principal de tareas y recursos
├── proceso.py # Clase Proceso y estados
├── recurso.py # Clase Recurso para gestión de hardware
├── README.md # Este archivo
└── pycache/ # Archivos de caché de Python
💻 Uso
El sistema se ejecuta en una interfaz de línea de comandos interactiva:

text
=== SISTEMA OPERATIVO - GESTOR DE TAREAS ===
Comandos disponibles:
1. crear <nombre> <prioridad> [tiempo]
2. eliminar <pid>
3. listar
4. recursos
5. asignar <pid> <recurso>
6. ejecutar
7. auto <n>
8. stats
9. salir

SO> 

⌨️ Comandos Disponibles

| Comando | Uso | Descripción |
|---|---|---|
| crear | crear <nombre> <prioridad> [tiempo] | Crea un nuevo proceso |
| eliminar | eliminar <pid> | Elimina un proceso por PID |
| listar | listar | Muestra todos los procesos |
| recursos | recursos | Lista los recursos del sistema |
| asignar | asignar <pid> <recurso> | Asigna recurso a proceso |
| ejecutar | ejecutar | Ejecuta un ciclo de planificación |
| auto | auto <n> | Ejecuta n ciclos automáticamente |
| stats | stats | Muestra estadísticas del sistema |
| salir | salir | Termina el programa |

📊 Estados de los Procesos
🆕 NUEVO: Proceso recién creado

✅ LISTO: En cola esperando ejecución

⚡ EJECUTANDO: Actualmente en CPU

🚫 BLOQUEADO: Esperando por recursos

🏁 TERMINADO: Finalizó su ejecución

📈 Características Técnicas
Algoritmo de planificación: Por prioridades (menor número = mayor prioridad)

Gestión de memoria: Paginación simulada con swapping

Sincronización: Colas separadas para procesos listos y bloqueados

Manejo de recursos: Asignación y liberación con verificación de disponibilidad

🔄 Flujo de Ejecución
Los procesos se crean y asignan a RAM o memoria virtual

Procesos en RAM entran a la cola de listos

El planificador selecciona el proceso de mayor prioridad

Se ejecuta por quantum de tiempo

Los procesos pueden bloquearse por recursos o terminar

La memoria se rebalancea automáticamente

🤝 Contribución
¡Las contribuciones son bienvenidas! Para contribuir:

Haz un fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request


