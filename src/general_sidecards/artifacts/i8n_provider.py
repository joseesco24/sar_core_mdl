# !/usr/bin/python3
# type: ignore

# ** info: python imports
from os.path import realpath
from os.path import dirname
from os.path import join
import locale
import json

# ** info: typing imports
from typing import Dict
from typing import Self

# Jinja
from jinja2 import Template

__all__: list[str] = ["I8nProvider"]


class I8nProvider:

    __slots__ = ["_locale_dir", "_messages_dict", "_logs_dict"]

    def __init__(self: Self, module: str) -> None:
        self._locale_dir: str = join(dirname(realpath(__file__)), "..", "i8n_files", self._get_locale_languaje())
        self._messages_dict: dict[str, str] = json.load(open(join(self._locale_dir, "messages.json")))[module]

    def _get_locale_languaje(self: Self) -> str:
        # todo: repalir thie method currently the linter is not recognizing the locale.getdefaultlocale() method
        locale_languaje: str = locale.getdefaultlocale()[0] if locale.getdefaultlocale()[0] != "C" else "en_US"
        return locale_languaje

    def message(self: Self, message_key: str, **kwargs) -> str:
        return self._get_message_from_dict(dict=self._messages_dict, key=message_key, **kwargs)

    def _get_message_from_dict(self: Self, dict: Dict, key: str, **kwargs) -> str:
        raw_message: str = dict[key] if key in dict else key
        return_message: Template = Template(raw_message).render(**kwargs) if bool(kwargs) else raw_message
        return return_message.lower()
