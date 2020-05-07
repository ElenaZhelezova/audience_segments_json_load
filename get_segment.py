from configparser import ConfigParser
from pathlib import Path
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import requests
import json

logging.basicConfig(filename='get_segment.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
ERROR_404 = {"error": "Bad request"}


def get_params(config_path, config_name):
    """
    looking for passed config file in own folder
    :param config_path: path to configuration file
    :param config_name: config part name, where parameters could be found
    :return: url and authorization parameters
    """

    config_parser = ConfigParser()
    config_path = Path(config_path)
    with config_path.open() as f:
        config_parser.read_file(f)
    params = config_parser[config_name]

    return params


def get_driver(config_params):
    """
    create a new hidden FireFox driver with proxy
    :return: driver
    """

    options = webdriver.FirefoxOptions()

    options.headless = True                # make it hidden
    profile = webdriver.FirefoxProfile()
    proxy_host = config_params['proxy_host']
    proxy_port = config_params['proxy_port']
    profile.set_preference('network.proxy.https', proxy_host)
    profile.set_preference('network.proxy.https_port', proxy_port)

    created_driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)
    created_driver.implicitly_wait(7)

    return created_driver


def authorize_driver(config_params):
    """
    authorization with ya passport
    :param config_params: authorization parameters
    :return: driver
    """
    driver_instance = get_driver(config_params)
    driver_instance.get(config_params['url'])
    try:
        driver_instance.find_element_by_class_name('button2').click()
        assert 'Авторизация' in driver_instance.title

        login = driver_instance.find_element_by_xpath('//input[@name="login"]')
        login.send_keys(config_params['log_name'])
        driver_instance.find_element_by_xpath('//button[@type="submit"]').click()

        passwd = driver_instance.find_element_by_xpath('//input[@name="passwd"]')
        passwd.send_keys(config_params['passwd'])
        passwd.submit()
        logging.info('driver has been authorized')
    except:
        logging.exception('driver has not been authorized, something went wrong')
        return

    return driver_instance


def get_data(driver):
    """
    get json data of list id
    :param driver:
    :return: json
    """
    url = driver.last_request.path
    headers = driver.last_request.headers
    cookies = driver.get_cookies()
    args = driver.last_request.body
    session = requests.Session()
    session.headers = headers
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    try:
        response = session.post(url, data=args)
        logging.info("segment's json data has been obtained")
    except:
        logging.exception("segment's json data has not been obtained")
        return

    return response.content.decode()


def get_segments_data(list_ids, conf_path='seg_config.ini', conf_name='scrap config'):
    """
    gets json data from segment found by id
    :param list_ids:
    :param conf_path:
    :param conf_name:
    :return:
    """
    return_data = {}
    config = get_params(conf_path, conf_name)
    auth_driver = authorize_driver(config)
    if not auth_driver:
        return ERROR_404

    id_elements = auth_driver.find_elements_by_class_name('audience-segment-row__label')
    status_elements = \
        auth_driver.find_elements_by_class_name('audience-segment-row__state')

    if not id_elements:
        logging.info("list ids has not been found")
        return ERROR_404

    if auth_driver.find_elements_by_class_name('crm-data-announcement__close'):
        button = WebDriverWait(auth_driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "crm-data-announcement__close")))
        button.click()

    for num, item in enumerate(id_elements):
        if not list_ids:
            break

        if item.text.split(' ')[0] != 'List_id':
            continue

        item_id = int(item.text.split(' ')[1])
        status_id = status_elements[num].text
        if (item_id in list_ids) and (status_id == 'Готов'):
            list_ids.remove(item_id)

            buttons = auth_driver.find_elements_by_class_name(
                'audience-segment-row__stats-button')
            buttons[num].click()
            logging.info(f"list id {item_id} processed")
            data = json.loads(get_data(auth_driver))
            auth_driver.find_element_by_class_name(
                'audience-segment-statistics__close').click()

            return_data[item_id] = data
            logging.info(f"List id {item} has been processed")

        elif (item_id in list_ids) and (status_id != 'Готов'):
            logging.info(f"List id {item_id} was not ready")

    auth_driver.quit()

    if list_ids:
        for item in list_ids:
            logging.info(f"List id {item} was not found")

    if not return_data:
        return ERROR_404
    print(return_data)
    return return_data


if __name__ == '__main__':
    get_segments_data(list_ids=[44688, 44889], conf_path='seg_config.ini',
                      conf_name='scrap config')
