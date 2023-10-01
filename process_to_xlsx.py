import pandas as pd
from datetime import datetime

try:
    df = pd.read_csv('employees.csv', encoding='utf-8')
except FileNotFoundError:
    print("Помилка: Файл CSV не знайдено.")
    exit(1)
except Exception as e:
    print(f"Помилка при зчитуванні CSV: {str(e)}")
    exit(1)

current_date = datetime.now()


def calculate_age(birthdate):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = current_date.year - birthdate.year - \
        ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age


df['Вік'] = df['Дата народження'].apply(calculate_age)

df['Вікова категорія'] = pd.cut(df['Вік'], bins=[0, 18, 45, 70, float('inf')],
                                labels=['молодший 18', '18-45', '45-70', 'старший 70'], right=False)

all_sheet = df.copy()
sheets = {
    'молодший 18': df[df['Вікова категорія'] == 'молодший 18'][['Прізвище', 'Ім’я', 'По-батькові', 'Дата народження', 'Вік']],
    '18-45': df[df['Вікова категорія'] == '18-45'][['Прізвище', 'Ім’я', 'По-батькові', 'Дата народження', 'Вік']],
    '45-70': df[df['Вікова категорія'] == '45-70'][['Прізвище', 'Ім’я', 'По-батькові', 'Дата народження', 'Вік']],
    'старший 70': df[df['Вікова категорія'] == 'старший 70'][['Прізвище', 'Ім’я', 'По-батькові', 'Дата народження', 'Вік']]
}

try:
    with pd.ExcelWriter('employees.xlsx', engine='xlsxwriter') as writer:
        all_sheet.to_excel(writer, sheet_name='all', index=False)
        for sheet_name, data in sheets.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for i, col in enumerate(all_sheet.columns):
                max_len = max((all_sheet[col].astype(
                    str).map(len).max(), len(col))) + 1
                worksheet.set_column(i, i, max_len)

except Exception as e:
    print(f"Помилка при створенні XLSX-файлу: {str(e)}")
    exit(1)

print("Ok, програма завершила свою роботу успішно.")
