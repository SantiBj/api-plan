from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    # definir el numero de elmentos de la pagina
    page_size = 8
    # definir como se llama el queriparam que biene por la url
    page_query_param = 'page'
    # se define el numero paginas maximas que tendra la vista que la implemente
    max_page_size = 100