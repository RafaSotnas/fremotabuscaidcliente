def payload_assinatura_entrada():
    return {
        "cnpj_requisitante": "00000000000000",
        "codigo_processo_consumidor": "0000000000",
        "garantidores": [{"cnpj": "00000000000000", "tipo_pessoa": "X"}],
        "participantes": [
            {"cpf": "00000000000000",
                "cnpj_pessoa_vinculada": "00000000000000"}
        ],
    }
