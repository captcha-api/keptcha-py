from keptcha import Captcha
from PIL import Image

from io import BytesIO

captcha = Captcha.new(height=250, width=500, circles=150, length=10)
captcha.decode()

img = Image.open(BytesIO(captcha.captcha_decoded))
img.show()
