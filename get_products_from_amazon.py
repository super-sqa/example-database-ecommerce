

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains





def click_all_next_btns(driver):

    next_page = driver.find_elements(By.CSS_SELECTOR, "a.a-button.a-button-image.a-carousel-button.a-carousel-goto-nextpage")
    for i in next_page:
        # breakpoint()
        ActionChains(driver).move_to_element(i).perform()
        i.click()
        time.sleep(1)
    print("Click next page on the carrousel.")

def get_description_name(driver):
    all_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div.a-carousel-controls div.zg-carousel-general-faceout div.p13n-sc-truncate-desktop-type2')
    print(f"Got {len(all_descriptions)} product elements.")
    for i in all_descriptions:
        i.click()
        time.sleep(1)

def get_product_lines(driver):

    all_products_on_page = driver.find_elements(By.CSS_SELECTOR, 'div.zg-carousel-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal[tabindex="-1"]')
    return [i.get_attribute('href') for i in all_products_on_page]


def get_all_links(driver):

    # all_links = []
    for i in range(30):
        links = get_product_lines(driver)
        # all_links.extend(links)
        click_all_next_btns(driver)
        with open('amz_links.csv', 'a') as f:
            for j in links:
                f.write(j + '\n')

        # print(len(set(all_links)))
        # breakpoint()

def get_details(links_list, driver):
    counter = 0
    with open('amz_detail2.csv', 'a') as f:
        for link in links_list:
            time.sleep(2)
            counter += 1
            print(f"Getting {counter} of {len(links_list)}")
            driver.get(link)
            title = driver.find_element(By.ID, "title").text
            description_1 = driver.find_element(By.CSS_SELECTOR, 'div#feature-bullets span.a-list-item').text
            # price = driver.find_element(By.CSS_SELECTOR, 'div.a-section.a-spacing-none.aok-align-center').text
            print(f"Title: {title}")
            print(f"description_1: {description_1}")
            # print(f"price: {price}")
            f.write(f"{title},{description_1}\n")
            f.write(f"======")

if __name__ == '__main__':
    driver = webdriver.Chrome()
    #
    # driver.get("https://www.amazon.com/gp/new-releases/?ref_=nav_cs_newreleases")

    # get_all_links(driver)

    with open('amz_links.csv', 'r') as f:
        content = f.readlines()
        # breakpoint()
        print('foo')

    non_duplicate = set(content)
    get_details(non_duplicate, driver)
