class Pedido:
    def __init__(self, id, mesa_id, trabajador_id, fecha_hora, estado, direccion, numero_contacto, nombre_cliente, tipo_pedido, tiempo_llegada=None, tipo_pago=None):
        self.id = id
        self.mesa_id = mesa_id
        self.trabajador_id = trabajador_id
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.direccion = direccion
        self.numero_contacto = numero_contacto
        self.nombre_cliente = nombre_cliente
        self.tipo_pedido = tipo_pedido
        self.tiempo_llegada = tiempo_llegada  
        self.tipo_pago = tipo_pago
