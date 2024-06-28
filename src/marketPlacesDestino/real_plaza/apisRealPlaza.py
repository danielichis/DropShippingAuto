import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://inretail.mysellercenter.com/#/dashboard')
        await page.wait_for_load_state("networkidle")

        # Crear un contexto de solicitud de API
        context = await p.request.new_context()

        # Hacer una petición GET
        urlEndpoint = "https://inretail.mysellercenter.com/sellercenter/api/v1/categories/?sortOrder=asc&sortBy=name.keyword&from=0&size=10&text=laptops"
        response = await context.get(urlEndpoint)

        # Imprimir el cuerpo de la respuesta
        print(await response.text())

        await browser.close()

asyncio.run(main())