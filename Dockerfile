# Usar imagem base oficial do Python com suporte ao PyTorch
FROM ultralytics/ultralytics:latest

# Definir diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar arquivos do projeto para o contêiner
COPY . /app

# Instalar dependências necessárias
RUN pip install --no-cache-dir flask pillow torch torchvision torchaudio ultralytics

# Expor a porta da API
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]