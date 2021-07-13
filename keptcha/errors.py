class StatusError(BaseException):
    """Error raised on bad status code"""

    def __init__(self, resp_json: dict, status: int):
        self.resp_json = resp_json
        self.status = status

    def __str__(self):
        return self.resp_json["message"]


class BadRequest(StatusError):
    def __repr__(self):
        return "BadRequest('{}', status={})".format(self.resp_json["message"], self.status)


class IncorrectCaptcha(StatusError):
    def __repr__(self):
        return "IncorrectCaptcha('{}', status={})".format(self.resp_json["message"], self.status)


class UUIDExpired(StatusError):
    def __repr__(self):
        return "UUIDExpired('{}', status={})".format(self.resp_json["message"], self.status)


class AlreadySolved(StatusError):
    def __repr__(self):
        return "AlreadySolved('{}', status={})".format(self.resp_json["message"], self.status)


class TooManyTries(StatusError):
    def __repr__(self):
        return "TooManyTries('{}', status={}".format(self.resp_json["message"], self.status)
