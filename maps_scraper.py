import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_google_maps():
    async with async_playwright() as p:
        # Headless True hona chahiye GitHub Actions ke liye
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Apni search query yahan likhein
        search_query = "Embroidery shops in California"
        await page.goto(f"https://www.google.com/maps/search/{search_query}")
        await asyncio.sleep(5)

        # Scrolling logic
        for _ in range(3): 
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)

        results = []
        shop_elements = await page.query_selector_all('a.hfpxzc')

        # Pehli 10 shops ka data (aap limit badha sakte hain)
        for i in range(min(10, len(shop_elements))):
            try:
                current_shops = await page.query_selector_all('a.hfpxzc')
                await current_shops[i].click()
                await asyncio.sleep(4)

                name = await page.inner_text('h1.DUwDvf') if await page.query_selector('h1.DUwDvf') else "N/A"
                
                phone = "N/A"
                phone_elem = await page.query_selector('button[data-item-id^="phone:tel:"]')
                if phone_elem: phone = await phone_elem.inner_text()

                address = "N/A"
                address_elem = await page.query_selector('button[data-item-id="address"]')
                if address_elem: address = await address_elem.inner_text()

                results.append({"Name": name, "Phone": phone, "Address": address})
                print(f"Scraped: {name}")
            except:
                continue

        df = pd.DataFrame(results)
        df.to_csv("google_maps_leads.csv", index=False)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_google_maps())
