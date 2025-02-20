from bs4 import BeautifulSoup

# อ่านไฟล์ vue.html
with open('vue.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# ใช้ BeautifulSoup เพื่อแยกวิเคราะห์ HTML
soup = BeautifulSoup(html_content, 'html.parser')

# ค้นหาตารางแรก
table = soup.find('table')

# นับจำนวนแถวใน <tbody> ของตารางแรก
if table:
    tbody = table.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')
        row_count = len(rows)
        print(f"จำนวนแถวใน <tbody>: {row_count}")
    else:
        print("ไม่พบ <tbody> ในตาราง")
else:
    print("ไม่พบตารางใน HTML")
