from typing import Self

from pydantic import BaseModel, ConfigDict


class QuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    async def as_query(cls, **kwargs) -> Self:
        raise NotImplementedError("Override this method in child model")
