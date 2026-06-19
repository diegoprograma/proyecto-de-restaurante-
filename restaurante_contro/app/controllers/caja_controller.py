"""
Módulo del Controlador - Intermediario del flujo arquitectónico MVC.
"""
from app.views.vista_consola import VistaConsola

class CajaController:
    def __init__(self, modelo, vista=None):
        self.modelo = modelo
        self.vista = vista or VistaConsola()

    def iniciar(self):
        """Inicia el flujo de la aplicación, usando la vista configurada."""
        if hasattr(self.vista, "iniciar"):
            self.vista.iniciar()
            return

        # Fallback para la versión por consola.
        while True:
            self.vista.mostrar_menu()
            opcion = self.vista.solicitar_opcion()

            if opcion == "1":
                desc, monto = self.vista.solicitar_datos_transaccion("Ingreso / Venta")
                try:
                    self.modelo.registrar_ingreso(desc, monto)
                    self.vista.mostrar_mensaje(f" Venta registrada con éxito: {desc} por ${monto:,.0f}")
                except ValueError as e:
                    self.vista.mostrar_mensaje(f" Error en datos: {e}")

            elif opcion == "2":
                desc, monto = self.vista.solicitar_datos_transaccion("Egreso / Gasto")
                try:
                    self.modelo.registrar_gasto(desc, monto)
                    self.vista.mostrar_mensaje(f" Gasto registrado con éxito: {desc} por ${monto:,.0f}")
                except ValueError as e:
                    self.vista.mostrar_mensaje(f" Error en datos: {e}")

            elif opcion == "3":
                nombre, plato, precio = self.vista.solicitar_datos_fiado()
                try:
                    self.modelo.registrar_almuerzo_fiado(nombre, plato, precio)
                    self.vista.mostrar_mensaje(f" Almuerzo colgado a la cuenta de {nombre} correctamente.")
                except ValueError as e:
                    self.vista.mostrar_mensaje(f" Error en datos: {e}")

            elif opcion == "4":
                nombre, monto = self.vista.solicitar_datos_abono()
                try:
                    self.modelo.registrar_abono_cliente(nombre, monto)
                    self.vista.mostrar_mensaje(f" Abono de ${monto:,.0f} procesado para {nombre}. Dinero ingresado a caja.")
                except ValueError as e:
                    self.vista.mostrar_mensaje(f" Error en operación: {e}")

            elif opcion == "5":
                balance = self.modelo.obtener_balance()
                self.vista.mostrar_reporte_caja(self.modelo.ingresos, self.modelo.gastos, balance)

            elif opcion == "6":
                nombre = self.vista.solicitar_nombre_cliente()
                cliente = self.modelo.obtener_cliente(nombre)
                if cliente:
                    self.vista.mostrar_historial_cliente(cliente)
                else:
                    self.vista.mostrar_mensaje(f" El cliente '{nombre}' no registra cuentas pendientes en el sistema.")

            elif opcion == "7":
                self.vista.mostrar_mensaje("¡Muchas gracias por utilizar el sistema del restaurante! Saliendo...")
                break

            input("\nPresiona [Enter] para continuar en el menú...")

    def registrar_ingreso(self, descripcion, monto):
        self.modelo.registrar_ingreso(descripcion, monto)

    def registrar_gasto(self, descripcion, monto):
        self.modelo.registrar_gasto(descripcion, monto)

    def registrar_fiado(self, nombre, plato, precio):
        self.modelo.registrar_almuerzo_fiado(nombre, plato, precio)

    def registrar_abono(self, nombre, monto):
        self.modelo.registrar_abono_cliente(nombre, monto)

    def obtener_resumen(self):
        return {
            "ingresos": self.modelo.ingresos,
            "gastos": self.modelo.gastos,
            "balance": self.modelo.obtener_balance()
        }

    def exportar_csv(self, ruta):
        self.modelo.exportar_resumen_csv(ruta)
