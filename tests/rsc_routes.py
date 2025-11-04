from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from datetime import datetime


def find_rsc_routes(base_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        rsc_urls = set()

        def log_request(request):
            url = request.url
            if ".rsc" in url:
                rsc_urls.add(url)
                print("🎯", url)

        page.on("request", log_request)
        print(f"🌐 Opening {base_url} ...")
        page.goto(base_url, wait_until="load", timeout=60000)

        # Scroll slowly to trigger lazy loads
        for i in range(3):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(3000)

        # Try clicking visible internal links (limited)
        links = page.locator("a[href^='/']").all()
        for link in links[:5]:
            href = link.get_attribute("href")
            if href:
                print(f"➡️ Navigating to {href}")
                try:
                    link.click()
                    page.wait_for_timeout(4000)
                except Exception:
                    pass

        time.sleep(5)
        browser.close()

        # Save results
        if rsc_urls:
            # 🧠 Prepare data
            df = pd.DataFrame({
                "HTTP Method": ["GET"] * len(rsc_urls),
                "URL": sorted(rsc_urls)
            })

            # 📂 Ensure reports folder exists
            os.makedirs("reports", exist_ok=True)

            # 🧾 Create clean filename with date
            domain = base_url.split("//")[1].split("/")[0].replace("www.", "")
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{domain}_rsc_routes_{date_str}.xlsx"
            filepath = os.path.join("reports", filename)

            # 💾 Save Excel file
            df.to_excel(filepath, index=False)
            print(f"\n✅ Saved {len(rsc_urls)} RSC routes → {filepath}")
        else:
            print("❌ No .rsc URLs found.")

        return list(rsc_urls)


# 🧪 Example
if __name__ == "__main__":
    find_rsc_routes("https://muvro-frontend.vercel.app/")
