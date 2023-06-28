from delivery.core.usecases.socket_io import SocketIO


def dictfetchall(cursor):

    columns = [col[0] for col in cursor.description]

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dispatch_event_socket(tp_evento=None, payload=None):

    data = {"event": tp_evento, "payload": payload}

    web_socket = SocketIO()
    web_socket.execute(data)
