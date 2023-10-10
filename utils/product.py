from typing import Any, List
from bs4 import BeautifulSoup
from pyppeteer import launch


async def get_cards_index(product: str) -> List[str]:
    url = f"https://ange-unite.com/cardlist/{product}.html"
    browser = await launch(args=["--single-process"])
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector("#app")
    content = await page.content()
    await browser.close()
    soup = BeautifulSoup(content, "html.parser")
    elements = soup.select("h3.p-headline-items span.p-subtext span.p-text-inner")

    res = []
    for element in elements:
        res.append(element.text)
    return res
