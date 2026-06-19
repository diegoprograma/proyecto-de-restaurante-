"""
Módulo de la Vista - Renderizado estético por consola mediante la librería 'rich'.
"""
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class VistaConsola:
    def __init__(self):
        self.console = Console()

    def mostrar_menu(self):
        """Pinta el panel del menú interactivo en la consola limpia."""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(
            Panel.fit(" [bold green]CONTROL DE CAJA Y FIADOS - RESTAURANTE[/bold green]", border_style="blue")
        )
        print("1. Registrar Venta Diaria (Efectivo)")
        print("2. Registrar Gasto (Proveedores, compras, servicios)")
        print("3. Fiar Almuerzo / Consumo (Cuenta de Cliente)")
        print("4. Recibir Pago de Crédito (Liquidación / Abono)")
        print("5. Ver Reporte de Caja de Hoy")
        print("6. Ver Relación de Almuerzos de un Cliente")
        print("7. Salir")

    def solicitar_opcion(self):
        return input("\nSeleccione una opción: ").strip()

    def solicitar_datos_transaccion(self, tipo_movimiento: str):
        self.console.print(f"\n[bold blue] Registrar {tipo_movimiento}:[/bold blue]")
        desc = input("Descripción del concepto: ").strip()
        while True:
            try:
                monto = float(input("Monto en pesos ($): ").strip())
                return desc, monto
            except ValueError:
                self.console.print("[red] Error: Ingrese un valor numérico válido.[/red]")

    def solicitar_datos_fiado(self):
        self.console.print("\n[bold yellow] Datos del Almuerzo Fiado:[/bold yellow]")
        nombre = input("Nombre del Cliente: ").strip()
        plato = input("Detalle del Plato (Ej: Almuerzo Corriente): ").strip()
        while True:
            try:
                precio = float(input("Precio acordado ($): ").strip())
                return nombre, plato, precio
            except ValueError:
                self.console.print("[red] Error: Ingrese un valor numérico para el precio.[/red]")

    def solicitar_datos_abono(self):
        self.console.print("\n[bold green] Registrar Abono / Pago:[/bold green]")
        nombre = input("Nombre del Cliente: ").strip()
        while True:
            try:
                monto = float(input("Monto del dinero recibido ($): ").strip())
                return nombre, monto
            except ValueError:
                self.console.print("[red] Error: Ingrese un valor numérico para el abono.[/red]")

    def solicitar_nombre_cliente(self):
        return input("\nEscribe el nombre del cliente a consultar: ").strip()

    def mostrar_mensaje(self, mensaje: str):
        print(f"\n{mensaje}")

    def mostrar_reporte_caja(self, ingresos: float, gastos: float, balance: float):
        """Muestra de forma tabulada el resumen financiero diario."""
        table = Table(title=" REPORTE DE CAJA DIARIA", title_style="bold magenta")
        table.add_column("Concepto Financiero", justify="left", style="cyan")
        table.add_column("Total Acumulado", justify="right", style="green")
        
        table.add_row("(+) Total Ventas / Ingresos", f"${ingresos:,.0f}")
        table.add_row("(-) Total Gastos / Egresos", f"${gastos:,.0f}")
        
        color_balance = "green" if balance >= 0 else "red"
        table.add_row("[bold]Balance Neto en Caja[/bold]", f"[bold {color_balance}]${balance:,.0f}[/bold {color_balance}]")
        self.console.print(table)

    def mostrar_historial_cliente(self, cliente):
        """Muestra detalladamente la libreta cronológica de créditos de un cliente."""
        table = Table(title=f" Historial de Créditos: {cliente.nombre}", title_style="bold yellow")
        table.add_column("Fecha / Hora de Consumo", justify="center", style="cyan")
        table.add_column("Detalle del Menú", justify="left", style="white")
        table.add_column("Valor Unitario", justify="right", style="red")
        
        for almuerzo in cliente.historial_almuerzos:
            fecha_str = almuerzo["fecha_hora"].strftime("%d/%m/%Y %H:%M:%S")
            table.add_row(fecha_str, almuerzo["plato"], f"${almuerzo['valor']:,.0f}")
            
        self.console.print(table)
        self.console.print(f"\n[bold red] Total Deuda Pendiente a la Fecha: ${cliente.total_deuda:,.0f}[/bold red]")