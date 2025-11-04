import os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from openpyxl import Workbook

def extract_api_routes(base_url):
    api_routes = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # True Or False
        context = browser.new_context()
        page = context.new_page()

        def log_request(request):
            url = request.url
            method = request.method
            if any(keyword in url for keyword in ["/api/", "/v1/", "/v2/", "/rest/"]):
                api_routes.add((method, url))  # store method + URL as tuple

        page.on("request", log_request)

        print(f"Opening {base_url} ...")
        try:
            page.goto(base_url, wait_until="networkidle", timeout=120000)
        except:
            print("⚠️ Network idle never reached, retrying with DOM load...")
            try:
                page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print(f"❌ Still failed: {e}")

        context.close()
        browser.close()

    print(f"\n💾 Found {len(api_routes)} API routes:")
    for method, route in api_routes:
        print(f"[{method}] {route}")

    return api_routes


if __name__ == "__main__":
    base_url = "https://www.tech2globe.com/"  # 🔁 replace with your target site
    routes = extract_api_routes(base_url)

    # 🧠 Extract site name from URL
    parsed = urlparse(base_url)
    site_name = parsed.netloc.replace("www.", "").split("/")[0]
    site_name = site_name.split(".")[0]

    # 📂 Create 'reports' folder if not exists
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # 📄 Define Excel file path inside reports folder
    excel_filename = os.path.join(reports_dir, f"{site_name}_api_routes.xlsx")

    if routes:
        # ✅ Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "API Routes"

        # ✅ Write header row
        ws.append(["HTTP Method", "URL"])

        # ✅ Write each API route
        for method, url in sorted(routes):
            ws.append([method, url])

        # ✅ Save Excel file
        wb.save(excel_filename)

        print(f"\n📊 Saved {len(routes)} API routes to {excel_filename}")
    else:
        print("❌ No API routes found.")
