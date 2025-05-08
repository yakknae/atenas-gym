# Atenas - Sistema de Gestión de Atenas gym

### Atenas Gym es un sistema de gestión integral diseñado para administrar eficientemente las operaciones de un gimnasio. Este proyecto permite gestionar socios, planes de entrenamiento, planes sociales, asistencias, pagos y más, brindando una solución completa para optimizar la administración del gimnasio.

### Menu principal

![image](https://github.com/user-attachments/assets/7b60b99d-f223-4d67-905c-2c6dd4ea338d)

### Formularios de dar de alta socios

![image](https://github.com/user-attachments/assets/6f4df892-e94c-40f5-9b75-3e8a3ab571f0)

### Planilla de socios

![image](https://github.com/user-attachments/assets/f6a2cd46-ca5e-4c50-812a-6fcf66e41568)

## Características principales

- **Gestión de Socios:** Registra, actualiza y asigna planes a socios.
- **Planes de Entrenamiento:** Crea y administra planes con detalles como precio y duración.
- **Planes Sociales:** Gestiona planes especiales para grupos específicos.
- **Control de Asistencias:** Registra y consulta asistencias diarias.
- **Gestión de Pagos:** Administra cobros mensuales y estados de pago.
- **Interfaz Intuitiva:** Diseño limpio y fácil de usar con tablas dinámicas.

## Requisitos

## Instalación

- Instalar dependencias

  > pip install -r requirements.txt

## Configurar la base de datos

> python -m app.database1

- Esto creará las tablas necesarias y cargará los datos iniciales.

## Iniciar el servidor

> uvicorn app.main:app --reload

## Detener el servidor

- Para detener el servidor, presiona `CTRL+C` en la terminal donde se está ejecutando.
