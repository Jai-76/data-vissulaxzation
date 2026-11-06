import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs=[]
        pg = await b.new_page(viewport={"width":1440,"height":860}, device_scale_factor=2)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        await pg.goto("file:///home/user/world-dashboard.html")
        await pg.wait_for_timeout(1200)
        await pg.click("#play")
        await pg.evaluate("document.querySelector('#slider').value=2026; document.querySelector('#slider').dispatchEvent(new Event('input'))")
        await pg.wait_for_timeout(500)
        await pg.mouse.move(10,10)
        await pg.screenshot(path="shots/final-2026.png")
        await pg.click("#about")
        await pg.wait_for_timeout(400)
        await pg.evaluate("document.querySelector('.modal').scrollTop = 520")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path="shots/final-modal.png")
        await pg.click("#close-modal")
        pg2 = await b.new_page(viewport={"width":430,"height":900}, device_scale_factor=2)
        await pg2.goto("file:///home/user/world-dashboard.html")
        await pg2.wait_for_timeout(1800)
        await pg2.screenshot(path="shots/final-mobile.png")
        print("ERRORS", errs[:5])
        await b.close()
asyncio.run(main())
