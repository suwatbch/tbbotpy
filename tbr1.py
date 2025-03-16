import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

try:
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=chrome_options)
    current_url = driver.current_url
    
    if "https://th.turboroute.ai/#/home" in current_url:
        # เปลี่ยนไปยังหน้า grab-single/single-hall
        driver.get("https://th.turboroute.ai/#/grab-single/single-hall")
        WebDriverWait(driver, 10).until(EC.url_contains('/grab-single/single-hall'))

        # my_car = {'4W': 4}
        # route_direction = ['KRM02-BAGH','NDD-EA1','NDD-PDT','POR-CT1']

        # my_car = {'4W': 0, '4WJ': 1, '6W5.5': 0, '6w7.2': 0, '6w8.8': 0}
        # route_direction = ['SO5-SKU','SO5-KOK','SO5-TLG-HKT','5BKT-EA2','CT1-EA2']

        my_car = {'4W': 1}
        route_direction = ['TSH-CT1']

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
                            try:
                                row_button = row.find_element(By.XPATH, ".//span[contains(text(), 'แข่งขันรับงาน')]")
                                row_button.click()

                                WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, "//span[text()='ยืนยันแข่งขันรับงาน']"))
                                )
                                time.sleep(1)
                                WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='แข่งขันรับงาน']]"))
                                )

                                # คลิกปุ่ม "แข่งขันรับงาน" ในป๊อปอัพ
                                # popup_button = driver.find_element(By.XPATH, "//button[span[text()='แข่งขันรับงาน']]")
                                # popup_button.click()
                                print(f"รับงานสำเร็จ สำหรับ {car_type} ในเส้นทาง {route}")

                            except WebDriverException as e:
                                print(f"ไม่สามารถ 'แข่งขันรับงาน' ได้ มี ERROR: {e}")

                            # เพิ่มจำนวนรถที่รับงาน
                            assigned_cars[car_type] += 1

                            # เพิ่มเส้นทางที่รับงาน
                            assigned_routes[car_type].append(route)

                            # ลดจำนวนรถที่มีใน my_car
                            my_car[car_type] -= 1

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
                # driver.execute_script(f"alert(`{summary}`);")
                break

            time.sleep(0.5)
            driver.refresh()
            time.sleep(0.5)

except (KeyboardInterrupt, WebDriverException) as e:
    print("หยุดการทำงาน")

finally:
    input("กด Enter เพื่อปิดเบราว์เซอร์...")
    driver.quit()