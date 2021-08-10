from typing import ValuesView
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Attribute, Food
from django.db import connection
import numpy
from rest_framework import serializers, viewsets
from .models import App
from .serializer import AppSerializer

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializers_class = AppSerializer

def index(request):
    return render(request,'delivery_main/index.html')

def recommand(request):
    keyword = request.GET['keyword']
    try:
        cursor = connection.cursor()
        sql = "select name, path, frequency, good, bad, food.fno from food, attribute where food.fno = attribute.fno and sense = %(sense)s"
        cursor.execute(sql, {'sense' : keyword})
        result_data = cursor.fetchall()
        connection.commit()
        connection.close()
        data_list = []
        probality = []
        result_sum = 0
        for food in result_data:
            result_sum = result_sum + food[2] + food[3] - food[4]
        for food in result_data:
            row = {'name' : food[0], 'path' : '/static/images/' + food[1], 'frequency' : food[2], 'good' : food[3], 'bad' : food[4], 'fno' : food[5], 'probality' : (food[2] + food[3] - food[4])/result_sum}
            data_list.append(row)
        for food in data_list:
            probality.append(food['probality'])
        if len(result_data) > 3:
            data_result_choice = numpy.random.choice(data_list, 3, replace=False, p=probality)
        elif len(result_data) > 0:
            data_result_choice = numpy.random.choice(data_list, len(data_list), replace=False, p=probality)
        else :
            data_result_choice = numpy.random.choice(data_list)
    except:
        connection.rollback()
        print("failed selecting in database")
    return render(request, 'delivery_main/recommand.html', {"list" : data_result_choice, "keyword" : keyword})

def good(request):
    if request.method == 'POST':
        fno = request.POST['fno']
        sense = request.POST['sense']
        try:
            cursor = connection.cursor()
            sql = "update attribute set good = good + 1 where sense = %s and fno = %s"
            cursor.execute(sql, (sense, fno))
            connection.commit()
            connection.close()
        except:
            connection.rollback()
            print("failed updating in database")
        return HttpResponseRedirect('/recommand/?keyword=' + request.POST['sense'])

def bad(request):
    if request.method == 'POST':
        fno = request.POST['fno']
        sense = request.POST['sense']
        try:
            cursor = connection.cursor()
            sql = "update attribute set bad = bad + 1 where sense = %s and fno = %s"
            cursor.execute(sql, (sense, fno))
            connection.commit()
            connection.close()
        except:
            connection.rollback()
            print("failed updating in database")
        return HttpResponseRedirect('/recommand/?keyword=' + request.POST['sense'])