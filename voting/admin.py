from django.contrib import admin
from django.utils.html import mark_safe
from voting.models import Person, PersonVotes, Voting


class PersonVotesInline(admin.TabularInline):
    model = PersonVotes
    extra = 0


@admin.register(Voting)
class AdminVoting(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'max_votes', 'is_active')
    search_fields = ('title',)
    inlines = (PersonVotesInline,)

    def is_active(self, obj):
        if obj.is_active():
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_active.short_description = 'Активно'


@admin.register(Person)
class AdminPerson(admin.ModelAdmin):
    list_display = ('get_full_name', 'age')
    search_fields = ('last_name', 'first_name', 'patronymic', 'biography')
