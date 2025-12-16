#selenium demo01
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com/")
print("Initial page Title is: ",driver.title)

#define wait stratergy --set one time in the appication 
driver.implicitly_wait(5)

#access the control on the page 
# time.sleep(5)
search_box=driver.find_element(By.NAME,"q")

#interact with the control 
#for ch in "DKTE College Ichalkaranji ":
#    search_box.send_keys(ch)
#    time.sleep(0.5)

search_box.send_keys("DKTE College Ichalkaranji ")
search_box.send_keys(Keys.RETURN)

#wait for the result 
print("later Page Title:",driver.title)

#stop the session 
time.sleep(10)
driver.quit()
