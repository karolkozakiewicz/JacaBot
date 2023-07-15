import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import threading
import requests
        
class StreamChecker():
    
    def __init__(self) -> None:
        self.options = Options()
        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.link = "https://ok.ru/videoembed/6364365004365"
        # self.link = "https://ok.ru/videoembed/7451630050833" #test
        self.driver.get(self.link)
        self.last_state = False
        self.status = None
        time.sleep(2)
        
    
    def site_refresh(self):
        while True:
            time.sleep(15)
            self.driver.get(self.link)
    
    def start_checking_stream(self) -> None:
        self.thread = threading.Thread(target=self.check_stream_status)
        self.thread_refresh = threading.Thread(target=self.site_refresh)
        self.thread.start()
        self.thread_refresh.start()
    
    def check_stream_status(self, sleep_time: int = 0) -> None:
        def _():
            time.sleep(sleep_time)
            try:
                div_element = self.driver.find_element(By.XPATH, "//div[@class='vid-card_live __ended']")
                return False
            except NoSuchElementException:
                return True

        while True:
            __ = self.program_status()
            if "OFF" in __:
                pass
            elif "ON" in __:
                x = _()  
                
                #stream zostal wlaczony
                if self.last_state == False and x == True:
                    self.last_state = x
                    self.status = True
                    
                #stream byl wlaczony ale już jest wyłączony
                elif self.last_state == True and x == False:
                    self.last_state = x
                    self.status = False
                    
                #stream jest wylaczony
                elif self.last_state == False and x == False:
                    self.last_state = x
                    self.status = False
                
                #stream jest włączony
                elif self.last_state == True and x == True:
                    self.last_state = x
                    self.status = True
                             
                        
            elif "EXIT" in __:
                print('Quitting....')
                break
     
    def program_status(self):
        return requests.get("http://192.168.0.215/status.html").text
            





