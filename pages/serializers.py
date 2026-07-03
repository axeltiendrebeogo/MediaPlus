from rest_framework import serializers

from .models import PageWeb


class PageListSerializer(serializers.ModelSerializer):
    """
    GET /api/pages/ — §5.1 du CdC.
    vues / visiteurs_uniques / duree_moyenne / scroll_moyen sont calculés
    par annotation SQL dans la queryset (voir pages/views.py) — pas des
    colonnes stockées.
    """

    media_id = serializers.IntegerField(source="media.id", read_only=True)
    vues = serializers.IntegerField(read_only=True)
    visiteurs_uniques = serializers.IntegerField(read_only=True)
    duree_moyenne = serializers.SerializerMethodField()
    scroll_moyen = serializers.SerializerMethodField()

    class Meta:
        model = PageWeb
        fields = [
            "id", "nom", "url", "date_publication", "auteur", "media_id",
            "vues", "visiteurs_uniques", "duree_moyenne", "scroll_moyen",
        ]

    def get_duree_moyenne(self, obj):
        val = getattr(obj, "duree_moyenne", None)
        return round(val) if val is not None else 0

    def get_scroll_moyen(self, obj):
        val = getattr(obj, "scroll_moyen", None)
        return round(val) if val is not None else 0


class PageDetailSerializer(PageListSerializer):
    """GET /api/pages/:id/ — même forme que la liste, un seul objet."""

    pass
