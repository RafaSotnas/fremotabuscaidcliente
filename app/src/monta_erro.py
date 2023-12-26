'''
    Função para ser usada na montagem do dict de erro

    Projeto: Assinatura Digital | Plataforma Agnostica
    Squad2020: Inovativos - Moeda Nacional
    Criado por: Rafael Oliveira
    Data : jul/2022

'''


def payload_erro(erros: list, resource_name: str) -> dict:

    msg = {
        'controle': 'erro',
        'Resource': 'lambda',
        'ResourceName': f'{resource_name}',
        'Erros': []
    }

    msg['Erros'].append(erros)

    return msg
