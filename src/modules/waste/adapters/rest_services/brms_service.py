# !/usr/bin/python3
# type: ignore

# ** info: python imports
from urllib.parse import urljoin
import logging

# ** info: typing imports
from typing import Self

# ** info: httpx imports
from httpx import Response
import httpx

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: artifacts imports
from src.sidecards.artifacts.env_provider import EnvProvider


__all__: list[str] = ["BrmsService"]


class BrmsService:
    def __init__(self: Self):
        self._env_provider: EnvProvider = EnvProvider()
        self.base_url: str = str(self._env_provider.sar_brms_base_url)

    def obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        data: dict[str, str] = {"stateWaste": state_waste, "weightInKg": weight_in_kg, "isotopesNumber": isotopes_number}
        url: str = urljoin(self.base_url, r"/brms/waste/clasification")

        logging.debug(f"brms url: {url}")

        try:
            raw_response: Response = httpx.post(url, json=data)
        except Exception:
            logging.critical("error unable to connect to brms")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

        logging.debug(f"brms url: {url}")

        if raw_response.status_code != status.HTTP_200_OK:
            logging.critical("the brms service didnt respond correctly")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

        response: int

        try:
            response = int(raw_response.text)
        except Exception:
            logging.critical("error parsing response from brms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if response == 0:
            logging.critical("the waste was not classified by the brms")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="waste not classifiable")

        return response