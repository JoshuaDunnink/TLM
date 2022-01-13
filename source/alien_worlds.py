from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
import geckodriver_autoinstaller
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pyautogui
from random import randint

approve_position = (300, 550)
geckodriver_autoinstaller.install()


class Driver:
    def __init__(self, profile=None):
        self.user_agent = (
            "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/"
            "537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/"
            "87.0.4280.141 Mobile Safari/537.36"
        )
        if not profile:
            self.profile = webdriver.FirefoxProfile(
                "/Users/FH13NF/Library/Application Support"
                "/Firefox/Profiles/sux3dl6h.default-release"
            )
        else:
            self.profile = profile

        self.profile.set_preference("dom.webdriver.enabled", False)
        self.profile.set_preference("useAutomationExtension", False)
        self.profile.set_preference(
            "general.useragent.override", self.user_agent
        )
        self.profile.update_preferences()
        self.options = Options()
        # self.options.add_argument("--headless")
        self.desired = DesiredCapabilities.FIREFOX
        self.driver = webdriver.Firefox(
            firefox_profile=self.profile,
            desired_capabilities=self.desired,
            options=self.options,
        )


def count_down(driver):
    countdown = ""
    while not countdown:
        countdown = driver.driver.find_element_by_id("countdown").text
        sleep(1)
    print("current countdown: " + countdown)

    hours, minutes, seconds = [int(number) for number in countdown.split(":")]
    if hours != 0 or minutes != 0 or seconds != 0:
        return (hours, minutes, seconds)
    else:
        return (0, 0, 0)


def click_mine():
    # driver.driver.find_element_by_id("mine").click()
    pyautogui.moveTo(80, 300, 0.5)
    sleep(1)
    pyautogui.click(80, 300)
    sleep(1)
    pyautogui.click(80, 300)


def click_claim():
    pyautogui.moveTo(80, 350, 0.5)
    sleep(1)
    pyautogui.click(80, 350)
    sleep(1)
    pyautogui.click(80, 350)
    # driver.driver.find_element_by_id("claim").click()
    sleep(2)


def click_approve():
    # driver.driver.switch_to.window(driver.driver.window_handles[1])
    # if (
    #     "Transaction Request" in driver.driver.page_source
    #     and "mine" in driver.driver.page_source
    # ):
    #     approve = driver.driver.find_element_by_class_name("button-text")
    #     if approve.text == "Approve":
    #         approve.click()
    #     else:
    #         exit(1)
    sleep(2)
    pyautogui.moveTo(300, 550, 0.5)
    sleep(2)
    pyautogui.click(x=300, y=550)
    sleep(1)
    pyautogui.click(x=300, y=550)
    sleep(2)
    # driver.driver.switch_to.window(main_window)


def move_mouse(speed=1, enabled=True):
    if enabled:
        width, height = pyautogui.size()
        random_width = randint(0, width)
        random_height = randint(0, height)
        pyautogui.moveTo(random_width, random_height, 1 / speed)


def mine(driver):
    if len(driver.driver.window_handles) == 1:
        click_mine()
    countdown = count_down(driver)
    if countdown != (0, 0, 0):
        return countdown
    while countdown == (0, 0, 0):
        sleep(2)
        move_mouse(4)
        if len(driver.driver.window_handles) == 1:
            click_mine()
        sleep(2)
        if len(driver.driver.window_handles) > 1:
            click_approve()
        else:
            click_claim()
        countdown = count_down(driver)
    return (0, 0, 0)


def main():
    driver = Driver()
    driver.driver.get("https://play.pocketaliens.io/")
    while True:
        move_mouse(4)
        main_window = driver.driver.window_handles[0]
        main_window_title = driver.driver.title
        while (
            driver.driver.find_element_by_id("loginresponse").text
            != "eqqba.wam"
        ):
            driver.driver.find_element_by_id("login").click()
            sleep(5)
        balance = driver.driver.find_element_by_id("balance").text
        print("current balance: " + balance)

        move_mouse(4)
        if len(driver.driver.window_handles) > 1:
            click_approve()

        move_mouse(4)
        if not driver.driver.title == main_window_title:
            driver.driver.switch_to.window(main_window)

        move_mouse(4)
        count_down = mine(driver)
        sleep_time = (
            count_down[0] * 3600 + count_down[1] * 60 + count_down[2] + 5
        )

        print("going to sleep for " + str(sleep_time) + " seconds")
        now = datetime.now()
        delta = now + timedelta(seconds=sleep_time)
        while now < delta:
            if len(driver.driver.window_handles) > 1:
                click_approve()
            sleep(60)
            move_mouse(4)
            sleep(1)
            move_mouse(4)
            now = datetime.now()
        driver.driver.refresh()


main()
