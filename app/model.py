import torch
import numpy as np
from torchvision import transforms
from PIL import Image


colors = {
    0: (36, 36, 36),    # Границы/Контур
    1: (200, 200, 200), # Дорога 
    2: (90, 77, 227),   # Здания
    3: (206, 214, 156), # Газон
    4: (133, 173, 130), # Деревья
    5: (207, 136, 37),  # Транспорт
    6: (122, 2, 16)     # Прочие объекты
}

def load_model(model_path: str):
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()  # Установка модели в режим оценки
    return model

def segment_image(model, image):
    # Преобразование изображения для модели
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)  # Добавляем размерность для батча

    with torch.no_grad():
        output = model(input_batch)  # Получаем выходные данные модели

    # Получаем предсказанную маску
    predicted_mask = torch.argmax(output, dim=1).cpu().numpy()[0]

    # Создание цветной маски на основе предсказанной маски
    colored_mask = np.zeros((*predicted_mask.shape, 3), dtype=np.uint8)
    
    for cls, color in colors.items():
        colored_mask[predicted_mask == cls] = color

    return Image.fromarray(colored_mask)  # Конвертация обратно в изображение PIL