from django.contrib import admin

from django.contrib import admin
from .models import Station, Route, Stop


class StopInline(admin.TabularInline):
    model = Stop
    extra = 0


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [StopInline]
    fieldsets = [
        ('Информация про поезд', {'fields': ('train',)}),
        ('Информация про маршрут', {'fields': [('from_station', 'to_station'), ('departure_time', 'arrival_time'),
                                               'starting_price']}),
    ]
    autocomplete_fields = ['from_station', 'to_station']
    list_display = ['rout', 'departure_time', 'arrival_time']
    list_filter = ['from_station', 'to_station']
    search_fields = ['from_station__name', 'to_station__name']

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        queryset |= self.model.objects.filter(from_station__name__icontains=search_term)
        queryset |= self.model.objects.filter(to_station__name__icontains=search_term)
        return queryset, may_have_duplicates

    @admin.display(description="Маршрут")
    def rout(self, rout):
        return f"{rout.from_station}-{rout.to_station}"

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    fields = ['name', 'city', 'country']
    search_fields = ["name", 'city']
    list_display = ['name', 'city', 'country']
