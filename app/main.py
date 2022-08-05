from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import accounts, planner, search, graph, tests

app = FastAPI()

## middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## router
app.include_router(router=accounts.router, prefix="/api")
app.include_router(router=planner.router, prefix="/api")
app.include_router(router=search.router, prefix="/api")
app.include_router(router=graph.router, prefix="/api")
app.include_router(router=tests.router, prefix="/api")