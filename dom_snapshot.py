#!/usr/bin/env python3
"""
Captura el DOM renderizado (post-JS) de una URL local y lo vuelca en dom.json.
Uso:
    python dom_snapshot.py http://localhost:8000/login.html
"""

import sys, json, asyncio, pathlib
from playwright.async_api import async_playwright

async def snapshot(url: str, outfile: str = "dom.json"):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")

        dom = await page.evaluate(
            """() => {
                const walk = (n) => {
                    if (!n.tagName) return null;
                    return {
                      tag: n.tagName.toLowerCase(),
                      id: n.id || null,
                      name: n.name || null,
                      type: n.type || null,
                      text: (n.innerText || '').trim().slice(0, 50),
                      children: Array.from(n.children).map(walk),
                    };
                };
                return walk(document.body);
            }"""
        )

        pathlib.Path(outfile).write_text(json.dumps(dom, indent=2), encoding="utf-8")
        print(f"[OK] {outfile} creado")
        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python dom_snapshot.py <url>")
    asyncio.run(snapshot(sys.argv[1]))
