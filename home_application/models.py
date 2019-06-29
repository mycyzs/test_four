# -*- coding: utf-8 -*-

from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=30,null=True)
    type = models.CharField(max_length=30,null=True)
    status = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=30,null=True)
    biz_name = models.CharField(max_length=30,null=True)
    owner = models.CharField(max_length=30,null=True)
    when_created = models.CharField(max_length=64,null=True)
    phone = models.CharField(max_length=30, null=True)
    title = models.CharField(max_length=30, null=True)


class Server(models.Model):
    host = models.ForeignKey(Host)
    name = models.CharField(max_length=30,null=True)
    depart = models.CharField(max_length=30,null=True)
    score = models.CharField(max_length=30,null=True)
    result = models.CharField(max_length=30,null=True)
    comment = models.CharField(max_length=120,null=True)