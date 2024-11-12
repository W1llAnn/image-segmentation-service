import os
import requests

# Укажите путь к папкам
input_folder = 'image_for_test'  # Папка с изображениями для тестирования
output_folder = 'output'          # Папка для сохранения результатов

# Создание папки output, если она не существует
os.makedirs(output_folder, exist_ok=True)

# URL вашего FastAPI приложения
url = "http://127.0.0.1:8000/segment/"

# Проход по всем файлам в папке input_folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Проверка на допустимые форматы изображений
        file_path = os.path.join(input_folder, filename)
        
        # Открытие файла для чтения в бинарном режиме
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}  # Форматирование данных для запроса
            
            # Отправка POST-запроса с изображением
            response = requests.post(url, files=files)
            
            # Проверка успешности запроса
            if response.status_code == 200:
                output_file_path = os.path.join(output_folder, f'segmented_{filename}')
                
                # Сохранение ответа (сегментированного изображения)
                with open(output_file_path, 'wb') as out_file:
                    out_file.write(response.content)
                print(f"Сегментированное изображение сохранено: {output_file_path}")
            else:
                print(f"Ошибка при обработке файла {filename}: {response.status_code} - {response.text}")