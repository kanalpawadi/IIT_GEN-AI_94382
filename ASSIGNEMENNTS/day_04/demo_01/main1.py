#1. Scrape Internship information and batches from Sunbeam website.
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# start the selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# load desired page in the browser
driver.get("https://www.sunbeaminfo.in/internship")
print("Page Title:", driver.title)
# define wait strategy
driver.implicitly_wait(5)
# interact with web controls
table_body=driver.find_element(By.CLASS_NAME,"table")
table_rows=table_body.find_elements(By.TAG_NAME,"tr")

for row in table_rows:
    #print(row.text)
    cols=row.find_elements(By.TAG_NAME,"td")
    if len(cols) == 8:
        info = {
            "Sr_No": cols[0].text,
            "Batch": cols[1].text,
            "Batch Duration": cols[2].text,
            "Start Date": cols[3].text,
            "End Date": cols[4].text,
            "Time": cols[5].text,
            "Fees (Rs.)": cols[6].text,
            "Download Brochure": cols[7].text
        }
        print(info)

#stop the session 
driver.quit()