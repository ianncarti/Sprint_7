import time


#метод генерирует уникальные креды для регистрации на основе текущей даты и возвращает тело запроса для регистрации
def generate_uniq_creds(base_name="courier"):
    timestamp = int(time.time())  # Получаем текущее время в секундах
    payload = {'login': f"{base_name}_{timestamp}", 'password': f"{base_name}_{timestamp}",
               'firstname': f"{base_name}_{timestamp}"}
    return payload
