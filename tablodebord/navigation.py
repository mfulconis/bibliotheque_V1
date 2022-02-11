from django.urls import reverse, reverse_lazy

NAV_ACCUEIL = 'Accueil'
NAV_RECHERCHE = 'Rechercher'
NAV_SAVE = 'MAJ BdD'

NAV_ITEMS = (
    (NAV_ACCUEIL, reverse_lazy('accueil')),
    (NAV_RECHERCHE, reverse_lazy('recherche')),
    (NAV_SAVE, reverse_lazy('save'))
)

def navigation_items(selected_item):
    items = []
    for name, url in NAV_ITEMS:
        items.append({
            'name' : name,
            'url' : url,
            'active' : True if selected_item == name else False
        })
    return items
