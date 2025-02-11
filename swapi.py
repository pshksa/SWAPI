# Импортируем необходимые библиотеки
import requests  # Для выполнения HTTP-запросов
import os       # Для работы с файловой системой (создание директорий и файлов)

# Базовый класс для работы с API
class APIRequester:
    def __init__(self, base_url):
       
        # Конструктор класса. Принимает базовый URL API и сохраняет его в атрибуте.
                
        self.base_url = base_url

    def get(self, endpoint=""):
        
        # Выполняет GET-запрос к указанному эндпоинту API.
                
        # Формируем полный URL, добавляя эндпоинт к базовому URL
        url = f"{self.base_url}/{endpoint}"
        # Выполняем GET-запрос
        response = requests.get(url)
        # Проверяем статус ответа. Если статус указывает на ошибку, выбрасываем исключение
        response.raise_for_status()
        # Возвращаем объект Response
        return response


# Класс для работы с API "Звёздных войн" (SWAPI)
class SWRequester(APIRequester):
    def __init__(self):
        
        # Конструктор класса. Инициализирует базовый URL для SWAPI.
        
        # Вызываем конструктор родительского класса с базовым URL SWAPI
        super().__init__("https://swapi.dev/api")

    def get_sw_categories(self):
        
        # Получает список доступных категорий из SWAPI.
                
        # Выполняем GET-запрос к базовому URL SWAPI
        response = self.get()
        # Преобразуем JSON-ответ в словарь Python
        data = response.json()
        # Возвращаем ключи словаря (это и есть категории)
        return list(data.keys())

    def get_sw_info(self, sw_type):
        
        # Получает данные по указанной категории из SWAPI.
                
        # Выполняем GET-запрос к указанной категории
        response = self.get(sw_type)
        # Возвращаем текстовое содержимое ответа
        return response.text


# Функция для сохранения данных из SWAPI в файлы
def save_sw_data():
    
    # Создаёт объект SWRequester, получает список категорий SWAPI,
    # запрашивает данные для каждой категории и сохраняет их в файлы.
    
    # Создаём объект SWRequester для работы с API
    sw_requester = SWRequester()
    # Получаем список доступных категорий
    categories = sw_requester.get_sw_categories()

    # Создаём директорию 'data', если она не существует
    if not os.path.exists('data'):
        os.makedirs('data')

    # Для каждой категории получаем данные и сохраняем их в файл
    for category in categories:
        # Получаем данные по категории
        data = sw_requester.get_sw_info(category)
        # Сохраняем данные в файл с именем <категория>.txt в директории 'data'
        with open(f'data/{category}.txt', 'w') as file:
            file.write(data)
        # Выводим сообщение об успешном сохранении
        print(f"Data for category '{category}' saved to data/{category}.txt")


# Вызов функции для сохранения данных
save_sw_data()