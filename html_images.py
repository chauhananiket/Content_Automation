import asyncio
from pathlib import Path
import sys
from playwright.async_api import async_playwright

# -------- CLI INPUT --------
if len(sys.argv) < 3:
    print("Usage: python script.py input.html output_folder [total_slides]")
    sys.exit(1)

INPUT_HTML = Path(sys.argv[1])
OUTPUT_DIR = Path(sys.argv[2])
TOTAL_SLIDES = int(sys.argv[3]) if len(sys.argv) > 3 else 7

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------- CONFIG --------
VIEW_W = 420
VIEW_H = 525
SCALE = 1080 / 420  # Instagram quality scaling


async def export_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )

        html_content = INPUT_HTML.read_text(encoding="utf-8")

        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(3000)  # wait for fonts/assets

        # -------- CLEAN UI --------
        await page.evaluate("""
        () => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
                .forEach(el => el.style.display='none');

            const frame = document.querySelector('.ig-frame');
            if (frame) {
                frame.style.cssText = 'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
            }

            const viewport = document.querySelector('.carousel-viewport');
            if (viewport) {
                viewport.style.cssText = 'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';
            }

            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;';
        }
        """)

        await page.wait_for_timeout(500)

        # -------- LOOP THROUGH SLIDES --------
        for i in range(TOTAL_SLIDES):
            await page.evaluate(f"""
            () => {{
                const track = document.querySelector('.carousel-track');
                if (track) {{
                    track.style.transition = 'none';
                    track.style.transform = 'translateX(' + (-{VIEW_W} * {i}) + 'px)';
                }}
            }}
            """)

            await page.wait_for_timeout(400)

            output_file = OUTPUT_DIR / f"slide_{i+1}.png"

            await page.screenshot(
                path=str(output_file),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H}
            )

            print(f"✅ Exported slide {i+1}/{TOTAL_SLIDES}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(export_slides())