# coding:utf8

from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=30)
    mobilePhone = models.CharField(max_length=30)

    mail = models.EmailField(max_length=30)
    addr =models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name','mobilePhone','mail','addr') #只显示model中指定的字段


class myEmail(models.Model):
    From = models.EmailField(max_length=200)
    To =  models.EmailField(max_length=200)
    Subject =models.CharField(max_length=100)
    Content =models.CharField(max_length=300)
    Type = models.IntegerField()  #  read  ,  unread , sent , unsend
    DateTime = models.DateTimeField('time', auto_now = True)

    def __unicode__(self):
        return self.Subject


class Emailaddress(models.Model):
    login_ip=models.CharField(max_length=20)
    user = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    pwd = models.CharField(max_length=200)
    emailtype = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.user


class Emailcontent(models.Model):
    subject=models.CharField(max_length=200)
    emailfrom=models.CharField(max_length=200)
    emaildate=models.CharField(max_length=200)
    content=models.TextField(max_length=2000)
    address=models.ForeignKey(Emailaddress,
    related_name='email_address')
    def __unicode__(self):
        return self.subject
