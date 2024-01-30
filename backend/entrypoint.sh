#!/bin/sh
PORT=${PORT:-3000}
exec uvicorn backend.src.mlcb_services.api.main:app --host 0.0.0.0 --port $PORT --reload
