"""
Get publishers script.
"""
import asyncio
from string import Template

from src.enums.scraper import ParseMode
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.utils import parse_config
from src.structures.scraper import ParserFieldConfig

PUBLISHERS_URL_TEMPLATE = Template('https://nashformat.ua/publishers/letter-${page_number}')
PUBLISHERS_SCRAPE_CONFIG = {
    'names': ParserFieldConfig(selector='.publishers_list li a', regex=r'.*?(?=\n)', mode=ParseMode.ALL),
}

async def main():
    async with PlaywrightScraperEngine() as engine:
        all_publishers = set()

        page_number = 1
        while True:
            url = PUBLISHERS_URL_TEMPLATE.substitute(page_number=page_number)
            async with engine.get_page() as page:
                await page.goto(url)
                result = await parse_config(config=PUBLISHERS_SCRAPE_CONFIG, target=page)

            print(result)

            if not result:
                break

            all_publishers.update(result['names'])

            page_number += 1

        page_number = 1
        while True:
            url = PUBLISHERS_URL_TEMPLATE.substitute(page_number=page_number)
            async with engine.get_page(cookies=[{'name': 'alphabet', 'value': 'en', 'url': url}]) as page:
                await page.goto(url)
                result = await parse_config(config=PUBLISHERS_SCRAPE_CONFIG, target=page)

            print(result)

            if not result:
                break

            all_publishers.update(result['names'])

            page_number += 1

    publisher_mapping = {publisher: [publisher] for publisher in all_publishers if publisher}
    print(publisher_mapping)


if __name__ == '__main__':
    asyncio.run(main())
