# Keptcha py

`keptcha` is an API wrapper (python) for [captcha-api](https://captcha-api.akshit.me). Provides both Synchronous and Asynchronous interfaces to interact with the API.

## Installation

```sh
pip install keptcha
```
> The project is not yet released on pypi so above would not work, proceed with git installation.

OR using git

```sh
pip install git+https://github.com/captcha-api/keptcha-py
```

## Usage

`keptcha` supports both Sync and Async usage.

### Sync

```py
from keptcha import Captcha

my_captcha = Captcha.new()
my_captcha.decode()

if my_captcha.verify("1337H4kOr"):
    print("You are not a bot!")
```

### Async

```py
from keptcha import AsyncCaptcha

my_captcha = await AsyncCaptcha.new()
await my_captcha.decode()

if (await my_captcha.verify("1337H4kOr")):
    print("You are not a bot!")
```

## Configuration

You can pass some keyword arguments to personalize your captcha.

```py
my_captcha = Captcha.new(height=100, width=250, circles=100, length=5)
```

## How to handle bad input?

You can do exception handling.

```py
from keptcha.errors import IncorrectCaptcha

try:
    my_captcha.verify("bad input")
except IncorrectCaptcha:
    print("sir you suck")
```

## Contributing

Feel free to submit a pull request. We very much appreciate it!

## License

Licenced under [MIT](LICENSE).