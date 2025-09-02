
# BDM Backend (FastAPI)

## Dev
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
uvicorn app.main:app --reload
```

## Migrations (optional)
This starter uses SQLAlchemy to auto-create tables on startup for speed. For production, add Alembic.
