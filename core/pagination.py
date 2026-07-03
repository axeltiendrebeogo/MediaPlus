from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Pagination standard utilisée sur tous les endpoints de liste.
    Conforme au contrat API : { "count", "next", "previous", "results" }
    Paramètres : ?page= et ?page_size= (défaut 20, max 100 — voir §5.1 du CdC)
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
