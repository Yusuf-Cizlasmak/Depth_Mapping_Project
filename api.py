import os
import uuid

from fastapi import FastAPI, File, UploadFile

from predictor import DepthEstimationModel

ALLOW_EXTENSIONS = {".jpg", ".png", ".jpeg"}
TEMP_FOLDER = "api_images"
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = FastAPI()
model = DepthEstimationModel()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # hataları daha kolay görebilmek adında try ve except şeklinde yazacağız.

    try:
        file_ext = os.path.splitext(file.filename)[1]  # .txt , .png ,.jpeg mi ?

        if file_ext not in ALLOW_EXTENSIONS:
            return {"error": "Yüklediğiniz resim JPG,JPEG veya PNG formatında olmalı"}

        # fotoğraflara random isimlendirme

        # You can use the filename_base to create a unique filename for the uploaded file
        # For example:
        # unique_filename = f"{filename_base}{file_ext}"
        # This will create a filename like "c4a3f6d8-9b2e-4c1d-a7e9-3e2b1f0a5d6f.jpg"
        filename_base = str(uuid.uuid4())
        filename = filename_base + file_ext

        # şimdi hedef dosya ile kaydedilecek yer ayarlayalım

        destination_path = os.path.join(TEMP_FOLDER, filename)

        output_path = os.path.join(TEMP_FOLDER, "output" + filename_base + ".png")

        # api'den gelen görüntüyü kaydetme

        with open(destination_path, "wb") as image_data:
            image_data.write(file.file.read())

        # Modeli çalıştırmak
        model.calculate_depthmap(destination_path, output_path)


        return {"OK": "Yapmak istediğiniz işlem tamamlandı."}

    except Exception as e:
        return {"error": str(e)}
