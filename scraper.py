import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re

def scrape_website(url, max_pages=5):
    visited = set()
    data = {
        "business_summary": "",
        "products_services": [],
        "scraped_date": datetime.now().strftime("%Y-%m-%d")
    }
    base_domain = urlparse(url).netloc
    pages_to_scrape = [url]

    def scrape_page(current_url):
        if len(visited) >= max_pages:
            return
        if current_url in visited:
            return
        if urlparse(current_url).netloc != base_domain:
            return
        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text content for business summary
            paragraphs = soup.find_all('p')
            page_text = ' '.join([p.get_text() for p in paragraphs])
            data["business_summary"] += page_text + " "

            # Extract products/services (common patterns)
            product_elements = soup.find_all(text=re.compile(r'Products|Services|Our Products|Our Services', re.I))
            for elem in product_elements:
                parent = elem.find_parent()
                if parent:
                    items = parent.find_next_sibling()
                    if items and items.name in ['ul', 'ol']:
                        for li in items.find_all('li'):
                            item_text = li.get_text(strip=True)
                            if item_text and item_text not in data["products_services"]:
                                data["products_services"].append(item_text)

            # Find and prioritize internal links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                if full_url not in visited and urlparse(full_url).netloc == base_domain:
                    if "product" in href.lower() or "service" in href.lower():
                        pages_to_scrape.insert(0, full_url)  # Prioritize product/service pages
                    else:
                        pages_to_scrape.append(full_url)

        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            print(f"Failed to scrape {current_url}: {e}")
        except Exception as e:
            print(f"An error occurred while scraping {current_url}: {e}")

    # Start scraping from the initial URL
    while pages_to_scrape and len(visited) < max_pages:
        next_page = pages_to_scrape.pop(0)
        scrape_page(next_page)

    # Summarize the business summary (optional - simple truncation here)
    data["business_summary"] = data["business_summary"].strip()[:1000]  # Limit to 1000 characters

    # Remove duplicates in products/services
    data["products_services"] = list(set(data["products_services"]))

    return data