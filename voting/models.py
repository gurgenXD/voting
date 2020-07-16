from django.db import models


class Person(models.Model):
    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)
    image = models.ImageField(upload_to='persons/', verbose_name='Изображение')
    age = models.PositiveIntegerField('Возраст')
    biography = models.TextField('Краткая биография')

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'

    def __str__(self):
        return self.get_full_name()


class Voting(models.Model):
    title = models.CharField('Название', max_length=250)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    max_votes = models.PositiveIntegerField('Максимальное количество голосов', null=True, blank=True,
                                            help_text='Максимальное количество голосов для досрочного завершения.')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'
        ordering = ('start_date',)

    def __str__(self):
        return self.title


class PersonVotes(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Персонаж', related_name='person_votes')
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, verbose_name='Голосование', related_name='person_votes')
    votes = models.PositiveIntegerField('Количество голосов', default=0)

    def save(self, *args, **kwargs):
        if self.voting.max_votes:
            if self.votes >= self.voting.max_votes:
                self.voting.is_active = False
                self.voting.save()
        super(PersonVotes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Участник голосования'
        verbose_name_plural = 'Участники голосования'

    def __str__(self):
        return f'{self.voting} - {self.person}'