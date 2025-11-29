from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.qparser import QueryParser
from whoosh.query import Term, Or, And
import os
from models import STE
import tempfile


class SearchEngine:
    def __init__(self):
        self.index_dir = os.path.join(tempfile.gettempdir(), "ste_search_index")
        self.schema = Schema(
            id=ID(stored=True, unique=True),
            name=TEXT(stored=True),
            model=TEXT(stored=True),
            country=TEXT(stored=True),
            manufacturer=TEXT(stored=True),
            category=TEXT(stored=True),
            characteristics=TEXT(stored=True)
        )
        self.ix = None

    def init_app(self, app, db):
        self.app = app
        self.db = db
        self.init_index()

    def init_index(self):
        # Создаем или открываем индекс
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
            self.ix = create_in(self.index_dir, self.schema)
            self.rebuild_index()
        else:
            try:
                self.ix = open_dir(self.index_dir)
            except:
                # Если индекс поврежден или не существует, пересоздаем его
                self.ix = create_in(self.index_dir, self.schema)
                self.rebuild_index()

    def rebuild_index(self):
        # Пересоздаем индекс на основе данных в базе
        writer = self.ix.writer()
        
        # Получаем все СТЭ из базы
        with self.app.app_context():
            ste_records = self.db.session.query(STE).all()
        
        for ste in ste_records:
            writer.add_document(
                id=str(ste.id),
                name=ste.name or "",
                model=ste.model or "",
                country=ste.country or "",
                manufacturer=ste.manufacturer or "",
                category=ste.category_name or "",
                characteristics=ste.characteristics or ""
            )
        
        writer.commit()

    def search(self, query_string="", filters=None):
        # Выполняем поиск по индексу
        results = []
        
        if not query_string and not filters:
            return results
            
        with self.ix.searcher() as searcher:
            # Создаем основной запрос
            main_query = None
            
            if query_string:
                # Используем QueryParser для основного поискового запроса
                # Поиск будет выполняться по нескольким полям
                from whoosh.qparser import MultifieldParser
                parser = MultifieldParser(['name', 'model', 'manufacturer', 'category', 'characteristics'], self.ix.schema)
                main_query = parser.parse(query_string)
            
            # Применяем фильтры
            if filters:
                filter_queries = []
                for field, value in filters.items():
                    if value.strip():
                        # Проверяем, что поле существует в схеме
                        if field in ['name', 'model', 'country', 'manufacturer', 'category']:
                            filter_queries.append(Term(field, value))
                
                if filter_queries:
                    if main_query:
                        # Если есть основной запрос, объединяем с фильтрами через AND
                        main_query = And([main_query] + filter_queries)
                    else:
                        # Если только фильтры, объединяем их через AND
                        if len(filter_queries) == 1:
                            main_query = filter_queries[0]
                        else:
                            main_query = And(filter_queries)
            
            # Если нет основного запроса и фильтров, возвращаем пустой результат
            if not main_query:
                return results
            
            # Выполняем поиск
            search_results = searcher.search(main_query, limit=None)  # Убираем ограничение
            
            # Получаем ID результатов
            result_ids = [int(result['id']) for result in search_results]
            
            # Загружаем полные объекты из базы данных
            with self.app.app_context():
                results = self.db.session.query(STE).filter(STE.id.in_(result_ids)).all()
                
        return results