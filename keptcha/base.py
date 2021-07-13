class BaseCaptcha:
    """Base Captcha class
    
    `Captcha` and `AsyncCaptcha` inherit from this.
    """

    API_BASE_URL = "https://captcha-api.akshit.me/v2"
    VERIFY_ENDPOINT = "/verify"
    GENERATE_ENDPOINT = "/generate"
