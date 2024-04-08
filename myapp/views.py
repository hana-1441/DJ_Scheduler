from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Data
from django.core import serializers
from datetime import datetime

# Create your views here.

@csrf_exempt # security token for POST method
def user_ip(request):   # function to take user i/p for prog lang and topic

    if request.method=="GET":
        data = serializers.serialize("json",Data.objects.all())
        return JsonResponse({'msg':"hey","data":json.loads(data)})

    if request.method=="POST":

        print(">>>>req payload : ",request.body)
        print(type(request.body)) # this got in byte format
        time_in=datetime.now().strftime("%H : %M : %S")
        body = json.loads(request.body.decode('utf-8')) # convert in JSON Formatted string 
        print(">>>>>>>>>>Body : ",body)
        try:
            # for single payload
            data = Data.objects.create(pl=body['pl'],topic=body['topic'],status="req accepted",time_in=time_in)
            s_data = serializers.serialize("json",(data,)) # query : why to send as list or tuple form ?
            return JsonResponse(s_data,safe=False)
        
        except:
            # for Multiple payload
            s_data=[]
            for i in body:
                data = Data.objects.create(pl=i['pl'],topic=i['topic'],status="req accepted",time_in=time_in)
                s_data.append(serializers.serialize("json",(data,))) # query : why to send as list or tuple form ?
            return JsonResponse(s_data,safe=False)