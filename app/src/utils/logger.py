from logging import basicConfig, getLogger, ERROR, INFO, WARNING
from json import dumps

niveis_log = {
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR
}


def log_object(message: str, salesforce_id: str, **kwargs):
    return dumps({
        'SalesforceID': salesforce_id,
        'Message': message,
        "Data": kwargs
    }, ensure_ascii=False)


def configure_logs():
    nivel_log = 'INFO'
    root = getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    data = dumps({
        'Appname': 'FremotaBuscaIdCliente',
        'Filename': '%(filename)s',
        'LogLevel': '%(levelname)s',
        'Payload': '%(message)s',
        'Timestamp': '%(asctime)s',
        'Function': '%(funcName)s',
        'Thread': '%(threadName)s'
    })
    data = data.replace('"%(message)s"', '%(message)s')
    basicConfig(format=data)
    getLogger().setLevel(niveis_log[nivel_log])
    getLogger("boto3").setLevel(WARNING)
    getLogger("botocore").setLevel(WARNING)
