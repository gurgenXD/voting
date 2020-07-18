from django.db import models
from django.urls import reverse
from django.utils import timezone


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
    XLSX_STATUSES = (
        (1, 'Сгенерирован'),
        (2, 'Генерируется'),
        (3, 'Сгенерировать'),
    )

    title = models.CharField('Название', max_length=250)
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    max_votes = models.PositiveIntegerField('Максимальное количество голосов', null=True, blank=True,
                                            help_text='Максимальное количество голосов для досрочного завершения.')
    xlsx = models.FileField(upload_to='xlsx/', verbose_name='XLSX файл', null=True, blank=True)
    xlsx_status = models.CharField(max_length=32, choices=XLSX_STATUSES, verbose_name='Статус XLSX файла', default=3)

    def is_active(self):
        now = timezone.now()

        if now > self.end_date or now <= self.start_date:
            return False

        if self.max_votes:
            for item in self.person_votes.all():
                if self.max_votes <= item.votes:
                    return False
        return True

    def get_absolute_url(self):
        return reverse('voting_page', args=[self.id])

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
        ordering = ('-votes',)
        unique_together = ('person', 'voting')

    def __str__(self):
        return f'{self.voting} - {self.person}'
