"""
Módulo del Modelo - Gestión de Caja y Créditos del Restaurante.
Aplicando principios de POO, encapsulamiento y validación de datos.
"""
from datetime import datetime
import pandas as pd

class Cliente:
    """
    Representa a un cliente frecuente con cuenta de cobro/crédito en el restaurante.
    """
    def __init__(self, nombre: str):
        if not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self.nombre = nombre.strip()
        self._historial_almuerzos = []  # Atributo protegido (Encapsulamiento)
        self._total_deuda = 0.0

    def fiar_almuerzo(self, plato: str, valor: float):
        """Registra un consumo a crédito en la cuenta del cliente."""
        if valor <= 0:
            raise ValueError("El precio del almuerzo debe ser mayor a cero.")
        
        self._historial_almuerzos.append({
            "plato": plato.strip(),
            "valor": valor,
            "fecha_hora": datetime.now()
        })
        self._total_deuda += valor

    def registrar_abono(self, monto: float):
        """Reduce la deuda pendiente tras un pago en efectivo."""
        if monto <= 0:
            raise ValueError("El monto del abono debe ser mayor a cero.")
        if monto > self._total_deuda:
            raise ValueError(f"El abono (${monto:,.0f}) supera la deuda actual (${self._total_deuda:,.0f}).")
        
        self._total_deuda -= monto

    @property
    def total_deuda(self):
        """Getter para acceder de forma segura a la deuda total."""
        return self._total_deuda

    @property
    def historial_almuerzos(self):
        """Getter para obtener la lista de consumos del cliente."""
        return self._historial_almuerzos


class CajaDiaria:
    """
    Gestiona el flujo de caja diario del restaurante (Ingresos, Gastos y Clientes).
    """
    def __init__(self):
        self._ingresos = 0.0
        self._gastos = 0.0
        self._clientes = {}  # Diccionario para mapear nombres con objetos Cliente
        self._movimientos = []  # Historial detallado de movimientos para reportes y exportación

    def registrar_ingreso(self, descripcion: str, monto: float):
        """Aumenta el capital de la caja por una venta en efectivo o abono."""
        if monto <= 0:
            raise ValueError("El monto del ingreso debe ser mayor a cero.")
        self._ingresos += monto
        self._movimientos.append({
            "tipo": "Ingreso",
            "descripcion": descripcion.strip(),
            "monto": float(monto)
        })

    def registrar_gasto(self, descripcion: str, monto: float):
        """Descuenta dinero de la caja para pagar proveedores o servicios."""
        if monto <= 0:
            raise ValueError("El monto del gasto debe ser mayor a cero.")
        self._gastos += monto
        self._movimientos.append({
            "tipo": "Gasto",
            "descripcion": descripcion.strip(),
            "monto": float(monto)
        })

    def registrar_almuerzo_fiado(self, nombre_cliente: str, plato: str, precio: float):
        """Asigna un almuerzo fiado a un cliente existente o nuevo."""
        nombre_normalizado = nombre_cliente.strip().capitalize()
        if nombre_normalizado not in self._clientes:
            self._clientes[nombre_normalizado] = Cliente(nombre_normalizado)

        self._clientes[nombre_normalizado].fiar_almuerzo(plato, precio)
        self._movimientos.append({
            "tipo": "Fiado",
            "descripcion": f"{nombre_normalizado} - {plato.strip()}",
            "monto": float(precio)
        })

    def registrar_abono_cliente(self, nombre_cliente: str, monto: float):
        """Procesa el pago de un cliente disminuyendo su cuenta e ingresando efectivo a caja."""
        nombre_normalizado = nombre_cliente.strip().capitalize()
        if nombre_normalizado not in self._clientes:
            raise ValueError(f"El cliente '{nombre_cliente}' no se encuentra registrado.")

        # Primero modifica la cuenta del cliente (puede lanzar ValueError)
        self._clientes[nombre_normalizado].registrar_abono(monto)
        # Si tiene éxito, el dinero ingresa formalmente a la caja del restaurante
        self.registrar_ingreso(f"Abono Crédito: {nombre_normalizado}", monto)

    def obtener_balance(self):
        """Calcula el balance neto actual."""
        return self._ingresos - self._gastos

    def exportar_resumen_csv(self, ruta_archivo: str):
        """Exporta el resumen de caja y los movimientos detallados a un archivo CSV."""
        movimientos_df = pd.DataFrame(self._movimientos)
        if movimientos_df.empty:
            movimientos_df = pd.DataFrame(columns=["tipo", "descripcion", "monto"])

        resumen_df = pd.DataFrame([
            {"tipo": "Resumen", "descripcion": "Total Ingresos", "monto": self._ingresos},
            {"tipo": "Resumen", "descripcion": "Total Gastos", "monto": self._gastos},
            {"tipo": "Resumen", "descripcion": "Balance Neto", "monto": self.obtener_balance()} 
        ])

        export_df = pd.concat([movimientos_df, resumen_df], ignore_index=True)
        export_df.to_csv(ruta_archivo, index=False, encoding="utf-8-sig")

    def obtener_cliente(self, nombre: str):
        """Retorna el objeto Cliente si existe en los registros."""
        return self._clientes.get(nombre.strip().capitalize(), None)

    @property
    def ingresos(self):
        return self._ingresos

    @property
    def gastos(self):
        return self._gastos