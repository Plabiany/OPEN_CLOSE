Para executar o Docker da aplicação, basta fazer o clone do repositório em sua máquina local:

Dentro da pasta do projeto executar o seguinte comando:

docker run -p 5000:5000 -v ./:/app/MODEL flask-yolo-api

Caso, queria fazer inferência, use o arquivo client.py, dentro dele é possível passar o caminho de uma imagem e ao executar "python3 client.py" a aplicação retornará se a garrafa esta "OPEN" ou "CLOSED".


Antes de executar o doc, se necessário atribuir ao usuario local aspermissões para execução com os seguintes comandos:

sudo usermod -aG docker $USER

newgrp docker

Em seguida executar:
docker run -p 5000:5000 -v ./:/app/MODEL flask-yolo-api
