import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

# ตั้งค่า Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # รันในโหมด headless
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # เปลี่ยน user-agent

# เริ่มต้น driver พร้อม options
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://th.turboroute.ai/#/login')

    # เพิ่มการหน่วงเวลาเพื่อเลียนแบบพฤติกรรมมนุษย์
    time.sleep(2)

    # ค้นหาและกรอกข้อมูลในช่อง username และ password
    username_field = driver.find_element(By.NAME, 'account')
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys('0955294478')
    password_field.send_keys('FleetSPT@2468')

    # เพิ่มการหน่วงเวลาก่อนส่งข้อมูล
    time.sleep(1)

    # ส่งฟอร์ม
    username_field.send_keys(Keys.RETURN)

    # รอให้หน้าใหม่โหลด
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
                        # คลิกปุ่ม "grab an order"
                        try:
                            row_button = row.find_element(By.XPATH, ".//span[contains(text(), 'grab an order')]")
                            row_button.click()
                            print(f"คลิกปุ่ม 'grab an order' สำหรับ {car_type} ในเส้นทาง {route}")

                        except WebDriverException as e:
                            print(f"ไม่สามารถคลิกปุ่ม 'grab an order' ได้: {e}")

                        # เพิ่มจำนวนรถที่รับงาน
                        assigned_cars[car_type] += 1

                        # เพิ่มเส้นทางที่รับงาน
                        assigned_routes[car_type].append(route)

                        # ลดจำนวนรถที่มีใน my_car
                        my_car[car_type] -= 1

                        return True

        # เพิ่มสรุปผลการรับงานรายรอบ
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n📅 สรุปผลรายรอบ: {current_time}")
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

    while True:
        if get_table_data():
            summary = "\n📅 ผลสรุปสุดท้าย:\n"
            summary += "✅ รับงาน:\n"
            for car_type, routes in assigned_routes.items():
                if routes:
                    summary += f"   - {car_type} จำนวน {len(routes)} คัน 🛣️ เส้นทาง: {', '.join(routes)}\n"
            
            print(summary)
            # แสดงผลสรุปสุดท้ายใน alert
            # driver.execute_script(f"alert(`{summary}`);")
            break

        driver.refresh()
        time.sleep(1)

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    input("กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()