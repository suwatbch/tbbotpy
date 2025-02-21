import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

driver = webdriver.Chrome()
driver.get('https://th.turboroute.ai/#/login')

# ค้นหาช่องกรอก username และ password โดยใช้ By.NAME
username_field = driver.find_element(By.NAME, 'account')  # ใช้ชื่อฟิลด์จาก HTML
password_field = driver.find_element(By.NAME, 'password')  # ใช้ชื่อฟิลด์จาก HTML

# กรอกข้อมูลล็อกอิน
username_field.send_keys('0955294478')
password_field.send_keys('FleetSPT@2468')
password_field.send_keys(Keys.RETURN)

# รอให้การเปลี่ยนเส้นทางเสร็จสิ้น
WebDriverWait(driver, 10).until(EC.url_contains('/home'))
driver.get('https://th.turboroute.ai/#/grab-single/single-hall')

my_car = {'4W': 2, '4WJ': 0, '6W5.5': 1, '6w7.2': 0} # จำนวนรถที่จะรับงาน
route_direction = ['SO5-SKU', 'SO5-TLG-HKT', '5BKT-EA2'] # เส้นทางรถที่จะรับงาน

assigned_cars = {key: 0 for key in my_car}
assigned_routes = {key: [] for key in my_car}

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

        if len(cells) >= 4:
            car_type = cells[3].text
            route = cells[1].text

            # ตรวจสอบว่ารถมีใน my_car และเส้นทางอยู่ใน route_direction
            if car_type in my_car and route in route_direction:
                car_count = my_car[car_type]

                # ถ้ารถมากกว่า 0 ถึงจะเข้ารับงาน
                if car_count > 0:
                    # เงื่อนไขการเข้ารับงาน...
                    # ฟังชั่นการเข้ารับงาน...

                    # เพิ่มจำนวนรถที่รับงาน
                    assigned_cars[car_type] += 1

                    # เพิ่มเส้นทางที่รับงาน
                    assigned_routes[car_type].append(route)

                    # ลดจำนวนรถที่มีใน my_car
                    my_car[car_type] -= 1

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📅 สรุปผล: {current_time}")

    print("🚗 รถว่าง:")
    for car_type, count in my_car.items():
        if count > 0:
            print(f"   - {car_type} จำนวน {count} คัน")

    print("✅ รับงาน:")
    for car_type, routes in assigned_routes.items():
        if routes:
            print(f"   - {car_type} จำนวน {len(routes)} คัน 🛣️ เส้นทาง: {', '.join(routes)}")
    
    print("-----------------------------------------------")
    
    return all(count == 0 for count in my_car.values())

try:
    while True:
        if (get_table_data()):
            break

        driver.refresh()
        time.sleep(1)

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    driver.quit()