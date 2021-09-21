import csv
from datetime import date, datetime
from . import FICHERO

class ValidationError(Exception):
    pass


class Movimiento():
    def __init__(self, diccionario):
        self.errores = []
        try:
            self.fecha = date.fromisoformat(diccionario["fecha"])
            ahora = datetime.now()
            if self.fecha.strftime("%Y%m%d") > ahora.strftime("%Y%m%d"):
                self.errores.append("La fecha no puede ser superior a la actual")
        except ValueError:
            self.errores.append("Formato de fecha")

        self.concepto = diccionario["concepto"]
        if self.concepto == "":
            self.errores.append("Informe el concepto")

        try:
            self.es_ingreso = diccionario["ingreso_gasto"]
        except KeyError:
            self.errores.append("Informe tipo de movimiento (ingreso/gasto)")

        try:
            self.cantidad = float(diccionario["cantidad"])
            if self.cantidad <=0:
                self.errores.append("Cantidad debe ser positiva")
        except ValueError:
            self.errores.append("Cantidad debe ser un número")



class ListaMovimientos():
    def __init__(self):
        self.movimientos = []

    def leer(self):
        self.movimientos = []
        fichero = open(FICHERO, "r")
        dreader = csv.DictReader(fichero)
        for linea in dreader:
            self.movimientos.append(linea)
        fichero.close()

    def escribir(self):
        if len(self.movimientos) == 0:
            return

        fichero = open(FICHERO, "w")
        #nombres_campo = ["fecha", "concepto", "ingreso_gasto", "cantidad"]
        nombres_campo = list(self.movimientos[0].keys())
        dwriter = csv.DictWriter(fichero, fieldnames = nombres_campo)
        dwriter.writeheader()
        for movimiento in self.movimientos:
            dwriter.writerow(movimiento)
        fichero.close()

    def anyadir(self, valor):
        movimiento = {}
        movimiento['fecha'] = valor['fecha']
        movimiento['concepto'] = valor['concepto']
        movimiento['ingreso_gasto'] = valor['ingreso_gasto']
        movimiento['cantidad'] = valor['cantidad']
        self.movimientos.append(movimiento)