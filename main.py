import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройки для Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '15pUf3AHAu4jEiJYySoflSK-PyDUbpblxKOWqVv747Ew'
SHEET_NAME = 'KommoCRM'

# Настройки для KommoCRM
KOMMO_API_KEY = 'YOUR_KOMMO_API_KEY'
KOMMO_API_ENDPOINT = 'https://api.kommocrm.com/v1/leads'  # Пример адреса API

def fetch_leads_from_kommo():
    headers = {'Authorization': f'Bearer {KOMMO_API_KEY}'}
    response = requests.get(KOMMO_API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Ошибка при получении данных из KommoCRM: {response.text}")
        return []

def update_google_sheets(leads):
    # Авторизация в Google Sheets
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', SCOPES)
    client = gspread.authorize(credentials)

    # Открытие таблицы
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    # Запись данных в таблицу
    for index, lead in enumerate(leads, start=2):  # Начинаем с второй строки, первая строка - заголовки
        sheet.update(f'A{index}', lead['name'])
        sheet.update(f'B{index}', lead['email'])
        sheet.update(f'C{index}', lead['phone'])
        # Другие поля из lead могут быть добавлены по аналогии

def main():
    leads = fetch_leads_from_kommo()
    if leads:
        update_google_sheets(leads)
        print("Данные успешно переданы в Google Sheets.")
    else:
        print("Нет данных для передачи.")

if __name__ == "__main__":
    main()