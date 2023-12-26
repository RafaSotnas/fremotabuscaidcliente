'''
    Função para buscar os dados do cliente no EQ3

    Projeto: Assinatura Digital | Plataforma Agnostica
    Squad2020: Inovativos - Moeda Nacional
    Criado por: Rafael Oliveira
    Data : jun/2022

'''

import json
from requests import post, exceptions
from json import loads, dumps
import os
from src.monta_erro \
    import payload_erro

__URL_BASE_EQ3__ = os.environ.get('UrlBaseEQ3')
__URL_ENDPOINT_EQ3__ = os.environ.get('UrlEndPointEQ3')
__SSL_BUNDLE_CER__ = os.environ.get('SSL_CERT_FILE')

__ITAU_API_KEY__ = os.environ.get('ItauApiKey')
__ITAU_FLOW_ID__ = os.environ.get('ItauFlowID')
__APIGW_API_ID__ = os.environ.get('ApigwApiId')


def get_id_eq3_envolvidos(token_sts, payload: dict):
    """
    Busca o id do EQ3 dos envolvidos (contraparte, garantidorPF,
    garantidorPJ, vistador e observador) e anexa com a chave 'id_cliente'

    :param token_sts: objeto Token usado para consultar o endpoint do EQ3
    :param payload: informa um dict de payload com todos os envolvidos
    passados.

    :return: se tudo Ok o return é só True, mas se houver algum erro
             o return será False e será retornado um dict com o erro

    """

    retorno = {}
    erros = []

    cnpj = payload["cnpj_requisitante"]
    exec_ok, retorno = get_dados_by_cpf_cnpj(token_sts, cnpj, 'PJ')

    if exec_ok is True:
        payload["codigo_pessoa_requisitante"] = retorno['id_cliente']
        del payload["cnpj_requisitante"]
    else:
        erros.append(retorno)

    # Gerar ID EQ3 de garantidores / PJ
    if 'garantidores' in payload:
        for garantidor in payload["garantidores"]:

            cnpj = garantidor['cnpj']
            exec_ok, retorno = get_dados_by_cpf_cnpj(
                token_sts,
                cnpj,
                'PJ'
            )

            if exec_ok is True:
                garantidor["identificador_pessoa"] = {
                    "codigo_identificador_pessoa": retorno['id_cliente'],
                    "tipo_identificador_pessoa": "CODIGO_PESSOA"
                }
                del garantidor["cnpj"]
            else:
                erros.append(retorno)

    # Gerar ID EQ3 de participantes / PF
    if 'participantes' in payload:
        for participante in payload['participantes']:

            cpf = participante['cpf']
            exec_ok, retorno = get_dados_by_cpf_cnpj(
                token_sts,
                cpf,
                'PF'
            )

            cnpj_vinculado = participante["cnpj_pessoa_vinculada"]
            exec_ok_vinculado, retorno_vinculado = get_dados_by_cpf_cnpj(
                token_sts,
                cnpj_vinculado,
                'PJ'
            )

            if exec_ok is True:
                participante["identificador_pessoa"] = {
                    "codigo_identificador_pessoa": retorno['id_cliente'],
                    "tipo_identificador_pessoa": "CODIGO_PESSOA"
                }

                participante["codigo_pessoa_vinculada"] \
                    = retorno_vinculado["id_cliente"]
                del participante["cnpj_pessoa_vinculada"]
                del participante["cpf"]
            else:
                erros.append(retorno)

    print("PAYLOAD POSTERIOR: ", payload)

    return True if len(erros) == 0 else False, erros


# def busca_id_by_envolvido(token_sts,
#                           envolvidos: list,
#                           tipo: str,
#                           erros: list):
#     """
#     Buscar o ID do EQ3 dos objetos referente ao envolvido informado.
#     Os envolvidos que podem ser usados nesta função tem que ser uma
#     lista de objetos com a seguinte estrutura:
#     {
#         'nome': 'Rafael Oliveira',
#         'cpf': '1234567890',
#         'email': 'email@email.com'
#     }
#
#     :param token_sts: string Token usado para consultar o endpoint do EQ3.
#     :param envolvidos: informa a parte do payload com os envolvidos.
#     :param tipo: inica se o número informado em 'cpf_cnpj' é CPF ou CNPJ.
#                  Aceita PJ (default) = para CNPJ e PF = para CPF
#     :param erros: informa o list que conterá o erro se houver
#     """
#
#     for envolvido in envolvidos:
#
#         cpf = envolvido['cpf']
#         exec_ok, retorno = get_dados_by_cpf_cnpj(token_sts, cpf, tipo)
#
#         if exec_ok is True:
#             envolvido['idCliente'] = retorno['id_cliente']
#         else:
#
#             erros.append(retorno)


def get_dados_by_cpf_cnpj(token_sts, cpf_cnpj, tipo: str = 'PJ'):

    print('LOGX Get token tst função')
    print(token_sts)
    """
    Busca o id do EQ3 no endpoint atráves do cpf ou cnpj passado

    :param token_sts: objeto Token usado para consultar o endpoint do EQ3
    :param cpf_cnpj: informa somente número do cpf ou cnpj
    :param tipo: inica se o número informado em 'cpf_cnpj' é CPF ou CNPJ.
                 Aceita PJ (default) = para CNPJ e PF = para CPF

    :return dict com o dados do EQ3
    """

    try:

        numero = tamanho_numero_eq3(cpf_cnpj)

        tipo_pessoa = 'J' if tipo.upper() == 'PJ' else 'F'

        payload = {
            "cpf_cnpj": f"{numero}",
            "tipo_pessoa": f"{tipo_pessoa}"
        }

        # Necessário por conta do flake8
        token_access = token_sts["access_token"]
        token_type = token_sts["token_type"]

        headers = {
            'accept': '*/*',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': f'{token_type} {token_access}',
            'x-itau-apikey': f'{__ITAU_API_KEY__}',
            'x-itau-flowID': f'{__ITAU_FLOW_ID__}',
            'x-apigw-api-id': f'{__APIGW_API_ID__}',
            'Content-Type': 'application/json',
            'Connetion': 'keep-alive'
        }

        url = f'https://{__URL_BASE_EQ3__}{__URL_ENDPOINT_EQ3__}'

        response = post(
            url=url,
            data=dumps(payload),
            headers=headers,
            verify=__SSL_BUNDLE_CER__
        )

        print('LOGX Fez a requisição')

        if response.status_code == 200 or response.status_code == 201:

            json_eq3 = loads(response.content)
            json_eq3 = json_eq3['data']

            print(json_eq3)
            print('LOGX REQUISIÇÃO aprovada')

        else:
            print('Exception na requisição')
            erro = payload_erro(
                {
                    'Exception': [
                        {
                            "status_code": response.status_code,
                            "msg": json.loads(
                                response.content.decode("utf-8")
                            ),
                        }
                    ]
                },
                'get_dados_by_cpf_cnpj()'
            )
            return False, erro

    except exceptions.RequestException as e:

        erro = payload_erro(
            {'Exception': [e.args]},
            'get_dados_by_cpf_cnpj()RequestException'
        )
        return False, erro

    except Exception as e:

        erro = payload_erro(
            {'Exception': [e.args]},
            'get_dados_by_cpf_cnpj()Exception'
        )
        return False, erro

    else:

        return True, json_eq3


def tamanho_numero_eq3(valor):
    """
        função para colocar no tamanho exigido pela api da sigla EQ3
    """

    qtd_valor = len(valor)

    if qtd_valor >= 14:
        return valor
    else:
        return f'000000000000000{valor}'[-14:]
