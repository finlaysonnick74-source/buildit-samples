import sys,asyncio
from playwright.async_api import async_playwright
SL="saltwater-cafe swell-academy peninsula-sparks ground-studio sudsy-paws barrenjoey-house".split()
BASE=sys.argv[1]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for s in SL:
      for w,h,tag in[(1280,800,"desktop"),(390,844,"mobile")]:
        pg=await b.new_page(viewport={"width":w,"height":h});errs=[]
        pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None);pg.on("pageerror",lambda e:errs.append(str(e)))
        bad=[];pg.on("response",lambda r:bad.append(r.url) if r.status>=400 else None)
        await pg.goto(f"{BASE}/{s}/",wait_until="networkidle");await pg.wait_for_timeout(1500)
        ov=await pg.evaluate("document.documentElement.scrollWidth-innerWidth")
        links=await pg.evaluate("[...document.querySelectorAll('a[href^=\"#\"]')].filter(a=>a.getAttribute('href').length>1&&!document.querySelector(a.getAttribute('href'))).length")
        await pg.screenshot(path=f"shots/{s}-{tag}-{w}.png")
        print(s,tag,"overflow",ov,"errs",errs,"bad",bad,"brokenanchors",links)
        await pg.close()
    await b.close()
asyncio.run(main())
