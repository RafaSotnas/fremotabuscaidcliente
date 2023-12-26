from logging import info, error
import json
from src.class_util import fremota_error
from src.dados_pessoa \
    import get_id_eq3_envolvidos
from guarda_segura \
    import token_sts
from src.utils.logger import configure_logs, log_object


def lambda_handler(event, context):
    configure_logs()
    payload_entrada = dict(event)
    salesforce_id = None
    # exec_ok, retorno = credential.get_secret()
    #
    # if exec_ok is True:
    salesforce_id = payload_entrada["codigo_processo_consumidor"]
    info(log_object("Inicio - Busca id EQ3 Cliente",
                    salesforce_id,
                    payloadentrada=event))

    exec_ok, retorno = token_sts.get_token_request()
    if not exec_ok:

        error(log_object('Erro - Busca id EQ3 Cliente: busca token sts',
                         salesforce_id,
                         detalhes=retorno))

        raise fremota_error(
            {
                "codigo": "ATV-CLI-011",
                "codigo_processo_consumidor":
                    event["codigo_processo_consumidor"],
                "msg": retorno,
            }
        )

    # else:
    #
    #     raise fremota_error(retorno)

    exec_ok, retorno = get_id_eq3_envolvidos(
        retorno,
        payload_entrada
    )

    if not exec_ok:

        error(log_object('Erro - Busca id EQ3 Cliente: busca id eq3',
                         salesforce_id,
                         detalhes=retorno))

        raise fremota_error(
            {
                "codigo": "ATV-CLI-010",
                "codigo_processo_consumidor":
                    event["codigo_processo_consumidor"],
                "msg": retorno,
            }
        )

    info(log_object("Fim - Busca id EQ3 Cliente",
                    salesforce_id,
                    payloadsaida=payload_entrada))

    return json.dumps(payload_entrada)
