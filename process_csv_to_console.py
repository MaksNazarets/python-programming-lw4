from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

current_date = datetime.now()


def calculate_age(birthdate):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = current_date.year - birthdate.year - \
        ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age


try:
    df = pd.read_csv('employees.csv', encoding='utf-8')
except FileNotFoundError:
    print("Помилка: Файл CSV не знайдено.")
    exit(1)
except Exception as e:
    print(f"Помилка при зчитуванні CSV: {str(e)}")
    exit(1)


df['Вік'] = df['Дата народження'].apply(calculate_age)

# Кількість співробітників чоловічої та жіночої статі
gender_counts = df['Стать'].value_counts()
print(
    f"Кількість співробітників чоловічої та жіночої статі: \n{gender_counts}\n")

gender_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Розподіл співробітників за статтю')
plt.show()

# Кількість співробітників в кожній віковій категорії
bins = [0, 18, 45, 70, float('inf')]
age_categories = ['<18', '18-45', '45-70', '>70']
df['Вікова категорія'] = pd.cut(
    df['Вік'], bins=bins, labels=age_categories, right=False)
age_category_counts = df['Вікова категорія'].value_counts().reindex(
    age_categories, fill_value=0)
print("Кількість співробітників в кожній віковій категорії:")
print(age_category_counts)
print()

# Діаграма вікових категорій
age_category_counts.plot(kind='bar')
plt.xlabel('Вікова категорія')
plt.ylabel('Кількість співробітників')
plt.title('Розподіл співробітників за віком')
plt.show()

# Кількість співробітників чоловічої та жіночої статі в кожній віковій категорії
gender_age_counts = df.groupby(
    ['Стать', 'Вікова категорія'], observed=False).size().unstack(fill_value=0)
print("Кількість співробітників чоловічої та жіночої статі в кожній віковій категорії:")
print(gender_age_counts)
print()

# Діаграми для розподілу співробітників чоловічої та жіночої статі в кожній віковій категорії
gender_age_counts.plot(kind='bar', stacked=True)
plt.xlabel('Вікова категорія')
plt.ylabel('Кількість співробітників')
plt.title('Розподіл співробітників за статтю та віком')
plt.legend(title='Стать')
plt.show()
