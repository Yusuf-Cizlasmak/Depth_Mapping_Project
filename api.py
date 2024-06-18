import os
import uuid

from fastapi import FastAPI, File, UploadFile

from predictor import DepthEstimationModel
from upload import upload_image

ALLOW_EXTENSIONS = {".jpg", ".png", ".jpeg"}
TEMP_FOLDER = "api_images"
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = FastAPI()
model = DepthEstimationModel()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    try:
        file_ext = os.path.splitext(file.filename)[1]  # .txt , .png ,.jpeg mi ?

        if file_ext not in ALLOW_EXTENSIONS:
            return {"error": "Yüklediğiniz resim JPG,JPEG veya PNG formatında olmalı"}

        filename_base = str(uuid.uuid4())
        filename = filename_base + file_ext

        destination_path = os.path.join(TEMP_FOLDER, filename)

        output_path = os.path.join(TEMP_FOLDER, "output" + filename_base + ".png")

        with open(destination_path, "wb") as image_data:
            image_data.write(file.file.read())

        # Modeli çalıştırmak
        model.calculate_depthmap(destination_path, output_path)

### EKLENİLEN KISIM ## 

        #Kaydettiğim dosyayı imgbb'ye yükleme (İŞLEM YAPILAN KISIM)
        response = upload_image(output_path)

        return response

    except Exception as e:
        return {"error": str(e)}
