from django.contrib import admin
from django.utils.html import mark_safe
from voting.models import Person, PersonVotes, Voting


class PersonVotesInline(admin.TabularInline):
    model = PersonVotes
    extra = 0


@admin.register(Voting)
class AdminVoting(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'max_votes', 'download_xlsx', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('xlsx', )
    inlines = (PersonVotesInline,)

    def is_active(self, obj):
        if obj.is_active():
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_active.short_description = 'Активно'

    def download_xlsx(self, obj):
        if obj.xlsx_status == 'generated':
            return mark_safe(f'<a href="{obj.xlsx.url}">{obj.xlsx.name}</a>')
        elif obj.xlsx_status == 'processing':
            return mark_safe('<span>Генерируется...</span>')
        else:
            return mark_safe(f'<a href="/create-xlsx/{obj.id}">Сгенерировать XLSX файл</a>')
    download_xlsx.short_description = 'XLSX файл'


@admin.register(Person)
class AdminPerson(admin.ModelAdmin):
    list_display = ('get_full_name', 'age')
    search_fields = ('last_name', 'first_name', 'patronymic', 'biography')
