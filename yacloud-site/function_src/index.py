import json
import socket
import datetime

def handler(event, context):
    body = {
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'Backend service is running!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }