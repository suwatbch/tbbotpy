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

        # รอให้ Dialog เปิด (ใช้ข้อความ "ยืนยันว่าไม่ใช่บอท" เป็นตัวตรวจสอบ)
        try:
            dialog = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'ยืนยันว่าไม่ใช่บอท')]"))
            )
            print("✅ Dialog เปิดสำเร็จ!")

            time.sleep(1)

            # ✅ ค้นหา iframe ของ reCAPTCHA (ใช้ CSS Selector)
            # iframes = driver.find_elements(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
            # if len(iframes) > 0:
            #     driver.switch_to.frame(iframes[0])  # ✅ เปลี่ยนไปที่ iframe แรก
            #     print("✅ เปลี่ยนไปที่ iframe ของ reCAPTCHA")
            # else:
            #     raise TimeoutException("❌ ไม่พบ iframe ของ reCAPTCHA")

            # ✅ ค้นหาและคลิก checkbox ของ reCAPTCHA
            checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
            )
            checkbox.click()
            print("✅ คลิก reCAPTCHA สำเร็จ!")

        except TimeoutException:
            print("❌ Dialog หรือ reCAPTCHA ไม่โหลดภายใน 5 วินาที!")

except (KeyboardInterrupt, WebDriverException) as e:
    print("❌ หยุดการทำงาน:", str(e))

finally:
    input("🔴 กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()
