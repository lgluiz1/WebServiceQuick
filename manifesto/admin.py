from django.contrib import admin
from .models import Manifesto, Minuta, ResumoNatureza, Descarregamento, ManifestoModelo

admin.site.register(Manifesto)
admin.site.register(Minuta)
admin.site.register(ResumoNatureza)
admin.site.register(Descarregamento)
admin.site.register(ManifestoModelo)

