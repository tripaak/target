from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.options import Options
import settings, time, random
import logging

# implement logger & set level
logger = logging.getLogger('target.com')
logger.setLevel(logging.INFO)
logger.propagate = False

# Define stream/file handler 
stream_handeler = logging.StreamHandler()
stream_handeler.setLevel(logging.INFO)
logger.addHandler(stream_handeler)

#define formatter and attatch to handeler 
formatter = logging.Formatter('<%(levelname)s>  <%(asctime)s>  <%(name)s>  %(message)s')
stream_handeler.setFormatter(formatter)

class Target:
    def __init__(self):
        starting_msg = "Starting Target"
        self.browser = self.init_driver()
        if self.browser:
            self.product_image = None
            self.TIMEOUT_SHORT = 5
            self.TIMEOUT_LONG = 20
            self.did_submit = False
            self.failed = False
            self.retry_attempts = 10


    def init_driver(self):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument('--log-level=3')
        driver = webdriver.Edge(options=options)
        return driver

    def login(self):
        self.browser.get("https://www.target.com")
        accountBtn = wait(self.browser, self.TIMEOUT_LONG).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Account, sign in"]'))
        )
        time.sleep(random.uniform(0.5, 1.5))
        accountBtn.click()
        time.sleep(random.uniform(0.5, 1.5))
        signIn = wait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'a[data-test="accountNav-signIn"]'))
        )
        if signIn:
            logger.info("Home Page loaded ")
            signIn.click()
        


    def authenticate(self):
        if self.browser.find_element('id','username'):
            for key in settings.target_user:
                self.browser.find_element(By.XPATH, '//input[@id="username"]').send_keys(key)
                time.sleep(random.uniform(0.5, 1.5))
        
            for key in settings.target_pass:
                self.browser.find_element(By.XPATH, '//input[@id="password"]').send_keys(key)
                time.sleep(random.uniform(0.5, 1.5))

            time.sleep(random.uniform(0.5, 1.5))    
            loginBtn = wait(self.browser, self.TIMEOUT_LONG).until(
                EC.element_to_be_clickable(self.browser.find_element(By.XPATH,'//button[@id="login"]'))
            )
            time.sleep(random.uniform(0.5, 1.5))
            loginBtn.click()
            logger.info(f"Login passed for {settings.target_user}")
            time.sleep(random.uniform(0.5, 1.5))
        else:
            self.browser.find_element_by_xpath('//input[@id="password"]').send_keys(settings.target_pass)

            loginBtn = wait(self.browser, self.TIMEOUT_LONG).until(
                EC.presence_of_element_located((By.XPATH,'//button[@id="login"]'))
            )
            time.sleep(random.uniform(0.5, 1.5))
            loginBtn.click()

    def go_to_past_orders(self):
        time.sleep(random.uniform(0.5,2.5))
        enable  = self.browser.find_element(By.CSS_SELECTOR, 'a[data-test="@web/AccountLink"]')
        time.sleep(random.uniform(0.5,2.5))
        enable.click()
        time.sleep(random.uniform(0.5,2.5))
        order  = self.browser.find_element(By.CSS_SELECTOR, 'a[data-test="accountNav-orders"]')
        time.sleep(random.uniform(0.5,2.5))
        order.click()
        time.sleep(random.uniform(0.5, 3.5))
        validate_order_page = wait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'div[data-test="order-history-back-button"]'))
        )
        time.sleep(random.uniform(0.5, 2.5))
        if validate_order_page:
            logger.info("Navigation to order details is passed ")
        time.sleep(random.uniform(0.5, 1.5))

    
        
    
if __name__ == '__main__':
    t = Target()
    t.login()
    time.sleep(random.uniform(0.5, 2.5))
    logger.info(f"Authentication function started for {settings.target_user}")
    t.authenticate()
    time.sleep(random.uniform(0.5, 5.5))
    t.go_to_past_orders()