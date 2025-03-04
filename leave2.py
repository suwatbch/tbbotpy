import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)
current_url = driver.current_url

def print_table_data():
    # รอให้ตารางโหลดเสร็จ
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

    # ดึงข้อมูลจากตาราง
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            print(cell.text, end=' | ')
        print()

try:
    if "https://leave.swmaxnet.com/" in current_url:
        driver.get("https://leave.swmaxnet.com/#module=workday")
        WebDriverWait(driver, 10).until(EC.url_contains('/#module=workday'))
        
        car = 3
        for _ in range(car, 0, -1):
            # ดึงข้อมูลตาราง
            print_table_data()

            # รอ 1 วินาที
            time.sleep(1)

            # รีเฟรชหน้า
            driver.refresh()

        print("")
        input()

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    input("กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()