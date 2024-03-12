from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.conf import settings
import os

import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()





def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)



@csrf_exempt
def emailscan(request):
    
    tfidf = pickle.load(open(os.path.join(settings.BASE_DIR,'vectorizer.pkl'),'rb'))
    model = pickle.load(open(os.path.join(settings.BASE_DIR,'model.pkl'),'rb'))
    if request.method == 'POST':
        # Parse JSON data from request body
        data = json.loads(request.body)
        # Access the 'mail' key from the parsed data
        mail = data.get('mail')
        mail = (mail.replace('\n',' '))
        mail = ' '.join(mail.split(' '))
        print(mail)
        transformed_sms = transform_text(mail)
    # 2. vectorize
        vector_input = tfidf.transform([transformed_sms])
        # 3. predict
        result = model.predict(vector_input)[0]
        print(result)
        # Return JSON response with the received email
        return JsonResponse({'result': str(result)})
    
    return JsonResponse({'message': False})