from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class PoemPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = 'p' # вторая страница будет /?p=2
    page_size_query_param = 'size'  # чтобы изменить кол-во записей на стр. http://127.0.0.1:8000/api/poem/?p=2&size=3
    max_page_size = 10
    # last_page_strings = 'end'

