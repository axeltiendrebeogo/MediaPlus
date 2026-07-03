from django import template

register = template.Library()


@register.filter
def mmss(secondes):
    """Formate une durée en secondes en 'Xm Ys' pour l'affichage PDF/rapport."""
    try:
        secondes = int(secondes or 0)
    except (TypeError, ValueError):
        return "0m 0s"
    m, s = divmod(secondes, 60)
    return f"{m}m {s:02d}s"
