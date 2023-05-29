import time

import os
# from dotenv import load_dotenv
# load_dotenv()

from selenium import webdriver 

import pandas as pd

# either use .env or manually set params here and be careful not to push your credentials
USERNAME = os.environ["USERNAME"] # os.getenv("USERNAME", "")
PASSWORD = os.environ["PASSWORD"] # os.getenv("PASSWORD", "")

def login(driver):
    """ 
    Description: Log in to Linkedin account
    """
    # Set username
    username = driver.find_element('xpath', '//input[@id="session_key"]')
    username.send_keys(USERNAME)
    
    time.sleep(2)

	# Set password
    password = driver.find_element('xpath', '//input[@id="session_password"]')
    password.send_keys(PASSWORD)				
    time.sleep(2)

	# Log on
    the_xpath = '//button[@data-id="sign-in-form__submit-btn"]'
    login_button = driver.find_element('xpath', the_xpath)
    login_button.click()
    time.sleep(30)

def connect(driver, person_profile_page: str):
    """
    Description: Attempt to connect on Linkedin. Return the page if not successful.
    """
    # connection button on the main actions list
    driver.get(person_profile_page)
    time.sleep(2)
    try:
        # connect
        connect_button = driver.find_element('xpath', '//div[@class="pv-top-card-v2-ctas "]//button/span[text()="Connect"]')
        connect_button.click()

        time.sleep(2)

        # send connection

        send_connection_button = driver.find_element('xpath', '//div[@class="artdeco-modal__actionbar ember-view text-align-right"]//button/span[text()="Send"]')
        send_connection_button.click()
        print(f"Sent connection to {person_profile_page} through main connect button")
    except Exception as e:
        try:
            # reset to person's page
            driver.get(person_profile_page)
            time.sleep(2)

            # assume connection button is hidden away
            more_button = driver.find_element('xpath', '//div[@class="pv-top-card-v2-ctas "]//button/span[text()="More"]')
            more_button.click()
            
            time.sleep(2)

            connect_within_more_button = driver.find_element('xpath', '//div[@class="pv-top-card-v2-ctas "]//div//span[text()="Connect"]')
            connect_within_more_button.click()

            time.sleep(2)

            send_connection_button = driver.find_element('xpath', '//div[@class="artdeco-modal__actionbar ember-view text-align-right"]//button/span[text()="Send"]')
            send_connection_button.click()

            # may ask for additional steps, not sure
            
            print(f"Sent connection to {person_profile_page} through connect button hidden in 'more' button")
            
        except Exception as e2:
            print(e2)
            return person_profile_page
    
    return

def main():
    driver = webdriver.Chrome()

    driver.get("https://www.linkedin.com/home")

    login(driver)

    invite_df = pd.read_csv("data/invite_df.csv")

    not_invited_list = []
    for page in invite_df.profile_pages:
        res = connect(driver, person_profile_page=page)
        if res:
            not_invited_list.append(res)
    
    # save off pages that we were not able to successfully send a connection
    pd.DataFrame(not_invited_list, columns=["profile_pages"]).to_csv("data/not_invited_df.csv", index=False)

    return

if __name__=="__main__":
    main()