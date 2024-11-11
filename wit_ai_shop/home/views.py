import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from wit_files import wit_speech
from gtts import gTTS
import playsound
from django.db import connection
import traceback

# Home view
def home(request):
    print("Rendering home view")  # Debug print
    return render(request, 'index.html')

# Mic view (handles speech recognition for navigation)
def mic(request):
    print("Mic view called")  # Debug print

    try:
        # Recognize speech and log the result for debugging
        text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
        print("Recognized speech data:", text)  # Debug print

        # Check if the API response contains an error
        if 'error' in text:
            print(f"Error from Wit.ai API: {text['error']}")  # Debug print
            return render(request, 'index.html', {'data': json.dumps({"error": text['error']})})

        # List of valid section IDs
        id_list = ['new_products_id', 'laptops_id', 'mobiles_id', 'header_id', 'cameras_id', 'special_deal_id']
        
        # Extract entities from the recognized text
        entity = text.get('entities', {})
        print("Extracted entities:", entity)  # Debug print

        # Extract the scroll section ID
        section = entity.get('scroll_section:scroll_section', [{}])
        print("Extracted section data:", section)  # Debug print

        if section and len(section) > 0:
            id_ref = section[0].get('value')
            print("Detected section ID:", id_ref)  # Debug print
        else:
            id_ref = None
            print("No section ID detected")  # Debug print

        # Handling redirection or providing a response
        if id_ref in id_list:
            final_id = "#" + id_ref
            print(f"Redirecting to section: {final_id}")  # Debug print
            return redirect(reverse('home') + final_id)
        elif id_ref == 'cart_id':
            print("Redirecting to cart section")  # Debug print
            data1 = json.dumps({1: 2})
            return render(request, 'index.html', {'data1': data1})
        else:
            print("Unrecognized ID reference, sending default response")  # Debug print
            data = json.dumps({1: 2})
            return render(request, 'index.html', {'data': data})

    except Exception as e:
        print(f"Error in mic view: {e}")  # Debug print
        traceback.print_exc()
        data = json.dumps({"error": "An error occurred during voice command processing"})
        return render(request, 'index.html', {'data': data})

# Mic control view (handles database queries based on speech commands)
def mic_con(request):
    print("Mic control view called")  # Debug print

    cat = request.POST.get('cat')
    item = request.POST.get('item')
    print(f"Received POST data - Category: {cat}, Item: {item}")  # Debug print

    if not cat or not item:
        print("Invalid category or item received")  # Debug print
        return render(request, 'view.html', {'data': json.dumps({"error": "Invalid category or item"})})

    try:
        text = wit_speech.RecognizeSpeech('myspeech.wav', 4)
        print("Recognized speech data:", text)  # Debug print

        if 'error' in text:
            print(f"Error from Wit.ai API: {text['error']}")  # Debug print
            return render(request, 'view.html', {'data': json.dumps({"error": text['error']})})

        entity = text.get('entities', {})
        print("Extracted entities:", entity)  # Debug print

        section = entity.get('mobile_query:mobile_query', [{}])
        if section and len(section) > 0:
            column = section[0].get('value')
            print(f"Recognized column: {column}, Item: {item}")  # Debug print
        else:
            print("Column not recognized properly")  # Debug print
            return render(request, 'view.html', {'data': json.dumps({"error": "Invalid column detected"})})

        cursor = connection.cursor()
        query = f'SELECT {column} FROM home_{cat} WHERE name = %s'
        print(f"Executing query: {query} with item: {item}")  # Debug print
        cursor.execute(query, [item])
        rows = cursor.fetchone()

        if rows:
            print(f"Data retrieved from database: {rows[0]}")  # Debug print
            message = gTTS(text=rows[0], lang='en', slow=False)
            message.save("wit_response.mp3")
            playsound.playsound("wit_response.mp3")
            return render(request, 'view.html')
        else:
            print(f"No data found for item: {item}, column: {column}")  # Debug print
            return render(request, 'view.html', {'data': json.dumps({"error": "No data found"})})

    except Exception as e:
        print(f"Error in mic_con view: {e}")  # Debug print
        traceback.print_exc()
        return render(request, 'view.html', {'data': json.dumps({"error": "An error occurred"})})

# Product view
def products_view(request):
    print("Rendering products view")  # Debug print
    return render(request, 'view.html')

# Product details view
def product(request):
    print("Rendering product details view")  # Debug print
    return render(request, 'view.html')
