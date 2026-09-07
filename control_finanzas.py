import json
import os

ARCHIVO_DATOS = "transacciones.json"


class GestorFinanzas:

    def __init__(self):
        self.transacciones = {}
        self.siguiente_id = 1
        self.cargar_desde_archivo()

    def agregar_transaccion(self, tipo, categoria, monto, descripcion):
        if tipo != "ingreso" and tipo != "gasto":
            print("El tipo debe ser 'ingreso' o 'gasto'")
        elif monto <= 0:
            print("El monto debe ser mayor a cero")
        else:
            self.transacciones[self.siguiente_id] = {
                "tipo": tipo,
                "categoria": categoria,
                "monto": monto,
                "descripcion": descripcion,
            }
            print("Se ha registrado la transaccion correctamente")
            self.siguiente_id += 1
            self.guardar_en_archivo()

    def eliminar_transaccion(self, id_transaccion):
        if self.transacciones.get(id_transaccion) is None:
            print("No existe una transaccion con ese id")
        else:
            del self.transacciones[id_transaccion]
            print("Se ha eliminado la transaccion")
            self.guardar_en_archivo()

    def calcular_balance(self):
        balance = 0
        for t in self.transacciones.values():
            if t["tipo"] == "ingreso":
                balance += t["monto"]
            else:
                balance -= t["monto"]
        return balance

    def mostrar_historial(self):
        if not self.transacciones:
            print("No hay transacciones registradas")
        else:
            print("Id   | Tipo     | Categoria      | Monto      | Descripcion")
            for id_transaccion, t in self.transacciones.items():
                print(id_transaccion, " | ", t["tipo"], " | ", t["categoria"], " | ", t["monto"], " | ", t["descripcion"])

    def mostrar_balance(self):
        print("Balance actual: ", self.calcular_balance())

    def guardar_en_archivo(self):
        datos = {
            "siguiente_id": self.siguiente_id,
            "transacciones": self.transacciones,
        }
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def cargar_desde_archivo(self):
        if not os.path.exists(ARCHIVO_DATOS):
            return
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.siguiente_id = datos.get("siguiente_id", 1)
        transacciones_guardadas = datos.get("transacciones", {})
        # las llaves se guardan como texto en el JSON, hay que volverlas enteros
        self.transacciones = {int(id_t): valor for id_t, valor in transacciones_guardadas.items()}


gestor = GestorFinanzas()
print("Control de finanzas personales")
while True:
    print("Menu de opciones")
    print("1. Agregar transaccion")
    print("2. Eliminar transaccion")
    print("3. Ver historial")
    print("4. Ver balance")
    print("5. Salir")
    opcion_seleccionada = int(input("Ingrese la opcion deseada: "))

    if opcion_seleccionada == 1:
        tipo = input("Tipo de transaccion (ingreso/gasto): ")
        categoria = input("Categoria: ")
        monto = float(input("Monto: "))
        descripcion = input("Descripcion: ")
        gestor.agregar_transaccion(tipo, categoria, monto, descripcion)
    elif opcion_seleccionada == 2:
        id_transaccion = int(input("Ingrese el id de la transaccion a eliminar: "))
        gestor.eliminar_transaccion(id_transaccion)
    elif opcion_seleccionada == 3:
        gestor.mostrar_historial()
    elif opcion_seleccionada == 4:
        gestor.mostrar_balance()
    elif opcion_seleccionada == 5:
        break
    else:
        print("Seleccione una opcion valida")
