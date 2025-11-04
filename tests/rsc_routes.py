from playwright.sync_api import sync_playwright
import pandas as pd
import time

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

        # Try clicking visible internal links
        links = page.locator("a[href^='/']").all()
        for link in links[:5]:
            href = link.get_attribute("href")
            if href:
                print(f"➡️ Navigating to {href}")
                try:
                    link.click()
                    page.wait_for_timeout(4000)
                except:
                    pass

        time.sleep(5)
        browser.close()

        # Save results
        if rsc_urls:
            df = pd.DataFrame({
                "HTTP Method": ["GET"] * len(rsc_urls),
                "URL": list(rsc_urls)
            })
            filename = f"{base_url.split('//')[1].split('/')[0]}_rsc_routes.xlsx"
            df.to_excel(filename, index=False)
            print(f"\n✅ Saved {len(rsc_urls)} RSC routes → {filename}")
        else:
            print("❌ No .rsc URLs found.")
        return list(rsc_urls)

# Example
find_rsc_routes("https://muvro-frontend.vercel.app/")
