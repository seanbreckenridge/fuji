#!/usr/local/env python3

import argparse
import sys
import traceback
from time import sleep
from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup

from make_credentials import generate


def wait():
    """Wait for time between keystrokes."""
    sleep(randint(1, 5) / 60)


def enter_text_slow(box, text):
    """Enter text slow; Fuji fails to work if send_keys is done all at once."""
    for c in text:
        box.send_keys(c)
        wait()


def valid_fuji(el):
    """Checks if the given email element is a valid fuji email; its from Fuji and was recieved recently."""
    subject_text = el.find_element_by_css_selector("div.all_message-min > div.all_message-min_text").text
    time_ago = el.find_element_by_css_selector(".all_message-min_datte").text
    if 'Fujitv.live' in subject_text:
        return "minute" in time_ago or time_ago == "moments ago"
    return False


def find_fuji_activation(driver):
    """Finds the fuji activation email."""
    try:
        # Wait for emails to load in
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "all_message-min_text")))
    except:
        return []
    emails = driver.find_elements_by_css_selector("li.all_message-item")
    fuji_emails = list(filter(valid_fuji, emails))
    return fuji_emails


def get_iframe_contents(driver):
    """Gets the iframe contents -- where the message body resides."""
    driver.switch_to.frame(driver.find_element_by_css_selector("iframe#msg_body"))
    contents = driver.execute_script("return document.body.innerHTML;")
    driver.switch_to.default_content()
    return contents


def wait_for_message(driver):
    """Waits for the iframe to load."""
    for _ in range(20):  # wait 20 seconds for message to load
        sleep(1)
        contents = get_iframe_contents(driver)
        if contents.strip():  # if iframe has text in it; email body has loaded
            return contents
    return None


def create_webdriver(chromedriver_path, hide):
    """Creates a webdriver, hides if requested."""
    options = Options()
    if hide:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    return webdriver.Chrome(chromedriver_path, chrome_options=options)


def confirm_email(driver, mailinator_account_url, hide):
    """Goes to mailinator, finds the activation email and activates the account."""

    driver.get(mailinator_account_url)
    fuji = find_fuji_activation(driver)
    if len(fuji) == 0:
        print("Couldn't find an email from Fuji... ")
        return False
    fuji_email = fuji.pop(0)
    fuji_email.click()
    contents = wait_for_message(driver)
    if wait_for_message is None:
        print("Couldn't find message contents...")
        return False
    activation_link = soup(contents, 'html.parser').find("a")["href"]
    driver.get(activation_link)
    return True


def fuji_register(driver, email_address, password, hide):
    """Registers on Fuji with a random username and password."""

    fuji_register_page = r"https://fujitv.live/register"

    driver.get(fuji_register_page)

    form_input = driver.find_element_by_id("regform")
    email_input = form_input.find_element_by_css_selector("input[name=account]")
    password_input = form_input.find_element_by_css_selector("input[name=password]")
    confirm_password = form_input.find_element_by_css_selector("input[name=conpassword]")

    enter_text_slow(email_input, email_address)
    enter_text_slow(password_input, password)
    enter_text_slow(confirm_password, password)

    driver.execute_script("document.getElementById('agree').checked = true")
    wait()
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#regform > div > div > button.btn-success'))
    )
    wait()
    driver.execute_script("document.getElementById('regform').submit()")
    wait_for_alert = WebDriverWait(driver, 20)
    wait_for_alert.until(EC.alert_is_present())
    alert = driver.switch_to_alert()
    alert.accept()


def run(driver, use_hidden, open_login):
    """Calls other functions; creates the account on Fuji and confirms email."""

    # create credentials
    username, password = generate(name_length=randint(3, 6))
    email_handle, mailinator_account_url = f"{username}@mailinator.com", \
        f"https://www.mailinator.com/v2/inbox.jsp?zone=public&query={username}"

    # Register for Fuji
    fuji_register(driver, email_handle, password, use_hidden)

    # Confirm Email from Fuji on Mailinator
    confirmed_email = confirm_email(driver, mailinator_account_url, use_hidden)

    if confirmed_email:
        print("Registered Successfully.")
        print(email_handle)
        print(password)
        if open_login:
            import webbrowser
            webbrowser.open_new_tab("https://fujitv.live/logon")
    else:
        print("Failed to confirm email.")


def get_options():
    """Gets options from user"""
    parser = argparse.ArgumentParser(description="Creates an account on Fujitv.live.")
    parser.add_argument("--hidden", help="Hide the ChromeDriver.", action="store_true")
    parser.add_argument("-o", "--open-logon", help="Open the login page.", action="store_true")
    parser.add_argument("-c", "--chromedriver-path", help="Provides the location of ChromeDriver. Should probably be the full path.")
    args = parser.parse_args()
    if args.chromedriver_path is None:
        args.chromedriver_path = "/usr/local/bin/chromedriver"  # default on mac
    return args.hidden, args.open_logon, args.chromedriver_path


def main():
    """Gets options, runs program, cleans up selenium on exception."""
    use_hidden, open_login, chromedriver_path = get_options()
    try:
        driver = create_webdriver(chromedriver_path, use_hidden)
        run(driver, use_hidden, open_login)
    except:
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
