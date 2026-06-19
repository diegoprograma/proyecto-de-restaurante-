"""
Suite de Pruebas Unitarias Automatizadas con Pytest.
"""
import pytest
from app.models.caja import CajaDiaria, Cliente

def test_exportar_resumen_csv_crea_archivo(tmp_path):
    """Caso válido adicional: verifica que el sistema pueda exportar un resumen a CSV."""
    caja = CajaDiaria()
    caja.registrar_ingreso("Venta del día", 50000)
    caja.registrar_gasto("Compra de ingredientes", 12000)
    caja.registrar_almuerzo_fiado("Ana", "Menú del día", 15000)

    archivo = tmp_path / "resumen_caja.csv"
    caja.exportar_resumen_csv(str(archivo))

    assert archivo.exists()
    contenido = archivo.read_text(encoding="utf-8")
    assert "Venta del día" in contenido
    assert "50000" in contenido
    assert "12000" in contenido
    assert "38000" in contenido

def test_registrar_ingreso_y_balance_valido():
    """Caso Válido 1: Valida sumas lógicas de ingresos y el cálculo neto del balance."""
    caja = CajaDiaria()
    caja.registrar_ingreso("Venta de 3 Almuerzos Corrientes", 36000)
    caja.registrar_gasto("Compra de verduras en la plaza", 10000)
    
    assert caja.ingresos == 36000
    assert caja.gastos == 10000
    assert caja.obtener_balance() == 26000

def test_registrar_almuerzo_fiado_cliente():
    """Caso Válido 2: Valida la instanciación de clientes y acumulación de créditos."""
    caja = CajaDiaria()
    caja.registrar_almuerzo_fiado("Diego", "Almuerzo Ejecutivo", 16000)
    
    cliente = caja.obtener_cliente("Diego")
    assert cliente is not None
    assert cliente.nombre == "Diego"
    assert cliente.total_deuda == 16000
    assert len(cliente.historial_almuerzos) == 1

def test_monto_negativo_lanza_error():
    """Caso Inválido Obligatorio: Verifica el disparo de excepciones ante datos erróneos."""
    caja = CajaDiaria()
    with pytest.raises(ValueError):
        # El sistema debe rechazar montos inválidos/negativos arrojando un ValueError
        caja.registrar_ingreso("Venta Inválida", -5000)