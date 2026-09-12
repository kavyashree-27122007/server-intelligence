import os
import sys
import traceback
from pathlib import Path

# Add project root to sys.path so 'app' can be imported anywhere
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from app.main import app
except Exception as exc:
    # If the real app fails to import, create a diagnostic app
    # that shows the actual error in Vercel logs and browser
    error_detail = traceback.format_exc()
    print(f"IMPORT ERROR:\n{error_detail}", file=sys.stderr, flush=True)

    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    app = FastAPI()

    @app.get("/{path:path}")
    @app.post("/{path:path}")
    async def diagnostic(path: str = ""):
        return PlainTextResponse(
            f"App failed to import. Error:\n\n{error_detail}",
            status_code=500,
        )
