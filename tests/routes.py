from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import urllib.parse
import openpyxl
from openpyxl.styles import Font, Alignment
from datetime import datetime

def extract_routes_from_site(base_url: str):
    routes = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"🌐 Opening base URL: {base_url}")
        try:
            page.goto(base_url, wait_until="networkidle", timeout=120000)
            print("✅ Page loaded successfully")
        except PlaywrightTimeoutError:
            print(f"⚠️ Timeout while opening {base_url} — trying partial load mode...")
            try:
                page.goto(base_url, wait_until="domcontentloaded", timeout=180000)
            except Exception as e:
                print(f"❌ Still failed to open: {e}")
                browser.close()
                return []
        except Exception as e:
            print(f"❌ Failed to open {base_url}: {e}")
            browser.close()
            return []

        # Handle optional “Continue” button
        try:
            page.get_by_role("button", name="Continue").click(timeout=3000)
            print("Clicked 'Continue' button")
            page.wait_for_timeout(1000)
        except Exception:
            print("No 'Continue' button found or already bypassed")

        # Wait for final page load
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except PlaywrightTimeoutError:
            print("⚠️ 'networkidle' never reached, continuing anyway...")
            page.wait_for_load_state("load", timeout=5000)

        # Scroll to ensure lazy content is loaded
        for _ in range(3):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight / 3)")
            page.wait_for_timeout(1000)

        # Collect all <a> tags
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
        parsed_base = urllib.parse.urlparse(base_url)

        for link in links:
            parsed_link = urllib.parse.urlparse(link)
            if parsed_link.netloc == parsed_base.netloc:  # internal links only
                routes.add(parsed_link.path)

        context.close()
        browser.close()

    return sorted(routes)


def save_routes_to_excel(routes, base_url):
    # Extract domain for filename
    domain = urllib.parse.urlparse(base_url).netloc.replace("www.", "")
    filename = f"{domain}_routes.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Routes"

    # Headers
    headers = ["S.No", "Route", "Full URL", "HTTP Method"]
    ws.append(headers)

    # Style headers
    for cell in ws[1]:
        cell.font = Font(bold=True, color="1F4E78")
        cell.alignment = Alignment(horizontal="center")

    # Data rows
    for i, route in enumerate(routes, start=1):
        ws.append([i, route, urllib.parse.urljoin(base_url, route), "GET"])

    # Auto-fit column widths
    for col in ws.columns:
        max_length = max(len(str(cell.value)) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    # Save Excel
    wb.save(filename)
    print(f"\n💾 Saved {len(routes)} routes to '{filename}'")


if __name__ == "__main__":
    BASE_URL = "https://muvro-frontend.vercel.app/" # Replace with your target URL
    routes = extract_routes_from_site(BASE_URL)

    if routes:
        print("\n✅ Extracted Routes:")
        for r in routes:
            print(r)
        save_routes_to_excel(routes, BASE_URL)
    else:
        print("⚠️ No routes extracted. Check the base URL or try again with headless=False.")
