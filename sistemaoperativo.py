import heapq
from collections import deque
from recurso import Recurso
from proceso import Proceso, EstadoProceso

class GestorTareas:
    def __init__(self):
        self.procesos = {}
        self.cola_listos = []
        self.cola_bloqueados = deque()
        self.proceso_actual = None
        self.recursos_sistema = {}
        self.contador_pid = 1
        self.memoria_virtual = []  # Cola de procesos en memoria virtual
        self.crear_recursos_basicos()

    def crear_recursos_basicos(self):
        self.recursos_sistema["CPU1"] = Recurso("CPU1", "CPU", 1)
        self.recursos_sistema["CPU2"] = Recurso("CPU2", "CPU", 1)
        self.recursos_sistema["RAM"] = Recurso("RAM", "memoria", 4)  # Capacidad reducida para forzar uso de MV
        self.recursos_sistema["DISCO"] = Recurso("DISCO", "disco", 2)
        self.recursos_sistema["MV"] = Recurso("MV", "memoria_virtual", 10)  # Memoria virtual en disco

    def crear_proceso(self, nombre, prioridad, tiempo_rafaga=5):
        proceso = Proceso(self.contador_pid, nombre, prioridad, tiempo_rafaga)
        self.procesos[self.contador_pid] = proceso
        
        # Intentar asignar RAM primero
        if self.recursos_sistema["RAM"].asignar_a_proceso(proceso):
            proceso.estado = EstadoProceso.LISTO
            heapq.heappush(self.cola_listos, proceso)
            print(f"Proceso creado: {proceso} [EN RAM]")
        else:
            # Si RAM está llena, usar memoria virtual
            if self.recursos_sistema["MV"].asignar_a_proceso(proceso):
                self.memoria_virtual.append(proceso)
                proceso.estado = EstadoProceso.BLOQUEADO
                print(f"Proceso creado: {proceso} [EN MEMORIA VIRTUAL]")
                self.mover_procesos_a_ram()  # Intentar rebalancear
            else:
                print(f"No se pudo crear el proceso {nombre}. Memoria llena.")
                del self.procesos[self.contador_pid]
                return None
        
        self.contador_pid += 1
        return proceso

    def mover_procesos_a_ram(self):
        """Mueve procesos de memoria virtual a RAM cuando hay espacio disponible"""
        if self.memoria_virtual and self.recursos_sistema["RAM"].esta_disponible():
            # Encontrar el proceso con mayor prioridad en memoria virtual
            self.memoria_virtual.sort(key=lambda p: p.prioridad)
            proceso_a_mover = self.memoria_virtual[0]
            
            if self.recursos_sistema["RAM"].asignar_a_proceso(proceso_a_mover):
                self.recursos_sistema["MV"].liberar(proceso_a_mover)
                self.memoria_virtual.remove(proceso_a_mover)
                proceso_a_mover.estado = EstadoProceso.LISTO
                heapq.heappush(self.cola_listos, proceso_a_mover)
                print(f"Proceso {proceso_a_mover.pid} movido de MV a RAM")

    def eliminar_proceso(self, pid):
        if pid in self.procesos:
            proceso = self.procesos[pid]
            proceso.terminar()
            
            # Liberar recursos
            if proceso in self.recursos_sistema["RAM"].procesos_asignados:
                self.recursos_sistema["RAM"].liberar(proceso)
            if proceso in self.recursos_sistema["MV"].procesos_asignados:
                self.recursos_sistema["MV"].liberar(proceso)
            
            # Remover de todas las colas
            if proceso == self.proceso_actual:
                self.proceso_actual = None
            self.cola_listos = [p for p in self.cola_listos if p.pid != pid]
            heapq.heapify(self.cola_listos)
            self.cola_bloqueados = deque([p for p in self.cola_bloqueados if p.pid != pid])
            if proceso in self.memoria_virtual:
                self.memoria_virtual.remove(proceso)
            
            del self.procesos[pid]
            print(f"Proceso {pid} eliminado del sistema")
            
            # Intentar mover procesos de MV a RAM después de liberar espacio
            self.mover_procesos_a_ram()
        else:
            print(f"Proceso {pid} no encontrado")

    def planificar_siguiente(self):
        self.verificar_procesos_bloqueados()
        if self.cola_listos:
            return heapq.heappop(self.cola_listos)
        return None

    def verificar_procesos_bloqueados(self):
        for proceso in list(self.cola_bloqueados):
            proceso.estado = EstadoProceso.LISTO
            self.cola_bloqueados.remove(proceso)
            heapq.heappush(self.cola_listos, proceso)

    def ejecutar_ciclo(self):
        if not self.proceso_actual or self.proceso_actual.estado == EstadoProceso.TERMINADO:
            self.proceso_actual = self.planificar_siguiente()
        if self.proceso_actual:
            if self.proceso_actual.estado == EstadoProceso.BLOQUEADO:
                self.cola_bloqueados.append(self.proceso_actual)
                self.proceso_actual = self.planificar_siguiente()
            if self.proceso_actual and self.proceso_actual.estado == EstadoProceso.LISTO:
                self.proceso_actual.ejecutar()
                if self.proceso_actual.estado == EstadoProceso.LISTO:
                    heapq.heappush(self.cola_listos, self.proceso_actual)
                    self.proceso_actual = None
        else:
            print("No hay procesos para ejecutar")

    def listar_procesos(self):
        if not self.procesos:
            print("No hay procesos en el sistema")
            return
        print("\n=== LISTA DE PROCESOS ===")
        for proceso in self.procesos.values():
            ubicacion = "RAM" if proceso in self.recursos_sistema["RAM"].procesos_asignados else "MV"
            print(f"{proceso} [UBICACIÓN: {ubicacion}]")
        
        print(f"\nProcesos en RAM: {len(self.recursos_sistema['RAM'].procesos_asignados)}")
        print(f"Procesos en Memoria Virtual: {len(self.memoria_virtual)}")

    def listar_recursos(self):
        print("\n=== RECURSOS DEL SISTEMA ===")
        for recurso in self.recursos_sistema.values():
            print(recurso)

    def asignar_recurso_a_proceso(self, pid, nombre_recurso):
        if pid in self.procesos and nombre_recurso in self.recursos_sistema:
            proceso = self.procesos[pid]
            recurso = self.recursos_sistema[nombre_recurso]
            proceso.solicitar_recurso(recurso)
        else:
            print(f"Proceso {pid} o recurso {nombre_recurso} no encontrado")

    def estadisticas(self):
        terminados = [p for p in self.procesos.values() if p.estado == EstadoProceso.TERMINADO]
        if terminados:
            tiempo_promedio_espera = sum(p.tiempo_espera() for p in terminados) / len(terminados)
            print("\n=== ESTADÍSTICAS ===")
            print(f"Procesos terminados: {len(terminados)}")
            print(f"Tiempo promedio de espera: {tiempo_promedio_espera:.2f} segundos")
            print(f"Procesos en RAM: {len(self.recursos_sistema['RAM'].procesos_asignados)}")
            print(f"Procesos en Memoria Virtual: {len(self.memoria_virtual)}")
            print(f"Utilización RAM: {(len(self.recursos_sistema['RAM'].procesos_asignados) / self.recursos_sistema['RAM'].capacidad) * 100:.1f}%")
            print(f"Utilización MV: {(len(self.memoria_virtual) / self.recursos_sistema['MV'].capacidad) * 100:.1f}%")