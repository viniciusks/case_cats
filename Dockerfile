# Imagem que a minha será baseada
FROM python:3.7

# Exposição da porta do serviço
EXPOSE 8888

# Adiciona tudo que está no diretório para o diretório padrão dentro do container
ADD . /

# Instala todas as dependências da api
RUN pip3 install -r requirements.txt

# Executa a api
CMD [ "python" , "main.py" ]