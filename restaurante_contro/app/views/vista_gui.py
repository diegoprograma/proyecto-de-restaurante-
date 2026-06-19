"""
Vista gráfica con tkinter para el control del restaurante.
Permite registrar ingresos, gastos y exportar el reporte a CSV.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class VistaGUI:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Control de Caja del Restaurante")
        self.ventana.geometry("900x520")
        self.ventana.configure(bg="#f4f7f9")
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Marco superior de resumen
        marco_resumen = ttk.Frame(self.ventana, padding=12)
        marco_resumen.pack(fill="x")

        ttk.Label(marco_resumen, text="Resumen diario", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        self.lbl_ingresos = ttk.Label(marco_resumen, text="Ingresos: $0", foreground="#1b5e20")
        self.lbl_ingresos.pack(anchor="w")
        self.lbl_gastos = ttk.Label(marco_resumen, text="Gastos: $0", foreground="#b71c1c")
        self.lbl_gastos.pack(anchor="w")
        self.lbl_balance = ttk.Label(marco_resumen, text="Balance: $0", foreground="#0d47a1")
        self.lbl_balance.pack(anchor="w")

        # Formulario
        marco_form = ttk.LabelFrame(self.ventana, text="Registrar operación", padding=10)
        marco_form.pack(fill="x", padx=12, pady=8)

        ttk.Label(marco_form, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tipo_var = tk.StringVar(value="Ingreso")
        self.combo_tipo = ttk.Combobox(
            marco_form,
            textvariable=self.tipo_var,
            values=["Ingreso", "Gasto", "Fiado", "Abono"],
            state="readonly",
            width=15,
        )
        self.combo_tipo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.descripcion = ttk.Entry(marco_form, width=40)
        self.descripcion.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(marco_form, text="Monto:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.monto = ttk.Entry(marco_form, width=20)
        self.monto.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(marco_form, text="Cliente (si aplica):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.cliente = ttk.Entry(marco_form, width=25)
        self.cliente.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(marco_form, text="Plato (si aplica):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.plato = ttk.Entry(marco_form, width=25)
        self.plato.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(marco_form, text="Guardar", command=self.guardar_operacion).grid(row=5, column=1, sticky="w", padx=5, pady=10)
        ttk.Button(marco_form, text="Exportar CSV", command=self.exportar_reporte).grid(row=5, column=2, sticky="w", padx=5, pady=10)

        # Tabla de movimientos
        marco_tabla = ttk.LabelFrame(self.ventana, text="Movimientos", padding=10)
        marco_tabla.pack(fill="both", expand=True, padx=12, pady=8)

        columnas = ("Tipo", "Descripción", "Monto")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Descripción", text="Descripción")
        self.tabla.heading("Monto", text="Monto")
        self.tabla.column("Tipo", width=100)
        self.tabla.column("Descripción", width=450)
        self.tabla.column("Monto", width=120, anchor="e")
        self.tabla.pack(fill="both", expand=True)

    def guardar_operacion(self):
        try:
            tipo = self.tipo_var.get()
            desc = self.descripcion.get().strip()
            monto = float(self.monto.get().strip())

            if not desc:
                raise ValueError("La descripción no puede estar vacía.")

            if tipo == "Ingreso":
                self.controlador.registrar_ingreso(desc, monto)
            elif tipo == "Gasto":
                self.controlador.registrar_gasto(desc, monto)
            elif tipo == "Fiado":
                cliente = self.cliente.get().strip()
                plato = self.plato.get().strip()
                if not cliente or not plato:
                    raise ValueError("Debe indicar cliente y plato para un fiado.")
                self.controlador.registrar_fiado(cliente, plato, monto)
            elif tipo == "Abono":
                cliente = self.cliente.get().strip()
                if not cliente:
                    raise ValueError("Debe indicar el cliente para registrar el abono.")
                self.controlador.registrar_abono(cliente, monto)
            else:
                raise ValueError("Tipo de operación inválido.")

            self.actualizar_resumen()
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Operación registrada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_reporte(self):
        try:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialfile="reporte_caja.csv",
                filetypes=[("Archivo CSV", "*.csv")],
            )
            if ruta:
                self.controlador.exportar_csv(ruta)
                messagebox.showinfo("Exportado", f"Archivo guardado en: {ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_resumen(self):
        resumen = self.controlador.obtener_resumen()
        self.lbl_ingresos.config(text=f"Ingresos: ${resumen['ingresos']:,.0f}")
        self.lbl_gastos.config(text=f"Gastos: ${resumen['gastos']:,.0f}")
        self.lbl_balance.config(text=f"Balance: ${resumen['balance']:,.0f}")

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for movimiento in self.controlador.modelo._movimientos:
            self.tabla.insert(
                "",
                "end",
                values=(movimiento["tipo"], movimiento["descripcion"], f"${movimiento['monto']:,.0f}"),
            )

    def iniciar(self):
        self.actualizar_resumen()
        self.actualizar_tabla()
        self.ventana.mainloop()
