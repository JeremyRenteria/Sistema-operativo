# proceso.py
from enum import Enum
import time

class EstadoProceso(Enum):
    NUEVO = "NUEVO"
    LISTO = "LISTO"
    EJECUTANDO = "EJECUTANDO"
    BLOQUEADO = "BLOQUEADO"
    TERMINADO = "TERMINADO"

class Proceso:
    def __init__(self, pid, nombre, prioridad, tiempo_rafaga=5):
        self.pid = pid
        self.nombre = nombre
        self.prioridad = prioridad
        self.tiempo_rafaga = tiempo_rafaga
        self.tiempo_restante = tiempo_rafaga
        self.estado = EstadoProceso.NUEVO
        self.recursos_asignados = []
        self.tiempo_llegada = time.time()
        self.tiempo_inicio = None
        self.tiempo_finalizacion = None

    def solicitar_recurso(self, recurso):
        if recurso.asignar_a_proceso(self):
            self.recursos_asignados.append(recurso)
            print(f"Proceso {self.pid} obtuvo el recurso {recurso.nombre}")
            return True
        else:
            print(f"Proceso {self.pid} no pudo obtener el recurso {recurso.nombre}")
            self.estado = EstadoProceso.BLOQUEADO
            return False

    def liberar_recurso(self, recurso):
        if recurso in self.recursos_asignados:
            recurso.liberar(self)
            self.recursos_asignados.remove(recurso)
            print(f"Proceso {self.pid} liberó el recurso {recurso.nombre}")

    def ejecutar(self):
        if self.estado == EstadoProceso.LISTO:
            self.estado = EstadoProceso.EJECUTANDO
            if self.tiempo_inicio is None:
                self.tiempo_inicio = time.time()
            
            print(f"Ejecutando proceso {self.pid} ({self.nombre})...")
            time.sleep(0.1)
            tiempo_quantum = min(2, self.tiempo_restante)
            self.tiempo_restante -= tiempo_quantum

            if self.tiempo_restante <= 0:
                self.terminar()
            else:
                self.estado = EstadoProceso.LISTO
                print(f"Proceso {self.pid} suspendido, tiempo restante: {self.tiempo_restante}")

    def terminar(self):
        self.estado = EstadoProceso.TERMINADO
        self.tiempo_finalizacion = time.time()
        for recurso in self.recursos_asignados.copy():
            self.liberar_recurso(recurso)
        print(f"Proceso {self.pid} ({self.nombre}) terminado")

    def tiempo_espera(self):
        if self.tiempo_finalizacion:
            return self.tiempo_finalizacion - self.tiempo_llegada - self.tiempo_rafaga
        return 0

    def __str__(self):
        recursos_str = ", ".join([r.nombre for r in self.recursos_asignados])
        return f"PID: {self.pid} | {self.nombre} | Prioridad: {self.prioridad} | Estado: {self.estado.value} | Recursos: [{recursos_str}] | Tiempo restante: {self.tiempo_restante}"

    def __lt__(self, other):
        return self.prioridad < other.prioridad
