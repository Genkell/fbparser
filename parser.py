from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def log_in(_driver):
    url = "https://www.facebook.com"
    _driver.get(url)
    _driver.maximize_window()
    username = _driver.find_element("id", "email")
    password = _driver.find_element("id", "pass")
    submit = _driver.find_element("name", "login")
    username.send_keys("pechkaar@gmail.com")
    password.send_keys("aezakmi01")
    submit.click()
    time.sleep(5)


def find_all_groups(_driver):
    for i in _driver.find_elements(By.TAG_NAME, "div"):
        try:
            if "article" in i.get_attribute("role") and "Группы" in i.text:
                for j in i.find_elements(By.TAG_NAME, "a"):
                    if j.text == "Все":
                        return j.get_attribute("href")
        except (Exception,):
            pass


def get_all_groups_links(_driver: webdriver.Chrome, amount: int):
    groups = []
    prev_list = []
    texts = []
    while len(groups) < amount:
        _driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        _driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        for i in _driver.find_elements(By.TAG_NAME, "div"):
            try:
                if "Участники" in i.text and i.text.count("Участники") == 1 and i.text not in texts:
                    texts.append(i.text)
                    _link = ""
                    for j in i.find_elements(By.TAG_NAME, "a"):
                        link = j.get_attribute("href")
                        fb_groups_pattern = "https://www.facebook.com/groups/"
                        if fb_groups_pattern in link \
                                and not link.endswith("?__tn__=%3C"):
                            _link = link
                            break
                    info = i.text.split("\n")[1].split(" · ")
                    _name = i.text.split("\n")[0]
                    _type = info[0]
                    _members = info[1]
                    _frequency = info[2]
                    _d = {
                        "name": _name,
                        "link": _link,
                        "type": _type,
                        "members": _members,
                        "frequency": _frequency
                    }
                    if _d not in groups:
                        groups.append(_d)
            except (Exception,):
                pass
        if groups == prev_list:
            break
        else:
            prev_list = groups.copy()
    return groups


def get_groups_info(q: str):
    q = q.replace(" ", "%20")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    log_in(driver)
    time.sleep(5)
    driver.get(f"https://www.facebook.com/search/top?q={q}")
    time.sleep(3)
    all_group_link = find_all_groups(driver)
    print(all_group_link)
    driver.get(all_group_link)
    return get_all_groups_links(driver, 500)
