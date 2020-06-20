# Case CATS

## Projeto
Projeto criado e desenvolvido por Vinicius Kremer Santos, com a finalidade de atender os requisitos propostos pelo case Cats.
Foram utilizados as seguintes tecnologias no projeto:
  * Python (versão 3.7)
  * Tornado (Python Web Framework)
  * MongoDB (Versão 4.0)
  * Docker

## API
A API foi desenvolvida em Python (versão 3.7) com o framework Tornado para levantar um server e receber as requisições.

Roda na porta **8888**.

Existe um padrão de retorno onde tem o "**status_code**" e o "**data**". 
O "**status_code**" pode retornar 2 valores *0* ou *1*, onde *0* serve para indicar que a API retornou com erro e *1* que serve para indicar o sucesso do retorno.
O campo "**data**" é um array dentro do JSON de retorno que, se tiver os dados no banco, a API irá retornar eles dentro deste campo. Caso ocorra de não haver dados, a API irá retornar uma mensagem dentro deste mesmo campo informando o motivo da falha.

Exemplo de retorno com sucesso:
```
{
    "status_code": 1,
    "data": [
        {
            
        }
    ]
}
```

Ela tem 4 endpoint que entre eles são: 
  * **/breeds/**
    > Retorna a lista completa de todas as raças de gatos do banco de dados
  * **/breeds/<id_nome_raça>**

docker run -d -p 27017:27017 -e AUTH=no --name mongo mongo
docker run -d -p 8888:8888 --name case_cats_api viniciusks/case_cats:1.0.0