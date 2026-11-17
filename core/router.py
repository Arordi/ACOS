from typing import List, Optional

from core.registry import ModelInfo, ToolInfo, model_registry, tool_registry


class ModelRouter:
    """
    Selects the most suitable model or tool for a task.

    Priority:
    1. Capability match
    2. Quality
    3. Free/open-source preference
    4. Cost
    5. Speed
    """

    def select_model(
        self,
        capability: str,
        prefer_free: bool = True,
        minimum_quality: float = 0.0,
    ) -> Optional[ModelInfo]:

        candidates: List[ModelInfo] = model_registry.list(
            capability=capability
        )

        candidates = [
            model
            for model in candidates
            if model.quality_score >= minimum_quality
        ]

        if not candidates:
            return None

        candidates.sort(
            key=lambda model: (
                model.quality_score,
                1 if prefer_free and model.is_free else 0,
                model.cost_score,
                model.speed_score,
            ),
            reverse=True,
        )

        return candidates[0]

    def select_tool(
        self,
        capability: str,
        prefer_free: bool = True,
        minimum_quality: float = 0.0,
    ) -> Optional[ToolInfo]:

        candidates: List[ToolInfo] = tool_registry.list(
            capability=capability
        )

        candidates = [
            tool
            for tool in candidates
            if tool.quality_score >= minimum_quality
        ]

        if not candidates:
            return None

        candidates.sort(
            key=lambda tool: (
                tool.quality_score,
                1 if prefer_free and tool.is_free else 0,
                tool.cost_score,
                tool.speed_score,
            ),
            reverse=True,
        )

        return candidates[0]


model_router = ModelRouter()
