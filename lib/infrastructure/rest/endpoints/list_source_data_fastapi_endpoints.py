from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.list_source_data_view_model import ListSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_source_data_controller import ListSourceDataControllerParameter

from dependency_injector.wiring import inject, Provide


class ListSourceDataFastAPIFeature(FastAPIEndpoint[ListSourceDataControllerParameter, ListSourceDataViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.list_source_data_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.list_source_data_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": ListSourceDataViewModel,
                "description": "Success",
            },
            400: {
                "model": ListSourceDataViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": ListSourceDataViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/client/{id}/source",
            responses=self.responses,
        )
        def endpoint(
            id: int | None = None,
        ) -> ListSourceDataViewModel | None:
            try:
                controller_parameters = ListSourceDataControllerParameter(
                    client_id=id,
                )
            except ValidationError as ve:
                raise HTTPException(status_code=400, detail=ve.errors())
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            view_model: ListSourceDataViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
