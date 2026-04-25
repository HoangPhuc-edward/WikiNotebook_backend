from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Khai báo thư mục routers
from routers import llms, notebooks, content, generate
app = FastAPI(title="WikiCrop AI Writing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [THÊM DÒNG NÀY] Nhúng router vào ứng dụng
app.include_router(llms.router)
app.include_router(notebooks.router)
app.include_router(content.router)
app.include_router(generate.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)