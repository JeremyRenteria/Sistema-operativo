import time
from sistemaoperativo import GestorTareas

def main():
    gestor = GestorTareas()
    
    print("=== SISTEMA OPERATIVO - GESTOR DE TAREAS ===")
    print("Comandos disponibles:")
    print("1. crear <nombre> <prioridad> [tiempo]")
    print("2. eliminar <pid>")
    print("3. listar")
    print("4. recursos")
    print("5. asignar <pid> <recurso>")
    print("6. ejecutar")
    print("7. auto <n>")
    print("8. stats")
    print("9. salir\n")

    while True:
        try:
            comando = input("SO> ").strip().split()
            if not comando:
                continue

            if comando[0] == "crear":
                if len(comando) >= 3:
                    nombre = comando[1]
                    prioridad = int(comando[2])
                    tiempo = int(comando[3]) if len(comando) > 3 else 5
                    gestor.crear_proceso(nombre, prioridad, tiempo)
                else:
                    print("Uso: crear <nombre> <prioridad> [tiempo]")

            elif comando[0] == "eliminar":
                pid = int(comando[1])
                gestor.eliminar_proceso(pid)

            elif comando[0] == "listar":
                gestor.listar_procesos()

            elif comando[0] == "recursos":
                gestor.listar_recursos()

            elif comando[0] == "asignar":
                pid = int(comando[1])
                recurso = comando[2]
                gestor.asignar_recurso_a_proceso(pid, recurso)

            elif comando[0] == "ejecutar":
                gestor.ejecutar_ciclo()

            elif comando[0] == "auto":
                ciclos = int(comando[1])
                for i in range(ciclos):
                    print(f"\n--- Ciclo {i+1} ---")
                    gestor.ejecutar_ciclo()
                    time.sleep(0.5)

            elif comando[0] == "stats":
                gestor.estadisticas()

            elif comando[0] == "salir":
                print("Terminando sistema operativo...")
                break

            else:
                print("Comando no reconocido")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
