from django.contrib import admin
from voting.models import Person, PersonVotes, Voting


class PersonVotesInline(admin.TabularInline):
    model = PersonVotes
    extra = 0


@admin.register(Voting)
class AdminVoting(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'max_votes', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    inlines = (PersonVotesInline,)


@admin.register(Person)
class AdminPerson(admin.ModelAdmin):
    list_display = ('get_full_name', 'age')
    search_fields = ('last_name', 'first_name', 'patronymic', 'biography')
