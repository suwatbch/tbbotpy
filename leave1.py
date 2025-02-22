from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)

# ตรวจสอบว่าเว็บที่ต้องการเปิดอยู่หรือไม่
current_url = driver.current_url
print(f"Current URL: {current_url}")

# ตรวจสอบว่าเปิดอยู่ที่ https://leave.swmaxnet.com/
if "https://leave.swmaxnet.com/" in current_url:
    # เปลี่ยนไปยังหน้า https://leave.swmaxnet.com/#module=workday
    driver.get("https://leave.swmaxnet.com/#module=workday")
    print("เปลี่ยนไปยังหน้า workday")
else:
    print("ไม่ได้เปิดอยู่ที่หน้า leave.swmaxnet.com")