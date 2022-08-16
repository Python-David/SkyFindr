from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

air_peace_url = "https://www.flyairpeace.com/"
chrome_driver_path = "/Users/kingbarz/Documents/Development/chromedriver"
wait_time = 60


class AirPeace:
    def __init__(self):
        self.driver = None
        self.service = None

    def get_today_flight_details(self, origin, destination):
        try:
            # 0. Open the landing page
            self.service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.implicitly_wait(wait_time)
            self.driver.get(air_peace_url)

            # 1. Handle Pop-up
            pop_up_close = self.driver.find_element(By.XPATH, "/html/body/header/div[3]/div[1]/div/div/div/a[1]/button")
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

                price = element_soup.find("div", {"class": "col-lg-12 fare-price-small"})
                if price is None:
                    pass
                    price_list.append("SOLD OUT")
                else:
                    price_list.append(price.text.replace("\n", ""))

                # Departure and arrival times

                time_of_flight = element_soup.find_all("span", {"class": "time"})
                flight_time = [x.text for x in time_of_flight]
                time_list.append(flight_time)

            flight_info = {}

            for num in range(len(price_list)):
                flight_info[num] = price_list[num], time_list[num]

            if len(flight_info) > 0:
                return flight_info
            else:
                self.driver.close()
                return "Sorry, no flights found."

        except NoSuchElementException:
            return "Cannot return flight details for this destination. Maybe try a different airline for the " \
                   "destination you want to go. "
        except ElementClickInterceptedException:
            return "Network error, please try again."
        except StaleElementReferenceException:
            return "Invalid return date selected. Try picking a closer date"

    def get_any_day_flight_details_one_way(self, user_day, user_month, user_year, origin, destination):
        try:
            # 0. Open the landing page
            self.service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.implicitly_wait(wait_time)
            self.driver.get(air_peace_url)

            # 1. Handle Pop-up
            pop_up_close = self.driver.find_element(By.XPATH, "/html/body/header/div[3]/div[1]/div/div/div/a[1]/button")
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

            # Set Date

            date_picker = self.driver.find_element(By.ID, "departuredate")
            date_picker.click()

            forward_button = self.driver.find_element(By.XPATH, '//span[@class="ui-icon ui-icon-circle-triangle-e"]')

            while True:
                month = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
                year = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text
                if month == user_month and year == user_year:
                    break
                forward_button.click()

            all_dates = self.driver.find_elements(By.XPATH, '//table[@class="ui-datepicker-calendar"]//a')

            for date in all_dates:
                if date.text == user_day:
                    date.click()
                    break

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

                price = element_soup.find("div", {"class": "col-lg-12 fare-price-small"})
                if price is None:
                    pass
                    price_list.append("SOLD OUT")
                else:
                    price_list.append(price.text.replace("\n", ""))

                # Departure and arrival times

                time_of_flight = element_soup.find_all("span", {"class": "time"})
                flight_time = [x.text for x in time_of_flight]
                time_list.append(flight_time)

            flight_info = {}

            for num in range(len(price_list)):
                flight_info[num] = price_list[num], time_list[num]

            if len(flight_info) > 0:
                return flight_info
            else:
                self.driver.close()
                return "Sorry, no flights found."

        except NoSuchElementException:
            return "Cannot return flight details for this destination. Maybe try a different airline for the " \
                   "destination you want to go. "
        except ElementClickInterceptedException:
            return "Network error, please try again."
        except StaleElementReferenceException:
            return "Invalid return date selected. Try picking a closer date"

    def get_any_day_flight_details_return(self, user_day, user_month, user_year, user_return_day, user_return_month,
                                          user_return_year, origin, destination):
        try:
            # 0. Open the landing page
            self.service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.implicitly_wait(wait_time)
            self.driver.get(air_peace_url)

            # 1. Handle Pop-up
            pop_up_close = self.driver.find_element(By.XPATH, "/html/body/header/div[3]/div[1]/div/div/div/a[1]/button")
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
                                                   "/html/body/form/div[5]/div/div[1]/div[3]/div/div/div/div/label[1]")
            ticket_type.click()

            # 6a. Set Departure Date

            date_picker = self.driver.find_element(By.ID, "departuredate")
            date_picker.click()

            forward_button = self.driver.find_element(By.XPATH, '//span[@class="ui-icon ui-icon-circle-triangle-e"]')

            while True:
                month = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
                year = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text
                if month == user_month and year == user_year:
                    break
                forward_button.click()

            all_dates = self.driver.find_elements(By.XPATH, '//table[@class="ui-datepicker-calendar"]//a')

            for date in all_dates:
                if date.text == user_day:
                    date.click()
                    break

            # 6b. Set Return Date

            date_picker = self.driver.find_element(By.ID, "returndate")
            date_picker.click()

            forward_button = self.driver.find_element(By.XPATH, '//span[@class="ui-icon ui-icon-circle-triangle-e"]')

            while True:
                month = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
                year = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text
                if month == user_return_month and year == user_return_year:
                    break
                forward_button.click()

            all_dates = self.driver.find_elements(By.XPATH, '//table[@class="ui-datepicker-calendar"]//a')

            for date in all_dates:
                if date.text == user_return_day:
                    date.click()
                    break

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
            flight_type = []

            for WebElement in flight_rows:
                element_html = WebElement.get_attribute("outerHTML")
                element_soup = BeautifulSoup(element_html, "html.parser")

                # Price

                price = element_soup.find("div", {"class": "col-lg-12 fare-price-small"})
                if price is None:
                    pass
                    price_list.append("SOLD OUT")
                else:
                    price_list.append(price.text.replace("\n", ""))

                # Departure and arrival times

                time_of_flight = element_soup.find_all("span", {"class": "time"})
                flight_time = [x.text for x in time_of_flight]
                time_list.append(flight_time)

                # Date of flight

                date_of_flight = element_soup.find_all("span", {"class": "flightDate"})
                flight_date = [x.text for x in date_of_flight]
                flight_day = flight_date[0].split()[1]
                if flight_day == user_day:
                    flight_type.append("Outbound")
                else:
                    flight_type.append("Inbound")

            flight_info = {}

            for num in range(len(price_list)):
                flight_info[num] = price_list[num], time_list[num], flight_type[num]

            if len(flight_info) > 0:
                return flight_info
            else:
                return "Sorry, no flights found."

            # self.driver.close()

        except NoSuchElementException:
            return "Cannot return flight details for this destination. Maybe try a different airline for the " \
                   "destination you want to go. "
        except ElementClickInterceptedException:
            return "Network error, please try again."
        except StaleElementReferenceException:
            return "Invalid return date selected. Try picking a closer date"
