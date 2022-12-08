import time
from typing import Set, Dict, Any

import pytest
from selenium import webdriver
from datetime import datetime
from settings import valid_email, valid_password, valid_username


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./webdriver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

# Проверка страницы /all_pets
def test_cards_all_pets():
    # Вводим email
    pytest.driver.find_element('id', 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element('id', 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element('css selector', 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной (/all_pets) странице
    assert pytest.driver.find_element('tag name', 'h1').text == "PetFriends"
    # Собираем информацию о питомцах
    images = pytest.driver.find_elements('css selector', '.card-deck .card-img-top')
    names = pytest.driver.find_elements('css selector', '.card-deck .card-title')
    descriptions = pytest.driver.find_elements('css selector', '.card-deck .card-text')

    # Проверяем найденную информацию о питомцах на не пустоту
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# Проверка, страницы /my_pets
def test_list_my_pets():
    # Вводим email
    pytest.driver.find_element('id', 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element('id', 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element('css selector', 'button[type="submit"]').click()
    # Переходим на страницу пользователя (/my_pets)
    pytest.driver.find_element('link text', 'Мои питомцы').click()
    # Проверяем, что мы оказались на личной (/my_pets) странице
    assert pytest.driver.find_element('tag name', 'h2').text == valid_username

    time.sleep(1)

    # Вытаскиваем оглавление из верхнего левого угла (с ником)
    title = pytest.driver.find_element('xpath', '// *[ @ class = ".col-sm-4 left"]')
    # Делим оглавление на строки, и вытаскиваем общее число питомцев
    title_pets_number = int(title.text.split('\n')[1][10:])

    # Считаем количество строк в таблице питомцев
    pets_in_table_number = len(pytest.driver.find_elements('xpath', '// *[ @ id = "all_my_pets"] / table / tbody / tr'))

    # Составляем список питомцев и заодно считаем количество питомцев с фотографиями
    list_of_my_pets = []
    pets_with_photo_number = 0
    # Обращаться за каждым элементом на сайт - убогое решение, полюбому можно вытащить строку целиком и уже локально её парсить, но я пока так не умею :(
    for i in range(pets_in_table_number):
        photo = pytest.driver.find_element('xpath', f'// *[ @ id = "all_my_pets"] / table / tbody / tr[{i+1}] / th / img')
        name = pytest.driver.find_element('xpath', f'// *[ @ id = "all_my_pets"] / table / tbody / tr[{i+1}] / td[1]').text
        pet_type = pytest.driver.find_element('xpath', f'// *[ @ id = "all_my_pets"] / table / tbody / tr[{i+1}] / td[2]').text
        age = pytest.driver.find_element('xpath', f'// *[ @ id = "all_my_pets"] / table / tbody / tr[{i+1}] / td[3]').text
        list_of_my_pets.append([name, pet_type, age])
        if photo.get_attribute('src') != '':
            pets_with_photo_number += 1

    # Проверяем что у каждого питомца Имя, Порода и Возраст не пустые
    all_pets_valid = True
    for pet in list_of_my_pets:
        if not ( pet[0] and pet[1] and pet[2] ):
            all_pets_valid = False
            break

    # У всех питомцев разные имена.
    list_of_my_pets_names = []
    for pet in list_of_my_pets:
        list_of_my_pets_names.append(pet[0])
    all_pets_have_different_names = True
    if len(list_of_my_pets_names) != len(set(list_of_my_pets_names)):
        all_pets_have_different_names = False

    # В списке нет повторяющихся питомцев. (Сложное задание)
    all_pets_different = True
    for i in range(len(list_of_my_pets)):
        for j in range(i+1, len(list_of_my_pets)):
            if list_of_my_pets[i] == list_of_my_pets[j]:
                all_pets_different = False
                break
        if not all_pets_different:
            break

    # Присутствуют все питомцы
    assert pets_in_table_number == title_pets_number
    # Хотя бы у половины питомцев есть фото
    assert pets_with_photo_number * 2 >= title_pets_number
    # У всех питомцев есть имя, возраст и порода
    assert all_pets_valid
    # В списке нет повторяющихся питомцев. (Сложное задание)
    assert all_pets_different
    # У всех питомцев разные имена.
    assert all_pets_have_different_names
