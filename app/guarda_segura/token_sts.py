'''
    Função para gerar token baseado no client_id e client_secret

    Projeto: Assinatura Digital | Plataforma Agnostica
    Squad2020: Inovativos - Moeda Nacional
    Criado por: Rafael Oliveira
    Data : jun/2022

'''

from requests import post
from json import loads

import os
from src.monta_erro \
    import payload_erro

__URL_BASE__ = os.environ.get('UrlTokenBase')
__URL_ENDPOINT__ = os.environ.get('UrlTokenEndPoint')
__SSL_ITAU_CER__ = os.environ.get('SSL_CERT_FILE')

__CLIENT_ID_ARN = os.environ.get('ClientId')
__CLIENT_SECRET_ARN = os.environ.get('ClientSecret')


def get_token_request():

    print('LOGX funcao get_token_request')
    print('LOGX Client:', __CLIENT_ID_ARN)
    print('LOGX Secret:', __CLIENT_SECRET_ARN)

    print('LOGX pegando info do cert:', __SSL_ITAU_CER__)

    payload = {
        "grant_type": "client_credentials",
        "client_id": __CLIENT_ID_ARN,
        "client_secret": __CLIENT_SECRET_ARN
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-itau-flowID': '10',
        'x-itau-correlationID': '15'
    }

    try:

        url = f'https://{__URL_BASE__}{__URL_ENDPOINT__}'

        response = post(
            url=url,
            data=payload,
            headers=headers,
            verify=__SSL_ITAU_CER__
        )

        json_token = loads(response.content)

    except Exception as e:

        erro = payload_erro(
            {'Exception': [e]},
            'get_token_request()'
        )
        return False, dict(erro)

    else:

        return True, dict(json_token)
