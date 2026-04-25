arginotebook_be/
│
├── api.py                 # File chạy chính (Khởi tạo FastAPI app)
│
├── routers/               # Tầng Route (Endpoint): Chỉ nhận Request và trả về Response
│   ├── notebooks.py       # Các API như /notebooks, /notebooks/{id}
│   ├── llms.py            # Các API quản lý LLM
│   └── generate.py        # API kích hoạt quá trình viết bài
│
├── services/              # Tầng Logic (Controller/Service): Trái tim của hệ thống
│   ├── notebook_svc.py    # Xử lý logic của sổ tay
│   └── ai_generation.py   # Ghép nối data từ MySQL, gọi VectorDB và LLM
│
├── databases/             # Tầng Database (CRUD): Chỉ chứa các lệnh thao tác MySQL
│   ├── crud_notebook.py   # Lệnh SELECT, INSERT, UPDATE cho bảng notebooks
│   ├── crud_llm.py        # Lệnh thao tác bảng llm_configs
│   └── connection.py      # Cấu hình kết nối MySQL (SQLAlchemy/PyMySQL)
│
├── schemas/               # Tầng Pydantic: Khai báo format dữ liệu vào/ra (để validate)
│   └── notebook_schema.py 
│
└── ai_core/               # Tầng Model AI (Lõi bạn đã viết)
    ├── preprocessor.py    # Chunking, Embedding, lưu ChromaDB
    ├── wiki_composer.py   # Agent viết bài, RAG logic
    ├── llm_engine.py      # Giao tiếp với LLM API
    └── extractor.py       # Trích xuất PDF, web, youtube


Quy trình
Router (routers/llms.py): Là người bồi bàn, chuyên ghi nhận yêu cầu từ khách.
-> Schema (schemas/llm_schema.py): Là người kiểm duyệt (bảo vệ), kiểm tra xem phiếu yêu cầu có ghi đúng thông tin không (tránh lỗi).
-> CRUD (databases/crud_llm.py): Là đầu bếp, người trực tiếp xuống kho (MySQL) để lấy hoặc cất nguyên liệu.