from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time

air_peace_url = "https://www.flyairpeace.com/"
chrome_driver_path = "/Users/kingbarz/Documents/Development/chromedriver"
wait_time = 60 * 60


class AirPeace:
    def __init__(self):
        self.service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(wait_time)
        self.driver.get(air_peace_url)

    def get_today_flight_details(self, origin, destination):
        # 1. Handle Pop-up
        pop_up_close = self.driver.find_element(By.XPATH, "/html/body/header/div[3]/div[1]/div/div/div/a[1]/button")
        time.sleep(3)
        pop_up_close.click()

        # 2a. Form Interaction
        # 2b. Switch to frame
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "reservation_form"))

        # 3. Select Origin (frame in element)
        from_dropdown = self.driver.find_element(By.NAME, "Origin")
        fdd = Select(from_dropdown)
        fdd.select_by_value(origin)

        # 4. Select Destination
        to_dropdown = self.driver.find_element(By.NAME, "Destination")
        tdd = Select(to_dropdown)
        tdd.select_by_value(destination)

        # 5. Select ticket type
        ticket_type = self.driver.find_element(By.XPATH,
                                               "/html/body/form/div[5]/div/div[1]/div[3]/div/div/div/div/label[2]")
        ticket_type.click()

        # 6. Submit
        submit = self.driver.find_element(By.ID, "submitButton")
        time.sleep(3)
        submit.click()

        # 7. Switch back to main page(back one frame)

        time.sleep(10)
        self.driver.switch_to.default_content()

        # 8. Get all flight details

        flight_rows = self.driver.find_elements(By.XPATH, '//div[@class="panel-heading flt-panel-heading "]')

        price_list = []
        time_list = []

        for WebElement in flight_rows:
            element_html = WebElement.get_attribute("outerHTML")
            element_soup = BeautifulSoup(element_html, "html.parser")

            # Price

            price = element_soup.find("div", {"class": "col-lg-12 fare-price-small"}).text.replace("\n", "")
            price_list.append(price)

            # Departure and arrival times

            time_of_flight = element_soup.find_all("span", {"class": "time"})
            flight_time = [x.text for x in time_of_flight]
            time_list.append(flight_time)

        flight_info = {}

        for num in range(len(price_list)):
            flight_info[num] = price_list[num], time_list[num]

        print(flight_info)