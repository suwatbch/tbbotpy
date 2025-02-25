import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options

try:
    # ตั้งค่า Chrome Driver
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=chrome_options)
    current_url = driver.current_url

    if "http://localhost:3000/" in current_url:
        driver.get("http://localhost:3000/")

        # รอและคลิกปุ่ม "เปิด DIALOG"
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='เปิด Dialog']"))
        )
        button.click()
        print("✅ คลิกปุ่ม 'เปิด DIALOG' สำเร็จ!")

        time.sleep(1)

        try:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, ":r1:"))
            )
            confirm_button.click()
            print("✅ คลิกปุ่ม 'ยืนยัน' สำเร็จ!")
        except TimeoutException:
            print("❌ ปุ่ม 'ยืนยัน' ไม่สามารถคลิกได้ภายใน 10 วินาที!")

except (KeyboardInterrupt, WebDriverException) as e:
    print("❌ หยุดการทำงาน:", str(e))

finally:
    input("🔴 กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()
