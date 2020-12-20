import os
import re
from requests import get
from time import sleep
from selenium import webdriver


def open_file(file_name):
    with open(file_name, "r", encoding="UTF-8") as file:
        file_list = file.read().splitlines()
        file_list = list(filter(None, file_list))    # 去掉空行
        # print(file_list)
        new_file_list = []
        for i in file_list:
            if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i):
                # print(i)
                new_file_list.append(i)
            else:
                i = "http://{}".format(i)
                # print(i)
                new_file_list.append(i)
    return new_file_list


def url_check(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"}
    try:
        response = get(url=url, headers=headers, timeout=3)
        status_code = response.status_code
        if int(status_code) == 200:
            return True
    except Exception as e:
        print(e)
        return False


def screenshots():
    image_name = 1
    working_path = os.getcwd()
    url_images_path = "{}\\url_images\\".format(working_path)
    url_list_path = "{}\\url_list.txt".format(working_path)
    url_list = open_file(url_list_path)
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("about:blank")
    sleep(1)

    for url in url_list:
        if url_check(url=url):
            driver.get(url)
            sleep(3)
            try:
                driver.get_screenshot_as_file(
                    "{}{}.png".format(url_images_path, image_name))
                print("网站{}截图成功：{}".format(image_name, url))
                image_name = image_name + 1
            except BaseException as error_message:
                print("网站{}截图失败：{}".format(image_name, error_message))
        else:
            print("网站截图失败！")
    driver.quit()


if __name__ == "__main__":
    # print(open_file("C:\\Users\\Administrator\\Desktop\\demo\\url_list.txt"))
    # print(url_check("https://wx.zsxq.com/"))
    screenshots()
