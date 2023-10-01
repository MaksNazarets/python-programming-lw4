from datetime import datetime
import random
import pandas as pd
from faker import Faker

fake = Faker('uk_UA')


male_patronymics = [
    "Іванович", "Петрович", "Сергійович", "Олександрович", "Михайлович", "Андрійович", "Вікторович", "Дмитрович", "Ярославович", "Антонович", "Валентинович", "Григорович", "Зіновійович", "Романович", "Васильович", "Максимович", "Олегович", "Володимирович", "Тимофійович", "Ігорович"
]

female_patronymics = [
    "Іванівна", "Петрівна", "Сергіївна", "Олександрівна", "Михайлівна", "Андріївна", "Вікторівна", "Дмитрівна", "Ярославівна", "Антонівна", "Валентинівна", "Григорівна", "Зіновіївна", "Романівна", "Василівна", "Максимівна", "Олегівна", "Володимирівна", "Тимофіївна", "Ігорівна"
]

data = []
for _ in range(2000):
    random_int = random.randint(1, 10)

    # 40% - female, 60% - male
    fname_patr_gender = {'fname': fake.first_name_female(), 'gender': "Жінка", 'patr': random.choice(female_patronymics)} if random_int < 5 else {
        'fname': fake.first_name_male(), 'gender': "Чоловік", 'patr': random.choice(male_patronymics)}

    c = fake.city()
    city = c if c[:5] != 'хутір' else random.choice(
        ['місто', 'селище', 'село']) + c[5:]

    first_name = fname_patr_gender['fname']
    last_name = fake.last_name()
    patronymic = fname_patr_gender['patr']
    gender = fname_patr_gender['gender']
    birthdate = fake.date_of_birth(tzinfo=None, minimum_age=datetime.now(
    ).year - 2008, maximum_age=datetime.now().year - 1938)
    position = fake.job()
    city = city
    address = fake.address()
    phone_number = fake.phone_number()
    email = fake.email()[:-11] + random.choice(['gmail.com', 'ukr.net'])

    data.append([last_name, first_name, patronymic, gender, birthdate,
                position, city, address, phone_number, email])

df = pd.DataFrame(data, columns=['Прізвище', 'Ім’я', 'По-батькові', 'Стать', 'Дата народження',
                  'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'])

df.to_csv('employees.csv', index=False, encoding='utf-8')
