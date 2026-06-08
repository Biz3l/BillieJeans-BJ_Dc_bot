import sqlalchemy as sa
import databases
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database"

DATABASE_URL = f"sqlite:///{DB_PATH}/database.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#TODO: Tenho que mudar mais itens que ficaram pendentes da migração da pasta da API para a pasta da database