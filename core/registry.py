from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelInfo:
    model_id: str
    name: str
    provider: str

    capabilities: List[str] = field(default_factory=list)

    quality_score: float = 0.0
    speed_score: float = 0.0
    cost_score: float = 0.0

    is_free: bool = False
    is_available: bool = True

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolInfo:
    tool_id: str
    name: str
    category: str

    capabilities: List[str] = field(default_factory=list)

    quality_score: float = 0.0
    speed_score: float = 0.0
    cost_score: float = 0.0

    is_free: bool = False
    is_available: bool = True

    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, ModelInfo] = {}

    def register(self, model: ModelInfo) -> None:
        self.models[model.model_id] = model

    def get(self, model_id: str) -> Optional[ModelInfo]:
        return self.models.get(model_id)

    def list(
        self,
        capability: Optional[str] = None,
    ) -> List[ModelInfo]:

        models = list(self.models.values())

        if capability:
            models = [
                model
                for model in models
                if capability in model.capabilities
            ]

        return [
            model
            for model in models
            if model.is_available
        ]


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}

    def register(self, tool: ToolInfo) -> None:
        self.tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> Optional[ToolInfo]:
        return self.tools.get(tool_id)

    def list(
        self,
        capability: Optional[str] = None,
    ) -> List[ToolInfo]:

        tools = list(self.tools.values())

        if capability:
            tools = [
                tool
                for tool in tools
                if capability in tool.capabilities
            ]

        return [
            tool
            for tool in tools
            if tool.is_available
        ]


model_registry = ModelRegistry()
tool_registry = ToolRegistry()
