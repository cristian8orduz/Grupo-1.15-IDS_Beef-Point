class Pedido:
    def __init__(self, id, mesa_id, trabajador_id, fecha_hora, estado):
        self.id = id
        self.mesa_id = mesa_id
        self.trabajador_id = trabajador_id
        self.fecha_hora = fecha_hora
        self.estado = estado
