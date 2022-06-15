import logging
import os

import uvicorn

debug = os.getenv("DEBUG", False) == "True"
logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
logging.info(f'Debugging={os.getenv("DEBUG", False)!r}')

uvicorn.run(
    "bit.endpoints.api:api_app",
    port=8000,
    log_level="debug" if debug else "info",
    reload=debug,
)
