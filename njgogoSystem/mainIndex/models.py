from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(max_length=20)
    passwd=models.CharField(max_length=15)
class matchlist(models.Model):
    matchname=models.CharField(max_length=20)
    # matchid=models.IntegerField()
    createuser=models.CharField(max_length=20)
    matchtype=models.CharField(max_length=60)
    matchBMtype=models.CharField(max_length=20)
class playerlist(models.Model):
    matchid=models.IntegerField()
    playerCompany=models.CharField(max_length=20)
    playerType=models.CharField(max_length=10)
    player1Name=models.CharField(max_length=8)
    player1Id=models.CharField(max_length=19)
    player2Name = models.CharField(max_length=8,null=True)
    player2Id = models.CharField(max_length=19,null=True)
    contact=models.CharField(max_length=8)
    contactNumber=models.CharField(max_length=11)
class zhixuce(models.Model):
    matchid=models.IntegerField()
    gametype=models.CharField(max_length=20)
    # matchdetail=models.CharField(max_length=30)
    player1=models.CharField(max_length=20)
    player2=models.CharField(max_length=20)
    lunshu=models.IntegerField()
    zubie=models.IntegerField()
    changci=models.IntegerField()
    # huosheng=models.CharField(max_length=20)
class fenzu(models.Model):
    matchid=models.IntegerField()
    gametype=models.CharField(max_length=20)
    zubie = models.IntegerField()
    fenzuqk=models.CharField(max_length=1000)
class saichang(models.Model):
    zhixuceid=models.IntegerField()
    huosheng=models.CharField(max_length=20)
    fenshu1=models.IntegerField()
    fenshu2=models.IntegerField()
    huobai=models.CharField(max_length=20)
class caipanall(models.Model):
    matchid=models.IntegerField()
    caipan=models.CharField(max_length=500)