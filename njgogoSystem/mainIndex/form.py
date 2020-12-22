from django import forms
from .models import *


class userform(forms.ModelForm):
    username = forms.CharField(label='账户', required=True)
    passwd = forms.CharField(label='密码', widget=forms.PasswordInput(), required=True)

    class Meta:
        model = user
        fields = ('username', 'passwd')


class matchlistform(forms.Form):
    matchname = forms.CharField(label='比赛名称', required=True,error_messages = {
            "required":    "不能为空",
            "invalid":    "格式错误",
            "max_length":     "用户名最长20位"
    })
    matchtype=forms.CharField(label='比赛类型',required=True)
    matchBMtype=forms.CharField(label="报名方式",required=True)


class baominglistform(forms.Form):
    # gametype=forms.CharField(label='',max_length=8)
    company=forms.CharField(label='',required=True)
    contactPeople=forms.CharField(label='',required=True)
    contactNumber = forms.CharField(label='', required=True)
    # player1=forms.CharField(label='运动员',required=True)
    # player1id=forms.CharField(label='居民二代身份证',required=True)
    # player2 = forms.CharField(label='运动员')
    # player2id = forms.CharField(label='居民二代身份证')
    playerall=forms.CharField(label='',required=True)

# class fenzuform(forms.Form):
#     zubie_num=forms.IntegerField(label="",required=True)
#     chuxian_num=forms.IntegerField(label="",required=True)

class exportform(forms.Form):
    exp_gametype=forms.CharField(label='',required=True)
    exp_fenzuqk=forms.CharField(label='',required=True)
    exp_taotaiqk=forms.CharField(label='',required=True)

class lufenform(forms.Form):
    zhixuceID=forms.CharField(label='')
    shengli1=forms.CharField(label='',required=True)
    shibai1 = forms.CharField(label='', required=True)
    fenshu11=forms.CharField(label='')
    fenshu12 = forms.CharField(label='')
    shengli2 = forms.CharField(label='', required=True)
    shibai2 = forms.CharField(label='', required=True)
    fenshu21 = forms.CharField(label='')
    fenshu22 = forms.CharField(label='')
    shengli3 = forms.CharField(label='',)
    shibai3 = forms.CharField(label='',)
    fenshu31 = forms.CharField(label='')
    fenshu32 = forms.CharField(label='')
    # zongshengli=forms.CharField(label='')
class jifentrigger(forms.Form):
    zhixuceid=forms.CharField(label='')

class caipanlistform(forms.Form):
    caipanlist = forms.CharField(label="")