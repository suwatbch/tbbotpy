from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# ตั้งค่า WebDriver (เช่น ChromeDriver)
driver = webdriver.Chrome()

# ไปที่หน้าเว็บที่ต้องการ
driver.get('http://localhost:8080/')  # เปิด URL ที่ต้องการ

def check_status_and_handle_popup():
    try:
        # รอให้ตารางโหลดเสร็จ
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        # ดึงข้อมูลจากแถวที่สอง
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        if len(rows) > 1:
            second_row = rows[1]

            # ค้นหาปุ่มในแถวที่สองและคลิก
            button = second_row.find_element(By.XPATH, ".//button[div[text()='ตรวจสอบสถานะ']]")
            button.click()


    except WebDriverException as e:
        print(f"เกิดข้อผิดพลาด: {e}")

    finally:
        # ปิด WebDriver
        input()

check_status_and_handle_popup()