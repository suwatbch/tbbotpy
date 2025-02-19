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
    # รอให้ตารางโหลดเสร็จ
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))
    # ดึงข้อมูลจากตาราง
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        print(f"Number of cells in row: {len(cells)}")  # พิมพ์จำนวนเซลล์ในแต่ละแถว
        # ดึงข้อมูลจากทุกเซลล์ในแถว
        row_data = [cell.text for cell in cells]
        if row_data:  # ตรวจสอบว่าแถวมีข้อมูล
            data.append(row_data)
    return data

try:
    # สลับไปที่ iframe ก่อน (ถ้ามี)
    try:
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframe)
    except:
        print("ไม่พบ iframe หรือไม่จำเป็นต้องสลับ")

    # ดึงข้อมูลตาราง
    table_data = get_table_data()

    # สลับกลับไปที่เนื้อหาหลัก
    driver.switch_to.default_content()

    # พิมพ์ข้อมูลออกมา
    for entry in table_data:
        print(entry)

    # รอให้ผู้ใช้ปิดโปรแกรมเอง
    input("กด Enter เพื่อปิดโปรแกรม...")

except WebDriverException as e:
    print(f"เกิดข้อผิดพลาด: {e}")

finally:
    # ปิด WebDriver
    driver.quit()