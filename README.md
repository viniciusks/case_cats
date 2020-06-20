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

Existe um padrão de retorno onde tem o "**return_code**" e o "**data**". 
O "**return_code**" pode retornar 2 valores *0* ou *1*, onde *0* serve para indicar que a API retornou com erro e *1* que serve para indicar o sucesso do retorno.
O campo "**data**" é um array dentro do JSON de retorno que, se tiver os dados no banco, a API irá retornar eles dentro deste campo. Caso ocorra de não haver dados, a API irá retornar uma mensagem dentro deste mesmo campo informando o motivo da falha.

Exemplo de retorno com sucesso:
```
{
    "return_code": 1,
    "data": [
        {
            "id_name": "abys",
            "name": "abyssinian",
            "origin": "egypt",
            "temperament": [
                "active",
                "energetic",
                "independent",
                "intelligent",
                "gentle"
            ],
            "description": "the abyssinian is easy to care for, and a joy to have in your home. they’re affectionate cats and love both people and other animals.",
            "images": [
                "https://cdn2.thecatapi.com/images/unPP08xOZ.jpg",
                "https://cdn2.thecatapi.com/images/KWdLHmOqc.jpg",
                "https://cdn2.thecatapi.com/images/xnzzM6MBI.jpg"
            ]
        }
    ]
}
```

Exemplo de retorno com falha:
```
{
    "return_code": 0,
    "data": [
        {
            "error_msg": "Não existe essa raça de gato."
        }
    ]
}
```

Ela tem 5 endpoint que entre eles são: 
  * **/breeds/** - GET
    > Retorna a lista completa de todas as raças de gatos.
  * **/breeds/<-id_name_breed->** - GET
    > Retorna informações de apenas uma raça conforme o id_name_breed passado. Exemplo de id_name_breed: *"abys, sib"*.
  * **/breeds-origin/<-origin->** - GET
    > Retorna raças que sejam da origem passada. Exemplo de origem: *"Russia", "Egypt", "Greece", "United State"*.
  * **/breeds-temperament/<-temperament->** - GET
    > Retorna raças que tenham o temperamento informado. Exemplos de temperamento: *"active", "energetic", "sweet", "independent", "intelligent", "gentle"*.
  * **/cats-category-images/<-category_id->** - POST
    > Conforme o category_id passado, pesquisa a imagem e insere no banco o endereço da mesma.
    > * category_id = 1 -> Hats cats
    > * category_id = 4 -> Sunglasses cats

O log da api é salva em um arquivo de log **api_cats.log**.
  
## Arquitetura
Foi utilizado Docker para montar a Infraestrutura de toda aplicação. Tudo está rodando em container Docker.

O Banco de dados utilizado foi o **MongoDB**, a imagem do container foi usada a oficial no repositóio Dockerhub.
Para iniciar o container dele basta rodar o comando abaixo:

  > docker run -d -p 27017:27017 --name mongo mongo

Ou rodar o **_docker-compose.yml_**.
O **MongoDB** está rodando na porta *27017*.

A aplicação *case_cats* está rodando em container Docker também. A imagem da aplicação já está no DockerHub, com o nome de **_viniciusks13/case_cats_**, tem tags e a utilizada foi a **_1.0.1_**.
O Dockerfile está junto no repositório Git no GitHub para análise da construção, mas ela também se encontra no DockerHub para a execução de um container.
Para iniciar o container dele basta rodar o comando abaixo:

  > docker run -d -p 8888:8888 --link=mongo --name case_cats_api viniciusks13/case_cats:1.0.1

Ou rodar o **_docker-compose.yml_**.
A aplicação **case_cats** está rodando na porta *8888*.

É recomendado levantar os containers através do **_docker-compose.yml_**.

## Como rodar localmente
Para rodar localmente basta ou rodar os comandos *docker run* ou rodar o *docker-compose.yml*

 * Rodando com *docker run*:
   1. Rodar o comando para subir o MongoDB
     ```
     docker run -d -p 27017:27017 --name mongo mongo
     ```

   2. Rodar o comando para subir a API Rest case_cats
     ```
     docker run -d -p 8888:8888 --link=mongo --name case_cats_api viniciusks13/case_cats:1.0.1
     ```

    Após a execução dessas desses comandos o ambiente estará de pé, a primeira execução pode levar em torno de 2-3 minutos para ficar tudo no ar, isso por conta da carga inicial de dados no MongoDB.

  * Rodando com *docker-compose.yml*:
    1. Rodar o comando do *docker-compose.yml* para subir os conteineres de MongoDB e a API Rest case_cats
      ```
       docker-compose -f docker-compose.yml -d up
      ```

      * OSB: A flag "-d" é o detached mode, quando o container inicia neste modo ele libera o terminal enquanto o processo fica rodando em background.
     
    O docker-compose.yml contém os dois conteiners configurados dentro dele.
    Após a execução dessas desses comandos o ambiente estará de pé, a primeira execução pode levar em torno de 2-3 minutos para ficar tudo no ar, isso por conta da carga inicial de dados no MongoDB.