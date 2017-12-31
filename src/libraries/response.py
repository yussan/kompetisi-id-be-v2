def api_response(status, message, data={}):
    if not status:
        status = 500

    if not message:
        if status == 200:
            message = 'ok'
        elif status == 201:
            message = 'aksi sukses'
        else:
            message = 'sedang terjadi masalah'

    json_response = {
        'status': status,
        'message': message
    }

    if status == 200 and not data:
        json_response.update(data)

    return json_response