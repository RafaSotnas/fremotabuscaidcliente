import lambda_function
import pytest
import requests_mock

from tests.util.payload import payload_assinatura_entrada
from src import dados_pessoa, monta_erro
from guarda_segura import token_sts


def test_lambda_function(mocker):
    mocker.patch(
        "guarda_segura.token_sts.get_token_request",
        return_value=(
            True,
            {
                "token_type": "Bearer",
                "access_token": "asddadcx34ffr5asde54r1eddse",
            },
        ),
    )

    mocker.patch(
        "src.dados_pessoa.get_dados_by_cpf_cnpj",
        return_value=(
            True,
            {
                "id_cliente": "62e3676d-5f2f-4291-9f44-fb2436e8d3ac",
                "tipo_pessoa": "J",
            },
        ),
    )

    payload = payload_assinatura_entrada()
    retorno = lambda_function.lambda_handler(payload, [])

    # melhorar asserts
    assert retorno


def test_lambda_function_exception_token(mocker):
    mocker.patch(
        "guarda_segura.token_sts.get_token_request",
        return_value=(
            False,
            {
                "msg": "erro no token",
            },
        ),
    )
    payload = payload_assinatura_entrada()

    with pytest.raises(Exception):
        lambda_function.lambda_handler(payload, [])


def test_lambda_function_exception_dados(mocker):
    mocker.patch(
        "guarda_segura.token_sts.get_token_request",
        return_value=(
            True,
            {
                "token_type": "Bearer",
                "access_token": "asddadcx34ffr5asde54r1eddse",
            },
        ),
    )

    mocker.patch(
        "src.dados_pessoa.get_dados_by_cpf_cnpj",
        return_value=(
            False,
            {"msg": "teste"},
        ),
    )
    payload = payload_assinatura_entrada()

    with pytest.raises(Exception):
        lambda_function.lambda_handler(payload, [])


def test_get_dados_by_cpf(mocker):
    mocker.patch(
        "guarda_segura.token_sts.get_token_request",
        return_value=(
            True,
            {
                "token_type": "Bearer",
                "access_token": "asddadcx34ffr5asde54r1eddse",
            },
        ),
    )

    with requests_mock.Mocker() as rm:
        rm.post(
            requests_mock.ANY,
            json={
                "status_code": 200,
                "data": {
                    "id_cliente": "62e3676d-5f2f-4291-9f44-fb2436e8d3ac",
                    "tipo_pessoa": "J",
                },
            },
        )

        exec_ok, retorno = dados_pessoa.get_dados_by_cpf_cnpj(
            {
                "token_type": "Bearer",
                "access_token": "asddadcx34ffr5asde54r1eddse",
            },
            "00000",
            "PJ",
        )

        # melhorar asserts
        assert retorno
        assert exec_ok is True


def test_token_error():
    with pytest.raises(Exception):
        payload = payload_assinatura_entrada()
        lambda_function.lambda_handler(payload, [])


def test_monta_erro():
    msg = monta_erro.payload_erro(["Erro"], "lambda")

    assert len(msg["Erros"]) >= 1


# classe para utilizar no monkeypatch.
# Para mockar funcionalidade do secrets manager
# class MockClientBoto3SecretsManager:
# def __init__(self, *args, **kwargs):
#     return None

# def get_secret_value(self, SecretId):
#     return {"SecretString": "ClientOuSecret"}


def test_secrets_manager():
    # monkeypatch.setattr("boto3.client", MockClientBoto3SecretsManager)

    with requests_mock.Mocker() as rm:
        rm.post(
            requests_mock.ANY,
            json={
                "status_code": 200,
                "data": {"access_token": "aaaaa", "token_type": "Bearer"},
            },
        )

        exec_ok, token = token_sts.get_token_request()

    assert exec_ok is True
    assert token


def test_exception_token_sts():
    # monkeypatch.setattr("boto3.client", MockClientBoto3SecretsManager)

    exec_ok, token = token_sts.get_token_request()

    assert exec_ok is False
    assert token


def test_valor():
    retorno = dados_pessoa.tamanho_numero_eq3("12345678901234")
    assert len(retorno) >= 14
