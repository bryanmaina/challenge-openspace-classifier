import json
from typing import Any

from challenge_openspace_classifier.utils.openspace import OpenSpace


class OpenspaceEncoder(json.JSONEncoder):
    def default(self, space: OpenSpace) -> dict[str, Any]:
        d = space.__dict__.copy()
        for key, value in space.__class__.__dict__.items():
            # include values returned by `@property` annotated methods
            if isinstance(value, property):
                d[key] = getattr(space, key)
        return d
