# Hello World Python 3

Aplicação exemplo Python 3

## Hierarquia de Pastas

| **Diretório**                                 | **Descrição**                        | **O que o diretório pode conter**                                                                                                               |
| -------------------------------------------   |--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **/app**                                      | Source da aplicação e Teste Unitário | Código Fonte da aplicação `(Source) juntamente com o Teste Unitário`                                                                              |
| **/tests**            | Test as a Code                 | Arquivo `testspec.yml` para TaaC |
| **/infra**                                    | Criação de Infraestrutura            | Arquivo YAML em formato CLOUDFORMATION CUSTOMIZADO, para criação de infraestrutura. <br>EX: Recurso lambda utilizado pela pipeline para provisionar a infraestrutura (`lambda.yaml`).   |
| **/pipeline**                                 | Pipeline Customizado                 | Arquivo `buildspec.yaml` para execução de BUILD CUSTOMIZADO.  <br>Arquivo `buildspec_test.yaml` para execução de TESTE UNITARIO CUSTOMIZADO.        | 

## Configuração TaaC

Para configurar o test as code, recomendamos seguir a seguinte [documentação](https://confluencecorp.ctsp.prod.cloud.ihf/display/CONTTEST/TAAC)

## Dúvidas??

### :pushpin: **Para maior informação sobre pipelines pode verificar nossa documentação nesse [link](https://pi5.pages-gitlab.prod.cloud.ihf/docs/)**