import time
import pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./webdriver/chromedriver.exe')

    # Открываем сайт магазина
    pytest.driver.get('https://www.onlinetrade.ru/')

    yield

    pytest.driver.quit()


# Проверяем работу поиска товара в магазине
def test_search():
    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим строку поиска и вводим запрос
    pytest.driver.find_element("name", "query").send_keys('7600x')

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим кнопку с лупой и нажимаем на неё
    pytest.driver.find_element("class name", "header__search__inputGogogo").click()
#    search_button.submit()

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Делаем контрольный скриншот
    pytest.driver.save_screenshot('test_search_result.png')

    # Проверяем заголовок окна
    assert "7600x — купить в ОНЛАЙН ТРЕЙД.РУ" == pytest.driver.title

# Проверяем что каждый найденный товар содержит фотографию, описание (с подсвеченным поисковым запросом) и цену
def test_search_results():
    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим строку поиска и вводим запрос
    pytest.driver.find_element("name", "query").send_keys('7600x')

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим кнопку с лупой и нажимаем на неё
    pytest.driver.find_element("class name", "header__search__inputGogogo").click()
    #    search_button.submit()

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

