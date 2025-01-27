import requests

url = "http://127.0.0.1:5000/classify"
files = {"image": open("/home/plabiany/Imagens/Capturas de tela/coronaa.png", "rb")}
response = requests.post(url, files=files)
print(response.json())
