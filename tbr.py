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
driver.get('https://th.turboroute.ai/#/login')

# ค้นหาช่องกรอก username และ password โดยใช้ By.NAME
username_field = driver.find_element(By.NAME, 'account')  # ใช้ชื่อฟิลด์จาก HTML
password_field = driver.find_element(By.NAME, 'password')  # ใช้ชื่อฟิลด์จาก HTML

# กรอกข้อมูลล็อกอิน
username_field.send_keys('0955294478')
password_field.send_keys('FleetSPT@2468')

# กด Enter เพื่อล็อกอิน
password_field.send_keys(Keys.RETURN)

# รอให้การเปลี่ยนเส้นทางเสร็จสิ้น
WebDriverWait(driver, 10).until(EC.url_contains('/home'))

# ไปที่ URL ใหม่
driver.get('https://th.turboroute.ai/#/grab-single/single-hall')

def get_table_data():
    # รอให้ตารางโหลดเสร็จและมีแถวอย่างน้อยหนึ่งแถว
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.el-table__body tbody tr'))
    )
    # ดึงข้อมูลจากตารางแรกที่พบ
    table = driver.find_element(By.CSS_SELECTOR, 'table.el-table__body')
    
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            print(cell.text, end=' | ')
        print("")

try:
    car = 3
    for _ in range(car, 0, -1):
        # ดึงข้อมูลตาราง
        get_table_data()

        # รอ 1 วินาที
        time.sleep(1)

        # รีเฟรชหน้า
        driver.refresh()

    print("")
    input() 

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    # ปิด WebDriver
    driver.quit()