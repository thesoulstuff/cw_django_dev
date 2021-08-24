from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')

    @property
    def ranking(self):
        RANKING_SCORE = {
            'answer': 10,
            'like': 5,
            'dislike': 3,
            'new': 10 
        }
        n_answers  = Answer.objects.filter(question=self, value__gt=0).count()
        n_likes = Answer.objects.filter(question=self, liked=True).count()
        n_dislikes = Answer.objects.filter(question=self, liked=False).count()
        ranking = 10 if self.created == datetime.now().date() else 0
        ranking += n_answers*RANKING_SCORE["answer"]
        ranking += n_likes*RANKING_SCORE["like"]
        ranking -= n_dislikes*RANKING_SCORE["dislike"]
        return ranking
        

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = ((0,'Sin Responder'),
                      (1,'Muy Bajo'),
                      (2,'Bajo'),
                      (3,'Regular'),
                      (4,'Alto'),
                      (5,'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0)
    comment = models.TextField("Comentario", default="", blank=True)
    liked = models.BooleanField(verbose_name="Me Gusta", null=True)
