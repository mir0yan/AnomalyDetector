from fastapi import FastAPI

import uvicorn



def start_api_server(application: FastAPI, host: str, port: int) -> None:
    uvicorn.run(application, host=host, port=port)
