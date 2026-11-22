import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
load_dotenv()
MANTRA_URL = os.getenv("MANTRA_URL")
MANTRA_USERNAME = os.getenv("MANTRA_USERNAME")
MANTRA_PASSWORD = os.getenv("MANTRA_PASSWORD")
playwright_instance = None
browser = None
page = None
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


async def open_mantra_portal():

    global playwright_instance, browser, page

    captcha_images = []

    if not all([MANTRA_URL, MANTRA_USERNAME, MANTRA_PASSWORD]):
        raise ValueError("Mantra credentials or URL missing in .env")

    # Start browser
    playwright_instance = await async_playwright().start()

    browser = await playwright_instance.chromium.launch(
        headless=False
    )

    page = await browser.new_page()

    # Open portal
    await page.goto(
        MANTRA_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Mantra portal opened")
    print("Page title:", await page.title())
    # Fill username
    await page.get_by_role("textbox",name="UserName").fill(MANTRA_USERNAME)
    # Fill password
    await page.get_by_role("textbox",name="Password").fill(MANTRA_PASSWORD)
    # Check CAPTCHA image
    captcha_image = page.locator("#imgcaptcha")
    if await captcha_image.is_visible():
        screenshot_path = SCREENSHOT_DIR / "mantra_captcha.png"
        # Capture CAPTCHA image
        await captcha_image.screenshot(
            path=str(screenshot_path)
        )
        captcha_images.append(str(screenshot_path))
        print("CAPTCHA detected")
    else:
        print("CAPTCHA not found")

    return {
        "captcha_images": captcha_images
    }

            # print(captcha_image)
            # if await captcha_image.count() > 0:
            #     print("CAPTCHA image detected")
            #     await captcha_image.screenshot(
            #     path="screenshots/captcha.png")
            # else:
            #     print("CAPTCHA image not found")
            # await page.get_by_role("textbox", name="Captcha").click()
            # await page.wait_for_timeout(10000)
            # await page.get_by_role("button", name="Log in").click()
            # # Allow the portal to respond
            # await page.wait_for_timeout(4000)
            # # await page.get_by_role("link", name="Enrollment ").click()
            # # await page.locator("#div_LeftMenu").get_by_role("https://mwoc.jindalsteel.com/Master/EmployeeKiosk", name="Add Worker").click()
            # # print("wait 4sec")
            # # await page.goto(
            # #     'https://mwoc.jindalsteel.com/Master/EmployeeKiosk',
            # #     wait_until="domcontentloaded",
            # #     timeout=60000
            # #             )
            # await page.get_by_role("button", name=" Add").click()
            # await page.locator("#AadharCard").fill("388780287998")
            # await page.locator("#FirstName").press_sequentially("nigam",delay=500)
            # await page.locator("#MiddleName").press_sequentially("")
            # await page.locator("#LastName").press_sequentially("bisoyi",delay=500)
            # print("Current URL:", page.url)
            # print("Page title:", await page.title())

            # # Keep browser open for inspection
            # await page.pause()



# if __name__ == "__main__":
#     asyncio.run(open_mantra_portal())

# load_dotenv()

# MANTRA_URL = os.getenv("MANTRA_URL")
# MANTRA_USERNAME = os.getenv("MANTRA_USERNAME")
# MANTRA_PASSWORD = os.getenv("MANTRA_PASSWORD")

async def fill_captcha_text(captcha_text: str):

    global page

    if page is None:
        raise ValueError("Mantra browser page is not available")

    if not captcha_text:
        raise ValueError("CAPTCHA text is required")

    # Fill ONLY CAPTCHA textbox
    # Replace #txtcaptcha with the actual CAPTCHA input selector
    await page.locator("#txtcaptcha").fill(captcha_text)

    print("CAPTCHA entered successfully")


async def click_mantra_login():

    global page

    if page is None:
        raise ValueError("Mantra browser page is not available")

    # Replace with your actual Login button selector
    await page.wait_for_timeout(10000)
    await page.get_by_role("button", name="Log in").click()

    print("Login button clicked")