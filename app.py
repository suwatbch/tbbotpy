from fastapi import FastAPI
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

app = FastAPI()

@app.get("/open-and-check")
async def open_and_check():
    url = "https://leave.swmaxnet.com/"  # URL ที่ต้องการเปิด
    webbrowser.open_new_tab(url)  # เปิดในแท็บใหม่ของเบราว์เซอร์ที่ใช้งานอยู่

    # รอให้แท็บใหม่เปิดก่อน (ปรับเวลาให้เหมาะสม)
    time.sleep(3)

    try:
        # เชื่อมต่อไปยัง Chrome ที่เปิดอยู่
        options = Options()
        options.debugger_address = "127.0.0.1:9222"  # ใช้ Remote Debugging ควบคุม Chrome ปัจจุบัน

        driver = webdriver.Chrome(service=Service(), options=options)

        # เปลี่ยนไปที่แท็บล่าสุด (อาจต้องปรับถ้ามีหลายแท็บ)
        driver.switch_to.window(driver.window_handles[-1])

        # โหลดหน้าเว็บ
        driver.get(url)
        time.sleep(3)

        # ตรวจสอบว่าเป็นเว็บที่ต้องการหรือไม่
        current_url = driver.current_url
        if "leave.swmaxnet.com" in current_url:
            driver.execute_script("alert('✅ พบเว็บเป้าหมายแล้ว!');")  # แสดง Alert
            time.sleep(2)
            return {"status": "success", "message": "✅ พบเว็บเป้าหมาย!"}
        else:
            return {"status": "error", "message": "❌ ไม่พบเว็บเป้าหมาย"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()  # ปิด Selenium

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
