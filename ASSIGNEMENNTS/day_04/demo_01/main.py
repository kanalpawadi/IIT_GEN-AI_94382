from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.sunbeaminfo.in/internship")
print("Page Title:", driver.title)

wait = WebDriverWait(driver, 10)

# Expand the accordion (VERY IMPORTANT)
accordion_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
)
driver.execute_script("arguments[0].click();", accordion_btn)

# Wait for table inside expanded accordion
table = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//div[@id='collapseSix']//table")
    )
)

rows = table.find_elements(By.XPATH, ".//tbody/tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) == 5:
        info = {
            "Technology": cols[0].text.strip(),
            "Aim": cols[1].text.strip(),
            "Prerequisite": cols[2].text.strip(),
            "Learning": cols[3].text.strip(),
            "Location": cols[4].text.strip(),
        }
        print(info)

driver.quit()
