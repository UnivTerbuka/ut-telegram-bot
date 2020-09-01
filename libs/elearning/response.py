from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ResponseMoodle:
    error: bool
    data: Optional[Any] = None
