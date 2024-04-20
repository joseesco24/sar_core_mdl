# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging

# ** info: typing imports
from typing import Callable
from typing import Self

# ** info: loguru imports
from loguru import logger

# ** info: starlette imports
from starlette.responses import StreamingResponse
from starlette.requests import Request

# ** info: sidecards.system.artifacts imports
from src.sidecard.system.artifacts.datetime_provider import DatetimeProvider
from src.sidecard.system.artifacts.uuid_provider import UuidProvider

# ** info: sidecards.system.middlewares.inheritables imports
from src.sidecard.system.middlewares.inheritables.base_middleware import BaseMiddleware


__all__: list[str] = ["LoggerContextualizerMiddleware"]


class LoggerContextualizerMiddleware(BaseMiddleware):

    def __init__(self: Self) -> None:
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._uuid_provider: UuidProvider = UuidProvider()

    async def __call__(
        self: Self,
        request: Request,
        call_next: Callable,
    ) -> StreamingResponse:

        request_id_is_uuid: bool = UuidProvider.check_str_uuid(request.headers[r"request-id"]) if r"request-id" in request.headers else False
        internal_id: str = self._uuid_provider.get_str_uuid()
        external_id: str = request.headers[r"request-id"] if request_id_is_uuid is True else internal_id
        full_url: str = str(request.url)

        if request_id_is_uuid is False:
            logging.warning(f"request-id header is not a valid uuid, using internal id: {internal_id}")
        else:
            logging.info(f"request-id header is a valid uuid: {external_id}")

        response: StreamingResponse

        with logger.contextualize(
            rqStartTime=self._datetime_provider.get_current_time(),
            internalId=internal_id,
            externalId=external_id,
        ):
            logging.debug("starting request")
            logging.info(f"request url: {request.method} - {full_url}")
            logging.debug("logger contextualizer middleware started")

            response = await call_next(request)

            logging.debug("logger contextualizer middleware ended")
            logging.info(f"request ended with status {response.status_code}")
            logging.debug("request ended sucessfully")

        return response
