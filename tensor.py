import os
import logging
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    filemode='w',
    format='[%(asctime)s] %(filename)s Line:%(lineno)d #%(levelname)s | %(name)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

task1_expected = {'search_field_found': True,
                  'suggest_is_visible': True,
                  'links>=5': True}

task2_expected = {'pictures_link_found': True,
                'pic1_exists': True,
                'next_is_not_the_same_pic': True,
                'pic1_matches': True}


class TensorTask:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.driver = webdriver.Chrome(os.path.join('static', 'chromedriver.exe'), options=self.options)

    def get_links(self):
        """ Задание № 1 """
        results = {key: False for key in task1_expected}
        # 1) Зайти на yandex.ru
        self.driver.get('https://yandex.ru')

        # 2) Проверить наличие поля поиска
        try:
            search_field = self.driver.find_element_by_id('text')
            results['search_field_found'] = bool(search_field)
            logging.info('Search field found')
        except NoSuchElementException as ex:
            logging.exception(ex)
            return results

        # 3) Ввести в поиск Тензор
        search_field.send_keys('Тензор')
        logging.info('"Тензор" input')
        sleep(5)

        # 4) Проверить, что появилась таблица с подсказками (suggest)
        try:
            suggest = self.driver.find_element_by_css_selector('div.suggest2__content.suggest2__content_theme_normal')
            results['suggest_is_visible'] = suggest.is_displayed()
            logging.info('Suggest is visible')
        except NoSuchElementException:
            results['suggest_is_visible'] = False
            logging.error('Suggest did not appear')

        # 5) При нажатии Enter появляется таблица результатов поиска
        search_field.send_keys(Keys.RETURN)
        try:
            tensor_urls = self.driver.find_elements_by_css_selector('h2 a')
            logging.info('Search results found')
        except NoSuchElementException:
            logging.error('No links found')
            return results

        # 6) В первых 5 результатах есть ссылка на tensor.ru
        urls_count = len([link for link in tensor_urls if 'tensor.ru' in link.get_property('href')])
        results['links>=5'] = (urls_count >= 5)
        logging.info(f"There is/are {urls_count} link(s) to tensor.ru")
        return results

    def get_pictures(self):
        """ Задание № 2 """
        results = {key: False for key in task2_expected}
        # 1) Зайти на yandex.ru
        self.driver.get('https://yandex.ru')

        # 2) Ссылка «Картинки» присутствует на странице
        try:
            pictures_link = self.driver.find_element_by_link_text('Картинки')
            results['pictures_link_found'] = bool(pictures_link)
            logging.info('Pictures link found')
        except NoSuchElementException as ex:
            logging.exception(ex)
            return results

        # 3) Кликаем на ссылку
        pictures_link.click()

        # 4) Проверить, что перешли на url https://yandex.ru/images/
        if 'https://yandex.ru/images/' in self.driver.current_url:
            logging.info('URL "https://yandex.ru/images/" is correct')
            # 5) Открыть 1 картинку, проверить что открылась
            # 5.1 Находим первое изображение и открываем
            try:
                first_picture = self.driver.find_elements_by_class_name('cl-teaser__wrap.cl-teaser-video-play')[0]
                logging.info('The first picture div found')
                first_picture.click()
            except NoSuchElementException or ElementClickInterceptedException as ex:
                logging.exception(ex, 'The first picture div not found')
                return results

            # 5.2 Убеждаемся, что изображение существует
            try:
                first_picture_source = self.driver.find_element_by_css_selector('div.image__wrap__i img.image__image'
                                                                                '').get_attribute('src')
                results['pic1_exists'] = bool(first_picture_source)
                logging.info('The first picture has a source')
            except NoSuchElementException as ex:
                first_picture_source = None
                logging.exception(ex, 'The first picture source path not found')

            # 6) При нажатии кнопки "вперед" картинка изменяется
            try:
                right_arrow = self.driver.find_element_by_css_selector('div.cl-layout__nav__right'
                                                                       ' a.cl-layout__nav__arrow ')
                logging.info('Right arrow found')
                right_arrow.click()
            except NoSuchElementException or ElementClickInterceptedException as ex:
                logging.exception(ex, 'Right arrow not found')
                return results

            try:
                second_picture_source = self.driver.find_element_by_css_selector('div.image__wrap__i img.image__image'
                                                                                 '').get_attribute('src')
                results['next_is_not_the_same_pic'] = (first_picture_source != second_picture_source)
                logging.info('The second picture is not the same as the first one')
            except NoSuchElementException as ex:
                logging.exception(ex, 'Second picture source not found')

            # 7) При нажатии кнопки назад картинка изменяется на изображение из шага 5.
            try:
                left_arrow = self.driver.find_element_by_css_selector('div.cl-layout__nav__left '
                                                                      'a.cl-layout__nav__arrow ')
                logging.info('Left arrow found')

                # перехватываем сообщение Яндекса о регистрации
                sleep(3)
                try:
                    msg_box = self.driver.find_element_by_css_selector('div.message-box__close svg')
                    if msg_box.is_displayed():
                        msg_box.click()
                except NoSuchElementException:
                    pass

                left_arrow.click()
            except NoSuchElementException as ex:
                logging.exception(ex, 'Left arrow not found')
                return results

            # Необходимо проверить, что это тоже изображение.
            try:
                new_picture_source = self.driver.find_element_by_css_selector('div.image__wrap__i'
                                                                              ' img.image__image').get_attribute('src')
                results['pic1_matches'] = (new_picture_source == first_picture_source)
                logging.info('Got the same picture after coming back')
            except NoSuchElementException as ex:
                logging.exception(ex, 'The source of picture not found after coming back')

            return results
        else:
            return results


if __name__ == '__main__':
    tensor = TensorTask()

    logging.info(' =========== Task № 1 started ===========')
    try:
        result = tensor.get_links()
        logging.info(result)
        assert task1_expected == result
        logging.info('First task passed successfully')
    except AssertionError as a:
        logging.exception(a)
        logging.info('First task failed')
    logging.info(' =========== Task № 1 finished ===========')

    logging.info(' =========== Task № 2 started ===========')
    try:
        result = tensor.get_pictures()
        logging.info(result)
        assert task2_expected == result
        logging.info('Second task passed successfully')
    except AssertionError as a:
        logging.exception(a)
        logging.info('Second task failed')
    logging.info(' =========== Task № 2 finished ===========')

    tensor.driver.quit()
