from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import platform
import subprocess
import asyncio
from urllib.parse import urlparse
from pyppeteer import connect

app = Flask(__name__)
CORS(app)

CHROME_DEBUG_URL = 'http://127.0.0.1:9222'

#---------UseChome--------------------------------------------------------

async def check_chrome_debug_mode():
    try:
        # ตรวจสอบว่า Chrome Debug Mode กำลังทำงานหรือไม่
        browser = await connect(browserURL=CHROME_DEBUG_URL)
        await browser.disconnect()
        return {
            "status": True,
            "message": "Chrome กำลังทำงานใน Debug Mode"
        }
    except Exception as e:
        print(f"Check chrome debug mode error: {str(e)}")
        return {
            "status": False,
            "message": "กรุณาเปิด Chrome ด้วย Debug Mode"
        }

@app.route('/check-chrome', methods=['GET'])
async def check_chrome():
    try:
        print('Checking Chrome debug mode status...')
        status = await check_chrome_debug_mode()
        return jsonify(status)
    except Exception as e:
        return jsonify({
            "status": False,
            "message": f"เกิดข้อผิดพลาดในการตรวจสอบ: {str(e)}"
        }), 500


def is_chrome_debug_running():
    try:
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                # ตรวจสอบว่ามี Chrome ที่รันในโหมด debug อยู่หรือไม่
                if (proc.info['cmdline'] and 
                    any('--remote-debugging-port=9222' in cmd for cmd in proc.info['cmdline'])):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False
    except Exception:
        return False

async def openChromeWithDebug(urls=[]):
    try:
        print(f"Starting Chrome with URLs: {urls}")  # Debug log
        
        # ตรวจสอบว่ามี Chrome ในโหมด debug รันอยู่หรือไม่
        if is_chrome_debug_running():
            print("Chrome debug mode is already running")
            # เชื่อมต่อกับ Chrome ที่เปิดอยู่
            browser = await connect(browserURL=CHROME_DEBUG_URL)
            print("Connected to existing Chrome")
        else:
            # สร้างคำสั่งตามระบบปฏิบัติการ
            system = platform.system()
            if system == "Windows":
                command = f"start chrome --remote-debugging-port=9222 {urls[0]}"
                shell = True
            elif system == "Darwin":  # macOS
                command = f"open -a 'Google Chrome' --args --remote-debugging-port=9222 {urls[0]}"
                shell = True
            else:  # Linux
                command = f"google-chrome --remote-debugging-port=9222 {urls[0]}"
                shell = False

            # รันคำสั่งเปิด Chrome
            subprocess.Popen(command, shell=shell)
            # รอให้ Chrome พร้อมใช้งาน
            await asyncio.sleep(2)
            
            print(f"Chrome started, connecting to {CHROME_DEBUG_URL}")
            browser = await connect(browserURL=CHROME_DEBUG_URL)
            print("Connected to new Chrome instance")

        # เปิด URL ที่เหลือในแท็บใหม่
        for url in urls:
            print(f"Opening new tab with URL: {url}")
            page = await browser.newPage()
            await page.goto(url, {'waitUntil': 'networkidle0'})

        # ตัด connection
        await browser.disconnect()

        return {
            "status": True,
            "message": f"เปิด Chrome และ URL ทั้งหมด {len(urls)} รายการสำเร็จ",
            "openedUrls": urls
        }
    except Exception as e:
        print(f"Failed to open Chrome: {str(e)}")
        return {
            "status": False,
            "message": "ไม่สามารถเปิด Chrome ได้",
            "error": str(e)
        }

async def background_open_chrome(urls):
    try:
        await openChromeWithDebug(urls)
    except Exception as e:
        print(f"Background task error: {str(e)}")

@app.route('/open-chrome', methods=['POST'])
async def open_chrome_debug():
    try:
        data = request.get_json()
        urls = data.get('urls', [])

        # ตรวจสอบรูปแบบข้อมูล
        if not urls or not isinstance(urls, list):
            return jsonify({
                "status": "error",
                "message": "กรุณาระบุ urls เป็น array ของ URL"
            }), 400

        # ตรวจสอบความถูกต้องของ URL
        valid_urls = []
        for url in urls:
            try:
                result = urlparse(url)
                if all([result.scheme, result.netloc]):
                    valid_urls.append(url)
            except:
                continue

        if not valid_urls:
            return jsonify({
                "status": "error",
                "message": "ไม่พบ URL ที่ถูกต้อง"
            }), 400

        # สร้าง task ให้ทำงานเบื้องหลัง
        asyncio.create_task(background_open_chrome(valid_urls))

        # ตอบกลับทันที
        return jsonify({
            "status": "success",
            "message": "กำลังเปิด Chrome ในเบื้องหลัง",
            "urls": valid_urls
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def closeAllChrome():
    try:
        chrome_processes = []
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if any(chrome_name in proc.info['name'].lower() for chrome_name in ['chrome', 'chromium']):
                    chrome_processes.append(proc)
                elif proc.info['cmdline'] and any('--remote-debugging-port' in cmd for cmd in proc.info['cmdline']):
                    chrome_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        for proc in chrome_processes:
            try:
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return True, len(chrome_processes) 
    except Exception:
        return False, 0 

@app.route('/close-chrome', methods=['GET'])
def close_chrome():
    success, count = closeAllChrome()
    if success:
        return {
            "status": "success",
            "message": f"Chrome has been closed successfully. Closed {count} processes"
        }, 200
    else:
        return {
            "status": "error",
            "message": "Failed to close Chrome processes"
        }, 500

#---------UseChome--------------------------------------------------------

if __name__ == '__main__':
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    app.debug = True 
    config = Config()
    config.bind = ["0.0.0.0:4000"]
    config.debug = True
    asyncio.run(serve(app, config))
