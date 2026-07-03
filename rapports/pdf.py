from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML

from .models import Rapport


def generer_pdf_rapport(rapport: Rapport):
    """Rend le template HTML du rapport en PDF (WeasyPrint) et l'attache à rapport.fichier_pdf."""
    stats = rapport.stats or {}

    contexte = {
        "titre": rapport.titre,
        "type_rapport": rapport.type_rapport,
        "periode_debut": rapport.periode_debut.strftime("%d/%m/%Y"),
        "periode_fin": rapport.periode_fin.strftime("%d/%m/%Y"),
        "date_generation": timezone.now().strftime("%d/%m/%Y à %H:%M"),
        "genere_par_nom": rapport.genere_par.nom,
        "inclure_graphiques": rapport.inclure_graphiques,
        "inclure_stats": rapport.inclure_stats,
        # Rapport "media"
        "kpi": stats.get("kpi"),
        "graphiques": stats.get("graphiques"),
        "stats_detaillees": stats.get("stats_detaillees"),
        # Rapport "global"
        "sections_par_media": stats.get("sections_par_media"),
        "comparaison": stats.get("comparaison"),
    }

    html_string = render_to_string("rapports/rapport_pdf.html", contexte)
    pdf_bytes = HTML(string=html_string).write_pdf()

    nom_fichier = f"rapport-{rapport.id}-{rapport.type_rapport}.pdf"
    rapport.fichier_pdf.save(nom_fichier, ContentFile(pdf_bytes), save=False)
