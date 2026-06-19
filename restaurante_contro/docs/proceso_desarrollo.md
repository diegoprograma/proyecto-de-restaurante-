# Proceso de desarrollo

## 1. Idea inicial
La idea del proyecto surgió de la necesidad de llevar un control ordenado de la caja y de las cuentas por cobrar en un restaurante. El objetivo era reemplazar el registro manual y reducir errores en ventas, gastos y pagos diferidos.

## 2. Análisis del problema
El sistema debía permitir al personal registrar ventas en efectivo, gastos del día, almuerzos fiados y abonos de clientes. También era importante visualizar el balance diario y consultar el historial de deuda de cada cliente.

## 3. Diseño de la solución
Se decidió organizar el proyecto con arquitectura MVC para separar responsabilidades. El modelo se encargó de la lógica financiera, la vista mostró la información al usuario y el controlador unió ambos componentes. Además, se definieron clases como `CajaDiaria` y `Cliente` para representar la lógica del negocio.

## 4. Implementación
Durante la implementación se crearon las clases principales del modelo, se conectó la lógica con una interfaz gráfica y también se dejó una versión por consola para pruebas y uso básico. Se incorporaron validaciones para evitar montos inválidos y se agregó la posibilidad de exportar reportes a CSV.

## 5. Pruebas
Se realizaron pruebas automatizadas con `pytest` para verificar el funcionamiento correcto de la caja, la creación de clientes, el cálculo del balance y el manejo de errores cuando se ingresan datos incorrectos.

## 6. Dificultades encontradas
Una de las principales dificultades fue mantener la lógica financiera consistente cuando un cliente hacía un abono, ya que esto afectaba tanto la deuda como el monto que debía registrarse en la caja. También fue necesario asegurar que la exportación de datos funcionara correctamente en distintos entornos.

## 7. Mejoras futuras
Como mejoras futuras se podrían agregar reportes semanales o mensuales, autenticación de usuarios para el control del sistema y almacenamiento persistente en base de datos para reemplazar los datos en memoria.
