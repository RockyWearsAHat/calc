---
description: "Quick visual QA check — screenshot a specific page and visually inspect it for rendering issues."
mode: "agent"
tools: ["bash", "analyze_images", "view"]
---

# Quick Visual Check

Screenshot and visually inspect a specific page of the Calculus Mastery app.

## Steps

1. Ask the user which page to check (or use the page they mentioned)
2. Use Playwright to screenshot it:

```bash
cd /Users/alexwaldmann/Desktop/Calc
python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def snap(url, name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=f'qa-output/screenshots/{name}.png', full_page=True)
        # Check for KaTeX errors
        errors = await page.evaluate('''() => {
            return document.querySelectorAll(\".katex-error\").length
        }''')
        print(f'Screenshot saved. KaTeX errors: {errors}')
        await browser.close()

asyncio.run(snap('PAGE_URL', 'PAGE_NAME'))
"
```

3. Use `analyze_images` to visually inspect the screenshot
4. Report findings: math rendering quality, layout issues, content clarity
5. If issues found, identify the fix location and apply it
