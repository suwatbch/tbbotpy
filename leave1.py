import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# ตั้งค่า WebDriver (เช่น ChromeDriver)
driver = webdriver.Chrome()

# ไปที่หน้าล็อกอิน
driver.get('https://leave.swmaxnet.com/')

# ค้นหาช่องกรอก username และ password โดยใช้ By.NAME
username_field = driver.find_element(By.NAME, 'login_username')  # ใช้ชื่อฟิลด์จาก HTML
password_field = driver.find_element(By.NAME, 'login_password')  # ใช้ชื่อฟิลด์จาก HTML

# กรอกข้อมูลล็อกอิน
username_field.send_keys('adminptn')
password_field.send_keys('1234')

# กด Enter เพื่อล็อกอิน
password_field.send_keys(Keys.RETURN)

# รอให้การแจ้งเตือนปรากฏ
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print("กดตกลงในแจ้งเตือนแล้ว")
except:
    print("ไม่มีการแจ้งเตือน")

# ไปที่ URL ใหม่
driver.get('https://leave.swmaxnet.com/#module=workday')

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
    car = 3
    for _ in range(car, 0, -1):
        # ดึงข้อมูลตาราง
        print_table_data()

        # รอ 1 วินาที
        time.sleep(1)

        # รีเฟรชหน้า
        driver.refresh()

    print("")
    input()  # รอให้ผู้ใช้กดปุ่มใด ๆ เพื่อหยุดการทำงาน

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    # ปิด WebDriver
    driver.quit()