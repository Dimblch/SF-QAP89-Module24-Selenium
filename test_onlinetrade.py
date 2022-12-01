import time
import pytest
from selenium import webdriver


def test_search_onlinetrade(selenium):
    # Открываем сайт магазина
    selenium.get('https://www.onlinetrade.ru/')

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим строку поиска
    search_input = selenium.find_element("name", "query")

    # Вводим поисковый запрос
    search_input.clear()
    search_input.send_keys('7600x')

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим кнопку с лупой и нажимаем на неё
    search_button = selenium.find_element("class name", "header__search__inputGogogo")
    search_button.submit()

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Делаем скриншот результатов
    selenium.save_screenshot('result.png')
