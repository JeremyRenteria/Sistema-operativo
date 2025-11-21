# recurso.py
class Recurso:
    def __init__(self, nombre, tipo, capacidad=1):
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.capacidad_disponible = capacidad
        self.procesos_asignados = []

    def asignar_a_proceso(self, proceso):
        if self.capacidad_disponible > 0:
            self.procesos_asignados.append(proceso)
            self.capacidad_disponible -= 1
            return True
        return False

    def liberar(self, proceso=None):
        if proceso and proceso in self.procesos_asignados:
            self.procesos_asignados.remove(proceso)
            self.capacidad_disponible += 1
        elif proceso is None:
            self.capacidad_disponible = self.capacidad
            self.procesos_asignados.clear()

    def esta_disponible(self):
        return self.capacidad_disponible > 0

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - Disponible: {self.capacidad_disponible}/{self.capacidad}"