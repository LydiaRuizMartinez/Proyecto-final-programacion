import funciones as f

COLOR_VERDE = "\033[1;32m"
COLOR_ROJO = "\033[1;31m"
COLOR_DEFECTO = "\033[0m"

OK = COLOR_VERDE + "OK" + COLOR_DEFECTO
ERROR = COLOR_ROJO + "ERROR" + COLOR_DEFECTO

print("Ejecutando tests....")

try:
    print("- Función leer_marcador(): ", end = "") 
    score_dict = f.leer_marcador()
    print(f"{OK}")
except Exception as error:
    print(f"{ERROR}")
    print(error)

try:
    print("- Función guardar_marcador(): ", end = "") 
    f.guardar_marcador(score_dict)
    print(f"{OK}")
except Exception as error:
    print(f"{ERROR}")
    print(error)

print("Fin de los tests")