from keptcha import Captcha

captcha = Captcha.new()
captcha.decode()

if captcha.verify("weifjweuif"):
    print("You are not a bot!")
