import asyncio
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

MANTRA_URL = os.getenv("MANTRA_URL")
MANTRA_USERNAME = os.getenv("MANTRA_USERNAME")
MANTRA_PASSWORD = os.getenv("MANTRA_PASSWORD")


async def open_mantra_portal():

    if not all([MANTRA_URL, MANTRA_USERNAME, MANTRA_PASSWORD]):
        raise ValueError("Mantra credentials or URL missing in .env")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        try:
            # Open portal
            await page.goto(
                MANTRA_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("Mantra portal opened")
            print("Page title:", await page.title())

            # Identify login fields
            username_field = page.locator(
                'input[type="email"], input[type="text"]'
            ).first

            password_field = page.locator(
                'input[type="password"]'
            ).first
           
            # Check login fields
            if await username_field.count() == 0:
                print("Username field not found")
                await page.pause()
                return

            if await password_field.count() == 0:
                print("Password field not found")
                await page.pause()
                return

            # Fill login details
            await username_field.fill(MANTRA_USERNAME)
            await password_field.fill(MANTRA_PASSWORD)

            print("Login details entered")

            #check captcha filed
            captcha_image = page.locator("#imgcaptcha")
            if await captcha_image.count() > 0:
                    print("CAPTCHA image detected")
                    await captcha_image.screenshot(
                    path="uploads/captcha.png"
                    )
            else:
                    print("CAPTCHA image not found")

            # Submit login form
            submit_button = page.locator(
                'button[type="submit"], input[type="submit"]'
            ).first

            if await submit_button.count() > 0:
                await submit_button.click()
            else:
                print("Submit button not identified.")
                await page.pause()
                return

            # Allow the portal to respond
            await page.wait_for_timeout(4000)

            print("Current URL:", page.url)
            print("Page title:", await page.title())

            # Keep browser open for inspection
            await page.pause()

        except Exception as exc:
            print("Portal automation error:", str(exc))

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(open_mantra_portal())