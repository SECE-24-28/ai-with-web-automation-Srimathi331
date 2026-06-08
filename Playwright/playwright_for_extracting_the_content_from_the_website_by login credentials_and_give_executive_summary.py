from playwright.sync_api import sync_playwright
from google import genai

# Gemini API Key
API_KEY = "YOUR-API-KEY"

# Create Gemini Client
client = genai.Client(api_key=API_KEY)

# SauceDemo Credentials
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Login
    page.goto("https://www.saucedemo.com")

    page.fill("#user-name", USERNAME)
    page.fill("#password", PASSWORD)

    page.click("#login-button")

    page.wait_for_load_state("networkidle")

    # Scrape Products
    products = page.locator(".inventory_item_name").all_inner_texts()

    print("\nProducts Found:\n")
    for product in products:
        print("-", product)

    # Prepare text for Gemini
    product_text = "\n".join(products)

    prompt = f"""
    Analyze these products:

    {product_text}

    Create a report with:

    1. Executive Summary
    2. Product Categories
    3. Key Insights
    4. Recommendations
    """

    # Gemini Call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n===== GEMINI REPORT =====\n")
    print(response.text)

    # Save Report
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("\nReport saved as report.txt")

    browser.close()