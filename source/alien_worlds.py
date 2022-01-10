from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
import geckodriver_autoinstaller
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pyautogui

approve_position= (300, 550)
geckodriver_autoinstaller.install()

user_agent = "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36"
profile = webdriver.FirefoxProfile(
    "/Users/FH13NF/Library/Application Support"
    "/Firefox/Profiles/sux3dl6h.default-release"
)

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference("useAutomationExtension", False)
profile.set_preference("general.useragent.override", user_agent)
profile.update_preferences()
options = Options()
# options.add_argument("--headless")
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(
    firefox_profile=profile, desired_capabilities=desired, options=options
)


def count_down():
    countdown = ""
    while not countdown:
        countdown = driver.find_element_by_id("countdown").text
        sleep(1)
    print("current countdown: " + countdown)

    hours, minutes, seconds = [int(number) for number in countdown.split(":")]
    if hours != 0 or minutes != 0 or seconds != 0:
        return (hours, minutes, seconds)
    else:
        return (0, 0, 0)


def mine():
    driver.find_element_by_id("mine").click()
    countdown = count_down()
    if countdown != (0, 0, 0):
        return countdown
    while countdown == (0, 0, 0):
        driver.find_element_by_id("claim").click()
        sleep(5)
        pyautogui.click(x=300, y=550)
        sleep(1)
        pyautogui.click(x=300, y=550)
        sleep(10)
        countdown = count_down()
    return (0, 0, 0)


def main():
    while True:
        driver.get("https://play.pocketaliens.io/")
        while driver.find_element_by_id("loginresponse").text != "eqqba.wam":
            driver.find_element_by_id("login").click()
            sleep(5)

        balance = driver.find_element_by_id("response").text
        print("current balance: " + balance)
        count_down = mine()
        sleep_time = (
            count_down[0] * 3600 + count_down[1] * 60 + count_down[2] + 5
        )

        print("going to sleep for " + str(sleep_time) + " seconds")
        now = datetime.now()
        delta = now + timedelta(seconds=sleep_time)
        while now < delta:
            sleep(60)
            pyautogui.click(x=300, y=550)
            sleep(1)
            pyautogui.click(x=300, y=550)
            now = datetime.now()


main()
