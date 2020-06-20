# case_cats

## Projeto
Projeto criado e desenvolvido por Vinicius Kremer Santos, com a finalidade de atender os requisitos propostos pelo case Cats.
Foram utilizados as seguintes tecnologias no projeto:
    * Python (versão 3.9)
    * Tornado (Python Web Framework)
    * Docker

docker run -d -p 27017:27017 -e AUTH=no --name mongo mongo
docker run -d -p 8888:8888 --name case_cats_api viniciusks/case_cats:1.0.0