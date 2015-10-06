from django.db import models

class Center(models.Model):
    name      = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    
    def __unicode__(self):
            return self.name

class Donor(models.Model):
    name  = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __unicode__(self):
            return self.name


class Donation(models.Model):
    FREQUENCY_CHOICES = (
        ('1','One-time'),
        ('2','Monthly'),
    )
    
    donor      = models.ForeignKey('Donor')
    center     = models.ForeignKey('Center')
    amount     = models.CharField(max_length=10)
    dt_donated = models.DateTimeField()
    anon       = models.BooleanField()
    frequency  = models.CharField(max_length=1, choices=FREQUENCY_CHOICES)
    key        = models.CharField(max_length=20)
    confirmed  = models.BooleanField()
    
    def __unicode__(self):
            return self.amount
    
    class Meta:
        ordering = ['-dt_donated']
