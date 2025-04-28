from django.contrib import admin
from .models import *

class StockAdmin(admin.ModelAdmin):
    list_display=("refMateriel","designation","situation","lieu","client","categorie")
admin.site.register(Stock,StockAdmin)

class ChargesaffaireAdmin(admin.ModelAdmin):
    list_display=("name","email","phone")
admin.site.register(Chargesaffaire,ChargesaffaireAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display=("refReservation","chargerAffaire","dateReservation","client","etat","created_at")
admin.site.register(Reservation,ReservationAdmin)

class DetilsReservationAdmin(admin.ModelAdmin):
    list_display=("refReservation","designation","qte","dateLivraison","dateRetour")
admin.site.register(DetilsReservation,DetilsReservationAdmin)

class ModulaireAdmin(admin.ModelAdmin):
    list_display=("id","gamme","dimension","refMateriel")
admin.site.register(Modulaire,ModulaireAdmin)

class GroupeElectrogeneAdmin(admin.ModelAdmin):
    list_display=("id","puissance","marque","dimension","refMateriel")
admin.site.register(GroupeElectrogene,GroupeElectrogeneAdmin)

class CabinesAutonomeAdmin(admin.ModelAdmin):
    list_display=("id","gamme","dimension","color","refMateriel")
admin.site.register(CabinesAutonome,CabinesAutonomeAdmin)


class MovementAdmin(admin.ModelAdmin):
    list_display=("id","typeMovement","dateMovement","typeLocation","refMateriel","designation","qte","matTrans","condTrans","lieu","observations")

admin.site.register(Movement,MovementAdmin)    