from bs4 import BeautifulSoup

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
        row_count = len(rows)
        print(f"จำนวนแถวใน <tbody>: {row_count}")

        # พิมพ์ค่าของคอลัมน์ที่ 2 ในแต่ละแถว
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 1:  # ตรวจสอบว่ามีคอลัมน์ที่ 2 หรือไม่
                print(columns[1].get_text(strip=True))
            else:
                print("ไม่พบคอลัมน์ที่ 2 ในแถวนี้")
    else:
        print("ไม่พบ <tbody> ในตาราง")
else:
    print("ไม่พบตารางใน HTML")
