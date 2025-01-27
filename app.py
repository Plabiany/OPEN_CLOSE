import torch
from ultralytics import YOLO
import flask
from flask import Flask, request, jsonify
from PIL import Image
import io

# Carregar o modelo YOLOv8 treinado
model = YOLO("best.pt")

app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    # Verificar se a extensão do arquivo é válida
    allowed_extensions = (".jpg", ".jpeg", ".png")
    if not file.filename.lower().endswith(allowed_extensions):
        return jsonify({"error": "Formato de arquivo inválido. Apenas JPEG e PNG são suportados."}), 400

    try:
        # Tentar abrir a imagem para garantir que é válida
        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        # Fazer predição com YOLO
        results = model(image)

        # Obter as detecções do primeiro resultado
        detections = results[0]  # Primeiro item da lista de resultados
        boxes = detections.boxes  # Bounding boxes detectadas
        confs = boxes.conf.tolist()  # Lista de scores de confiança
        labels = boxes.cls.tolist()  # Lista de classes detectadas
        xywh = boxes.xywh.tolist()  # Coordenadas do bounding box (x, y, largura, altura)

        # Se não houver detecções, retornar resposta padrão
        if len(confs) == 0:
            return jsonify({"Bottle_Status": "none", "Confidence": 0.0, "Bounding_Box": None})

        # Selecionar a predição com maior confiança
        max_index = confs.index(max(confs))
        best_label = int(labels[max_index])  # Classe como inteiro
        best_confidence = float(confs[max_index])  # Confiança como float
        best_bounding_box = xywh[max_index]  # Melhor bounding box

        # Log para depuração
        print(f"Detecção com maior confiança: Classe {best_label}, Confiança {best_confidence}, Bounding Box {best_bounding_box}")

        # Mapear os índices das classes para "open" e "closed"
        class_mapping = {0: "OPEN", 1: "CLOSED"}  # Ajuste conforme seu dataset
        bottle_status = class_mapping.get(best_label, "unknown")

        # Log para ver o status final da tampa
        print(f"Classificação final: {bottle_status} com confiança {best_confidence}")

        # Retornar a classificação, confiança e o bounding box
        return jsonify({
            "Bottle_Status": bottle_status,
            "Confidence": best_confidence
        })

    except Exception as e:
        return jsonify({"error": f"Falha ao processar a imagem: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
