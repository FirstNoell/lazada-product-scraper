import csv
from playwright.sync_api import sync_playwright

def scrape_lazada(search_query="storage box"):
    url = f"https://www.lazada.com.ph/catalog/?q={search_query}"

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        page.wait_for_timeout(5000)

        products = page.query_selector_all('div[data-qa-locator="product-item"]')

        for product in products[:10]:  # limit to 10 (portfolio demo)
            try:
                title = product.query_selector("a").inner_text()
                price = product.query_selector(".price--NVB62").inner_text()

                img_el = product.query_selector("img")
                image = img_el.get_attribute("src") or img_el.get_attribute("data-src")

                results.append({
                    "title": title,
                    "price": price,
                    "image": image
                })

            except Exception as e:
                continue

        browser.close()

    return results


def save_to_csv(data, filename="sample_output.csv"):
    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    data = scrape_lazada()
    save_to_csv(data)
    print("✅ Data saved to sample_output.csv")
