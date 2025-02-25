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
    driver.get("http://localhost:3000/")

    # รอและคลิกปุ่ม "เปิด DIALOG"
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='เปิด Dialog']"))
    )
    button.click()
    print("✅ คลิกปุ่ม 'เปิด DIALOG' สำเร็จ!")

    time.sleep(0.5)

    # สลับไปยัง iframe ของ reCAPTCHA
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # คลิกที่ Checkbox reCAPTCHA
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
    ).click()
    print("✅ คลิก Checkbox reCAPTCHA สำเร็จ!")

    # กลับมาที่หน้าเว็บหลัก
    driver.switch_to.default_content()
    print("✅ กลับมาที่หน้าเว็บหลัก")

    # ค้นหา iframe ของ reCAPTCHA อีกครั้ง
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    iframe_elements = driver.find_elements(By.TAG_NAME, "iframe")

    captcha_iframe = None
    captcha_has_images = False

    # ตรวจสอบว่า iframe ใดเป็นของ reCAPTCHA
    for iframe in iframe_elements:
        iframe_src = iframe.get_attribute("src")
        cd_frame_id = iframe.get_attribute("cd_frame_id_")

        if "google.com/recaptcha/api2" in iframe_src:
            captcha_iframe = iframe
            if cd_frame_id:
                captcha_has_images = True
            break  # หยุดที่ iframe แรกที่พบ

    if captcha_iframe:
        # สลับไปยัง iframe ของ reCAPTCHA
        driver.switch_to.frame(captcha_iframe)

        time.sleep(1)

        if captcha_has_images:
            print("🔴 พบ cd_frame_id_! reCAPTCHA ต้องการแก้รูปภาพด้วยตัวเอง!")
        else:
            print("🟢 ไม่มี cd_frame_id_ reCAPTCHA ผ่านได้เลย!")

            try:
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, ":r1:"))
                )
                confirm_button.click()
                print("✅ คลิกปุ่ม 'ยืนยัน' สำเร็จ!")
            except TimeoutException:
                print("❌ ปุ่ม 'ยืนยัน' ไม่สามารถคลิกได้ภายใน 10 วินาที!")

    else:
        print("❌ ไม่พบ iframe ของ reCAPTCHA!")

except (KeyboardInterrupt, WebDriverException) as e:
    print("❌ หยุดการทำงาน:", str(e))

finally:
    input("🔴 กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()