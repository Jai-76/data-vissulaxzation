import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1500,"height":880}, device_scale_factor=1.5)
        errs=[]
        pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
        pg.on("console", lambda m: errs.append("CONSOLE "+m.text) if m.type=="error" else None)
        await pg.goto("file:///home/user/world-dashboard.html")
        await pg.wait_for_timeout(1200)
        info = await pg.evaluate("""() => ({
            years: window.__DATA__.meta.years,
            inds: Object.fromEntries(Object.entries(window.__DATA__.meta.indicators).map(([k,v])=>[k,v.year_max])),
            range: document.querySelector('#year-range').textContent,
            sliderMax: document.querySelector('#slider').max,
            projOn: document.querySelector('#proj').checked })""")
        print("META", info)
        await pg.click("#play")  # pause
        for y in [2024, 2025, 2026]:
            await pg.evaluate(f"document.querySelector('#slider').value={y}; document.querySelector('#slider').dispatchEvent(new Event('input'))")
            await pg.wait_for_timeout(400)
            vals = await pg.evaluate("""() => ({y: document.querySelector('#year-big').textContent,
                pop: document.querySelector('#st-pop').textContent,
                life: document.querySelector('#st-life').textContent,
                co2: document.querySelector('#st-co2').textContent})""")
            print(y, vals)
            await pg.screenshot(path=f"shots/y{y}.png")
        # hover a bubble at 2026 to check the ≈ marker
        box = await pg.locator("#chart").bounding_box()
        await pg.mouse.move(box["x"]+box["width"]*0.55, box["y"]+box["height"]*0.35)
        await pg.wait_for_timeout(400)
        tip = await pg.evaluate("document.querySelector('#tip').innerText")
        print("TIP:", tip.replace("\n"," | ")[:220])
        await pg.screenshot(path="shots/hover2026.png")
        # projection off
        await pg.click("#proj")
        await pg.wait_for_timeout(500)
        off = await pg.evaluate("""() => ({range: document.querySelector('#year-range').textContent,
             sliderMax: document.querySelector('#slider').max, year: document.querySelector('#year-big').textContent})""")
        print("PROJ OFF", off)
        # GDP vs population with projection on -> 2025 is observed
        await pg.click("#proj")
        await pg.select_option("#sel-y", "pop")
        await pg.wait_for_timeout(400)
        print("gdp/pop range", await pg.evaluate("document.querySelector('#year-range').textContent"))
        print("ERRORS", errs[:6])
        await b.close()
asyncio.run(main())
