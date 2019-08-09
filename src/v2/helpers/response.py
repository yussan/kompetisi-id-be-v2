def apiResponse(status, message='', data={}):
    if not status:
        status = 500

    if not message:
        if status == 200:
            message = 'ok'
        elif status == 201:
            message = 'aksi sukses'
        elif status == 204:
            message = 'data kosong'
        elif status == 400:
            message = 'parameter tidak valid'
        else:
            message = 'sedang terjadi masalah'

    json_response = {
        'status': status,
        'message': message
    }

    if data:
        json_response.update(data)

    print("response", json_response)

    return json_response
