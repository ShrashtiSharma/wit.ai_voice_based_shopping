import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from wit_files import wit_speech
from gtts import gTTS
import playsound
from django.db import connection

# Create your views here.

def home(request):
    return render(request, 'index.html')

def mic(request):
    text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
    id_list = ['new_products_id', 'laptops_id', 'mobiles_id', 'header_id', 'cameras_id', 'special_deal_id']

    try:
        entity = text.get('entities', {})
        section = entity.get('scroll_section:scroll_section', [{}])[0]  # Use get to avoid KeyError
        id_ref = section.get('value')

        if id_ref in id_list:
            final_id = "#" + id_ref
            return redirect(reverse('home') + final_id)
        elif id_ref == 'cart_id':
            data1 = json.dumps({1: 2})
            return render(request, 'index.html', {'data1': data1})
        else:
            data = json.dumps({1: 2})
            return render(request, 'index.html', {'data': data})
            
    except Exception as e:  # Catch specific exceptions if possible
        print(f"Error in mic view: {e}")  # Log the error for debugging
        data = json.dumps({1: 2})
        return render(request, 'index.html', {'data': data})

def mic_con(request):
    cat = request.POST.get('cat')
    item = request.POST.get('item')

    if not cat or not item:  # Validate inputs
        return render(request, 'view.html', {'data': json.dumps({"error": "Invalid category or item"})})

    try:
        text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
        entity = text.get('entities', {})
        section = entity.get('mobile_query:mobile_query', [{}])[0]
        column = section.get('value')

        cursor = connection.cursor()
        query = f'SELECT {column} FROM home_{cat} WHERE name = %s'  # Use parameterized queries to prevent SQL injection
        cursor.execute(query, [item])  # Use a list to pass parameters
        rows = cursor.fetchone()

        if rows:
            message = gTTS(text=rows[0], lang='en', slow=False)
            message.save("wit_response.mp3")
            playsound.playsound("wit_response.mp3")
            return render(request, 'view.html')
        else:
            return render(request, 'view.html', {'data': json.dumps({"error": "No data found"})})
        
    except Exception as e:
        print(f"Error in mic_con view: {e}")
        return render(request, 'view.html', {'data': json.dumps({"error": "An error occurred"})})

def product(request):
    return render(request, 'view.html')
