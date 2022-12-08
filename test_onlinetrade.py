import time
import pytest
from selenium import webdriver
from datetime import datetime

string_to_search = 'intel'

# Подготавливаем строку с датой и временем для имени файла скриншота
dt = str(datetime.now())
dtf = dt[0:4]+dt[5:7]+dt[8:10]+'_'+dt[11:13]+dt[14:16]+dt[17:19]

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
    pytest.driver.find_element("name", "query").send_keys(string_to_search)

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим кнопку с лупой и нажимаем на неё
    pytest.driver.find_element("class name", "header__search__inputGogogo").click()

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Делаем контрольный скриншот
    pytest.driver.save_screenshot(f'test_search_{dtf}.png')

    # Проверяем заголовок окна
    assert string_to_search + " — купить в ОНЛАЙН ТРЕЙД.РУ" == pytest.driver.title


# Проверяем что каждый найденный товар содержит фотографию, описание и цену
def test_search_results():
    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим строку поиска и вводим запрос
    pytest.driver.find_element("name", "query").send_keys(string_to_search)

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Находим кнопку с лупой и нажимаем на неё
    pytest.driver.find_element("class name", "header__search__inputGogogo").click()

    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Просматриваем и считаем результаты поиска
    goods = pytest.driver.find_elements("class name", "indexGoods__item")
    images = pytest.driver.find_elements('xpath', '// *[ @ class = "indexGoods__item__flexCover"] / a / img')
    titles = pytest.driver.find_elements('xpath', '// *[ @ class = "indexGoods__item__descriptionCover"] / a')
    prices = pytest.driver.find_elements('xpath', '// *[ @ class = "indexGoods__item__price"] / span')

    # Проверяем что во всех найденных карточках товаров нашлись изображение, описание и цена
    assert len(goods) == len(images) == len(titles) == len(prices)

    print(f' Total found {len(images)} or more goods')
    pytest.driver.save_screenshot(f'test_search_results_{dtf}.png')

    # Проверяем что найденные изображения, описания и цены не пустые
    for i in range(len(images)):
        assert images[i].get_attribute('src') != ''
        assert titles[i].text != ''
        assert prices[i].text != ''
