# 🕵️‍♂️ Playwright Website Route Extractor Suite

A collection of Python automation scripts built with **Playwright** to extract different types of website routes, log API activity, and export data to **Excel reports**.

Each script automatically scans websites, captures routes or API calls, and saves results inside the `reports/` folder for easy access and documentation.

---

## 📂 Features Overview

| Script | Purpose | Output |
|:-------|:---------|:--------|
| **api_route_extractor.py** | Captures network requests like `/api/`, `/v1/`, `/v2/`, `/rest/` to find all backend API endpoints | Excel file with `HTTP Method` and `URL` columns |
| **routes.py** | Crawls all internal links (`<a>` tags) from a given base URL to map front-end routes | Excel file with columns `S.No`, `Route`, `Full URL`, `HTTP Method` |
| **rsc_routes.py** | Detects `.rsc` (React Server Components) requests in modern frameworks like Next.js 13+ | Excel file listing all `.rsc` URLs found |

---

## 🧠 How It Works

Each script:
1. Uses **Playwright** to open the given website in a headless Chromium browser.
2. Logs specific requests or routes while navigating and scrolling.
3. Optionally clicks on internal links to trigger lazy-loaded content.
4. Saves extracted data into a formatted Excel report.

---

## 🪜 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
