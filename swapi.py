import os

import requests

class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, endpoint=""):
        try:
            response = requests.get(self.base_url + endpoint)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print("Ошибка при запросе:", e)
            return None

class SWRequester(APIRequester):
    def __init__(self, base_url="https://swapi.dev/api/"):
        super().__init__(base_url)
    
    def get_sw_categories(self):
        response = self.get()
        if response:
            return list(response.json().keys())
        return []
    
    def get_sw_info(self, sw_type):
        response = self.get(sw_type + "/")
        if response:
            return response.text
        return ""

def save_sw_data():
    sw = SWRequester()
    categories = sw.get_sw_categories()
    
    if not os.path.exists("data"):
        os.mkdir("data")
    
    for category in categories:
        data = sw.get_sw_info(category)
        with open(f"data/{category}.txt", "w", encoding="utf-8") as f:
            f.write(data)
    
    print("Файлы сохранены в папке data")

if __name__ == "__main__":
    save_sw_data()