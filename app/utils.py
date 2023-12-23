import typing

import orjson
from starlette.responses import JSONResponse


class CustomJSONResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps({"meta": {"code": 200, "message": "ok"}, "data": content})
