from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com")

search_box = driver.find_element(By.NAME, "q")
search_box.clear()
search_box.send_keys("who is the president of america?")
search_box.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 15)
 
card = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//div[contains(., 'Search Assist')]"
    ))
)
 
answer_text = card.get_attribute("innerText")

print("Search Assist Answer:\n")
print(answer_text[:500])

# driver.quit()
