import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from wit_files import wit_speech
import json
from gtts import gTTS
import playsound
from django.db import connection

# Create your views here.

def home(request):
    return render(request, 'index.html')       

def mic(request):
    text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
    id_list = ['new_products_id','laptops_id','mobiles_id','header_id','cameras_id','special_deal_id']
    try:
        entity = text['entities']
        section = entity['scroll_section:scroll_section'][0]
        id_ref = section['value']
        if id_ref in id_list:
            final_id = "#" + id_ref
            return redirect(reverse('home')+ final_id)

        elif id_ref == 'cart_id':
            data1 = json.dumps({1:2})
            return render(request, 'index.html', {'data1':data1})
        else:
            data = json.dumps({1:2})
            return render(request, 'index.html', {'data':data})
            
    except:
        data = json.dumps({1:2})
        return render(request, 'index.html', {'data':data})

def mic_con(request):
    cat = request.POST['cat']
    item = request.POST['item']
    try:
        text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
        entity = text['entities']
        section = entity['mobile_query:mobile_query'][0]
        column = section['value']
        column = str(column)
        cursor = connection.cursor()
        query = f'select {column} from home_{cat} where name = "{item}"'
        cursor.execute(query)
        rows = cursor.fetchone()
        if rows:
            message = gTTS(text=rows[0], lang='en', slow=False)
            message.save("wit_response.mp3")
            playsound.playsound("wit_response.mp3")
            return render(request, 'view.html')
        else:
            data = json.dumps({1:2})
            return render(request, 'view.html', {'data':data})
        
    except:
        data = json.dumps({1:2})
        return render(request, 'view.html', {'data':data}) 

def product(request):
    return render(request, 'view.html')

