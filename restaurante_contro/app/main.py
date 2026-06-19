"""
Archivo Principal de Arranque del Software del Restaurante.
Configura el sys.path para salvaguardar la arquitectura de módulos.
"""
import sys
import os

# Asegura de forma dinámica la raíz para evitar fallos de importación de módulos vecinos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.caja import CajaDiaria
from app.controllers.caja_controller import CajaController
from app.views.vista_gui import VistaGUI

def main():
    # Inicialización del modelo de datos unificado
    modelo_caja = CajaDiaria()
    # Inyección del modelo al controlador
    controlador = CajaController(modelo_caja)
    # Ejecución de la versión gráfica
    vista_gui = VistaGUI(controlador)
    controlador.vista = vista_gui
    controlador.iniciar()

if __name__ == "__main__":
    main()