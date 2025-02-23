from fastapi import FastAPI
from selenium import webdriver
import time

app = FastAPI()

@app.get("/check-website")
async def check_website():
    # ตั้งค่า Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # เปิดเต็มจอ
    # options.add_argument("--headless")  # ถ้าต้องการให้ทำงานเบื้องหลัง

    driver = webdriver.Chrome(options=options)

    try:
        # เปิด URL เป้าหมาย
        driver.get("https://leave.swmaxnet.com/")
        time.sleep(3)  # รอให้หน้าเว็บโหลด

        # ตรวจสอบ URL
        current_url = driver.current_url
        if "leave.swmaxnet.com" in current_url:
            driver.execute_script("alert('พบเว็บเป้าหมายแล้ว!');")  # แสดง Alert
            time.sleep(2)  # รอให้เห็น Alert
            return {"status": "success", "message": "✅ พบเว็บเป้าหมาย!"}
        else:
            return {"status": "error", "message": "❌ ไม่พบเว็บเป้าหมาย"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()  # ปิดเบราว์เซอร์

