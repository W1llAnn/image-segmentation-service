from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import torch
from app.model import load_model, segment_image

app = FastAPI()

# Загрузка модели
model = load_model("app/model_3_8.pt")

@app.post("/segment/")
async def segment(file: UploadFile = File(...)):
    # Чтение изображения из загруженного файла
    image = Image.open(file.file).convert("RGB")
    
    # Сегментация изображения
    segmented_image = segment_image(model, image)
    
    # Конвертация сегментированного изображения в байты для ответа
    img_byte_arr = io.BytesIO()
    segmented_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")
