import random
import time, logging

log = logging.getLogger(__name__)

import getconfig
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


wait_on_search_result = getconfig.props["wait_on_search_result"]
search_keywords = getconfig.props["search_keywords"].split(',')
search_engine = getconfig.props["search_engine"]
repeat_all = getconfig.props["repeat_all"]

log.info("wait_on_search_result: " + wait_on_search_result + " min")
log.info("search_keywords list: " + str(search_keywords))
log.info("search_engine: " + search_engine)

def start():
    repeat_count = 1
    if repeat_all.lower() == "yes":
        repeat_count = 100

    for i in range(0, repeat_count):

        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        log.info("Browser opened")
        driver.maximize_window()
        log.info("Browser maximized")


        for keyword in search_keywords:
            try:
                driver.get(search_engine)
                log.info("Navigated to : "+ search_engine)
                driver.find_element(by=By.ID, value = "search").send_keys(keyword)
                log.info("Found search box and written the keyword: " + keyword)
                driver.find_element(by=By.CLASS_NAME, value= "input-group-btn").click()
                log.info("Found search button and clicked")
                log.info("waiting for 5 sec for search result to be apeared")
                time.sleep(5)
                log.info("Trying to find all the search results and their links")
                all_links_elements =  driver.find_elements(by=By.TAG_NAME, value='a')
                all_links_list =[]
                for link in all_links_elements:
                    try:
                        if "presearch" not in link.get_attribute("href"):
                            all_links_list.append(link.get_attribute("href"))
                    except:
                        pass
                all_links_list = list(set(all_links_list))
                log.info("Found below links (count- "+str(len(all_links_list))+"): ")
                log.info(all_links_list)

                random_link_to_navigate = all_links_list[random.randint(1,13)]
                log.info("Navigating to : "+ random_link_to_navigate)
                driver.get(random_link_to_navigate)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(int(wait_on_search_result)*60)
            except:
                pass


if __name__ == '__main__':
    start()
