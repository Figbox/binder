from app.core.table_class import PageTable
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String


# see https://fastapi.tiangolo.com/tutorial/sql-databases/
class BinderTable(PageTable):
    __tablename__ = 'binder'
    template_path = Column(String(250))
