import random

from app.core.adaptor.DbAdaptor import DbAdaptor
from app.core.module_class import ApiModule, TableModule
from app.core.page_engine.PageAdaptor import PageAdaptor
from app.modules.binder.table import BinderTable
from app.modules.sample.table import SampleTable
from fastapi import APIRouter, Body, Depends


class Binder(ApiModule, TableModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.get('/description')
        def description():
            return 'this is a sample module_manager description,' \
                   ' this sample will tell you how to' \
                   ' create a module_manager for Figbox'

        @bp.post('/show_body', description='description', summary='summary')
        def show_body(body: str = Body(..., embed=True)):
            return f'your body is: {body}'

        # テーブル関連
        # TODO: change table class
        @bp.post('/create', description='create data to table')
        def create(dba: DbAdaptor = Depends(DbAdaptor(BinderTable).dba),
                   link: str = Body(..., embed=True),
                   title: str = Body(..., embed=True),
                   content: str = Body(..., embed=True),):
            """create data into the table"""
            data = BinderTable(template_path='/temp.html',
                               link=link,
                               title=title,
                               content=content)
            return dba.add(data)

        # TODO: change table class
        @bp.get('/read', description='read data from table')
        def read(dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba)):
            """read data from table"""
            return dba.read_all()

        # TODO: change table class
        @bp.put('/update', description='update')
        def update(id: int, dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba),
                   data: str = Body(..., embed=True)):
            sample_data = dba.read_by_id(id)
            sample_data.data = data
            return dba.update(sample_data)

        # TODO: change table class
        @bp.delete('/delete', description='delete a data')
        def delete(id: int, dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba)):
            return dba.delete(id)

        # TODO: change table class
        @bp.get('/page/{link}', description='show a page')
        def show_page(link: str, page_adaptor: PageAdaptor = Depends()):
            return page_adaptor.bind(SampleTable, link, 'sample/temp.html')

        # 任意なプレフィックスを作成する為
        page_bp = self._register_free_prefix('/binder', 'binder')

        @page_bp.get('/{link}', description='link to page')
        def page_link(link: str, page_adaptor: PageAdaptor = Depends()):
            return page_adaptor.bind(BinderTable, link, 'binder/temp.html')

    def get_table(self) -> list:
        return [BinderTable]

    def _get_tag(self) -> str:
        return 'binder module'

    def get_module_name(self) -> str:
        return 'binder'


binder = Binder()
