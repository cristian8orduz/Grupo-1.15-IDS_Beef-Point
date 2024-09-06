# Beef Point Restaurant POS

Este repositorio está destinado al desarrollo del aplicativo relacionado con el Trabajo con Empresa realizado por el Grupo 1.15 de la asignatura Ingeniería de Software, del semestre 2024-1S de la carrera Ingeniería de Sistemas e Informática de la Universidad Nacional de Colombia Sede Medellín. El cuál se realizará en conjunto con el restaurante Beef Point. El Grupo 1.15 está conformado por Samuel Gutiérrez (Product Owner Proxy), Cristian Plazas (Scrum Master) y Santiago Lopez (Developer).

## Descripción

Esta aplicación es un sistema de punto de venta (POS) para el restaurante Beef Point. Permite gestionar pedidos tanto en mesa como a domicilio, realizar seguimiento de los pedidos y mantener un historial de los mismos. El sistema está desarrollado utilizando Python y Tkinter para la interfaz gráfica.

## Características

- **Gestión de Pedidos en Mesa**: Los trabajadores pueden crear, visualizar y confirmar pedidos en mesa.
- **Gestión de Pedidos a Domicilio**: Permite registrar pedidos a domicilio incluyendo la dirección y el número de contacto del cliente.
- **Historial de Pedidos**: Consulta los pedidos confirmados con todos los detalles, incluidos los productos y sus cantidades.
- **Gestión de Trabajadores**: Los trabajadores deben iniciar sesión para acceder al sistema, permitiendo un control más seguro y personalizado de los pedidos.

## Requisitos

Para poder ejecutar la aplicación, necesitarás tener instalados los siguientes componentes:

- **Python 3.x**: Asegúrate de tener Python instalado en tu máquina. Puedes descargarlo desde [aquí](https://www.python.org/downloads/).
- **Librerías requeridas**: Las librerías necesarias para ejecutar la aplicación son estándar en Python, como `tkinter` y `sqlite3`.

## Instalación

Sigue estos pasos para clonar y ejecutar el proyecto:

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tuusuario/beef-point-pos.git
    cd beef-point-pos/src
    ```

2. **Entrar a Ruta Proyecto**:
    ```bash
    cd src
    ```

3. **Instalar Liberias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecutar la aplicación**:
    ```bash
    python main.py
    ```

## Uso

1. **Iniciar Sesión**: Ingresa el usuario y contraseña de un trabajador registrado.
2. **Nuevo Pedido**: Crea un nuevo pedido seleccionando una mesa disponible.
3. **Pedido a Domicilio**: Crea un pedido a domicilio ingresando la dirección y el número de contacto.
4. **Historial de Pedidos**: Consulta los pedidos confirmados y sus detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama con tu función o mejora (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios necesarios y haz commit de los mismos (`git commit -m 'Agregar nueva funcionalidad'`).
4. Haz push de los cambios a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request en GitHub.

## Contacto

Para más información o preguntas sobre este proyecto, puedes contactar al Grupo 1.15:

- **Samuel Gutiérrez** - Product Owner Proxy
- **Cristian Plazas** - Scrum Master
- **Santiago Lopez** - Developer
