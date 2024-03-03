# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyResponseDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto

# ** info: app core imports
from src.modules.waste.cores.business.waste_core import WasteCore

# ** info: sidecards imports
from src.sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["WasteRouter"]


class WasteRouter:

    def __init__(self: Self):
        # ** info: building artifacts
        self._path_provider: PathProvider = PathProvider()
        # ** info: building needed cores
        self._waste_core: WasteCore = WasteCore()
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=self._path_provider.build_posix_path("waste"), tags=["Wastes"])

        # ** info: bulding router endpoints
        self.router.add_api_route(
            description="classifies the waste according to its attributes",
            summary="classifies the waste according to its attributes",
            path=self._path_provider.build_posix_path("clasification", "obtain"),
            response_model=WasteClasificationResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_obtain_waste_classify,
            methods=["POST"],
        )

        # ** info: bulding router endpoints
        self.router.add_api_route(
            description="classify a waste by id request description",
            summary="classify a waste by id request summary",
            path=self._path_provider.build_posix_path("clasification", "update"),
            response_model=WasteClassifyResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_update_waste_classify,
            methods=["POST"],
        )

    async def _api_obtain_waste_classify(self: Self, parameter_search_request: WasteClasificationRequestDto = Body(...)) -> WasteClasificationResponseDto:
        waste_classify_response: WasteClasificationResponseDto = await self._waste_core.driver_obtain_waste_classify(parameter_search_request)
        return waste_classify_response

    async def _api_update_waste_classify(self: Self, waste_classify_request: WasteClassifyRequestDto = Body(...)) -> WasteClassifyResponseDto:
        waste_classify_response: WasteClassifyResponseDto = await self._waste_core.driver_update_waste_classify(waste_classify_request)
        return waste_classify_response