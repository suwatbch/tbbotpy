import time
from bs4 import BeautifulSoup
from datetime import datetime

loops = 3

# จำนวนรถที่จะรับงาน
my_car = {'4W': 2, '4WJ': 0, '6W5.5': 1, '6w7.2': 0}
# เส้นทางรถที่จะรับงาน
route_direction = ['SO5-SKU', 'SO5-TLG-HKT', '5BKT-EA2']


assigned_cars = {key: 0 for key in my_car}
assigned_routes = {key: [] for key in my_car}

def process_rows(rows):
    for row in rows:
        cells = row.find_all('td')

        if len(cells) >= 4:
            car_type = cells[3].get_text(strip=True)
            route = cells[1].get_text(strip=True)

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


        else:
            print("ครั้งนี้มีคอลัมน์ไม่เพียงพอ")
            return True  # หยุดการทำงาน
    return False

def all_cars_assigned():
    return all(count == 0 for count in my_car.values())

# อ่านไฟล์ tbr.html
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# ใช้ BeautifulSoup เพื่อแยกวิเคราะห์ HTML
soup = BeautifulSoup(html_content, 'html.parser')

# ค้นหาตารางแรก
table = soup.find('table', class_='el-table__body')

# นับจำนวนแถวใน <tbody> ของตารางแรก
if table:
    tbody = table.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')

        for _ in range(loops):
            try:
                stop_program = process_rows(rows)
                
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")
                break

            if not stop_program:
                # สรุปผลหลังจากวนครบทุกแถว
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

                if stop_program or all_cars_assigned():
                    break

                # รอ 1 วินาที
                time.sleep(1)
        
    else:
        print("ไม่พบ <tbody> ในตาราง")
else:
    print("ไม่พบตารางใน HTML")