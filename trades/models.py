import datetime
from django.db import models
from django.utils import timezone

class Trade(models.Model):
    ticker = models.CharField('Ticker', max_length=20)
    currency = models.CharField('Currency', max_length=5)
    purchase_date = models.DateTimeField('Date purchased', auto_now=True)
    sell_date = models.DateTimeField('Date sold', auto_now=False)
    number_of_shares = models.IntegerField('Number of shares', default=1)
    owner = models.EmailField()
    price = models.FloatField()

    def __str__(self):
        return self.ticker + ' ' + purchase_date

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text
