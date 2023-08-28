# ATMFacilito

ATMFacilito (Cajero automático desarrollado en Python)

## Desarrollado 🔥 por:

- Simón Maquilón https://www.linkedin.com/in/simonmaquilon
- Vicente Ciampa https://www.linkedin.com/in/vciampa

## ✅ Uso de la aplicación:

- Crear el archivo **.env** en el ruta raíz del proyecto, ejemplo:

  ```
  DATABASE=./data/atmfacilito.db
  SECRET_KEY=ef8e207c4ffb339d97747fed86b86e9a94b8387e
  ```

- Crear un ambiente de Python, ejemplo usando venv:

  ```
  python -m venv venv
  ```

- **_Activar el ambiente e instalar las dependencias:_**

  ```
  source ./env/bin/activate

  pip install -r requirements.txt
  ```

- Ejecutar el proyecto **Flask** (http://127.0.0.1:3000):

  ```
  python main.py
  ```

### ✅ Apertura de una Cuenta

Formulario básico sin validación para que los participantes puedan crear sus cuentas de prueba.

### ✅ Retirar de dinero vía QR

Este módulo permite retirar dinero desde un cajero automático mediante un código QR, generado por la aplicación.

### ✅ Depósito de dinero

Permite depositar la cantidad de dinero que ingreses mediante el teclado.

### ✅ Panel - Mis Cuentas

Permite consultar tu información de cuenta en tiempo real.
