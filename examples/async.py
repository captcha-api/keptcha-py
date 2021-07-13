import asyncio

from keptcha import AsyncCaptcha

async def main():

    captcha = await AsyncCaptcha.new(close_session_after_verify=True)
    await captcha.decode()

    if (await captcha.verify("weifjweuif")):
        print("You are not a bot!")

asyncio.run(main())