from abc import abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import Any

__all__ = ["IMDFFeature", "IMDFFeatureReference"]


class IMDFFeature(BaseModel):
    model_config = ConfigDict(
        # extra="allow,"
        arbitrary_types_allowed=True
    )

    id: str  # ae095f89-49f8-4189-b5dd-9c6d62de3203

    @abstractmethod
    def to_imdf_spec_feature(self) -> dict[str, Any]:
        raise NotImplementedError


class IMDFFeatureReference(IMDFFeature):
    feature_type: str  # IMDFFeatureType  # building

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        return self.model_dump()
