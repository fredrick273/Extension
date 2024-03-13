from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse,HttpResponse
from django.conf import settings
import os
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

import pickle
from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import urllib
import urllib.request
from datetime import datetime
import requests
import numpy as np
import whois
import tldextract
import string
import datetime
from dateutil.relativedelta import relativedelta
from csv import reader

from web3 import Web3

from .models import secretkeys,UserSubscription,codes

ps = PorterStemmer()

model = pickle.load(open(os.path.join(settings.BASE_DIR,'SVM_Model.pkl'), 'rb'))

# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
  index = url.find("://")
  split_url = url[index+3:]
  index = split_url.find("/")
  split_url = split_url[:index]
  split_url = split_url.replace(".", "")
  counter_hex = 0
  for i in split_url:
    if i in string.hexdigits:
      counter_hex +=1
  total_len = len(split_url)
  having_IP_Address = 0
  if counter_hex >= total_len:
    having_IP_Address = 1
  return having_IP_Address

# 3.Checks the presence of @ in URL (Have_At)
sc=['@','~','`','!', '$','%','&']
def haveAtSign(url):
  flag=0
  for i in range(len(sc)):
    if sc[i] in url:
      at = 1
      flag=1
      break
  if flag==0:
    at = 0
  return at

# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
  if len(url) < 54:
    length = 0
  else:
    length = 1
  return length

# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0

# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0

#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0

# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate



# 11.DNS Record availability (DNS_Record)
# obtained in the featureExtraction function itself

# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
      extract_res = tldextract.extract(url)
      url_ref = extract_res.domain + "." + extract_res.suffix
      html_content = requests.get("https://www.alexa.com/siteinfo/" + url_ref).text
      soup = BeautifulSoup(html_content, "lxml")
      value = str(soup.find('div', {'class': "rankmini-rank"}))[42:].split("\n")[0].replace(",", "")
      if not value.isdigit():
        return 1
      value = int(value)
      if value < 100000:
        return 0
      else:
        return 1
    except:
        return 1

# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)
def domainAge(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  try:
    whois_res = whois.whois(url)
    if datetime.datetime.now() > whois_res["creation_date"][0] + relativedelta(months=+6):
      return 0
    else:
      return 1
  except:
    return 1

# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
      try:
        expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
      except:
        end=1
  if (expiration_date is None):
      end=1
  elif (type(expiration_date) is list):
      today = datetime.datetime.now()
      domainDate = abs((expiration_date[0] - today).days)
      if ((domainDate/30) < 6):
        end = 1
      else:
        end=0
  else:
      today = datetime.datetime.now()
      domainDate = abs((expiration_date - today).days)
      if ((domainDate/30) < 6):
        end = 1
      else:
        end=0
  return end

# 15. IFrame Redirection (iFrame)
def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1

# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0

# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

#16. Extra feature checks url exists in popular websites data
def checkCSV(url):
  flag=0
  try:
    checkURL=urlparse(url).netloc
  except:
    return 1
  with open(os.path.join(settings.BASE_DIR,'Web_Scrapped_websites.csv'), 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        if row[0]==checkURL:
            flag=0
            break
        else:
            flag=1
  if flag==0:
      return 0
  else:
      return 1

def featureExtraction(url):

  features = []
  #Address bar based features (10)
  #features.append(getDomain(url))
  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))

  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(url))
  features.append(1 if dns == 1 else domainEnd(domain_name))

  # HTML & Javascript based features
  try:
    response = requests.get(url)
  except:
    response = ""

  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(forwarding(response))

  return features




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


@csrf_exempt
def philurl(request):
   if request.method == 'POST':
        data = json.loads(request.body)
        # Access the 'mail' key from the parsed data
        url = data.get('url')
        print(url)
        # 
        api_key = '0215385173ea37b8fa8c006be27e61b5176998f86413ae62a6a2added4ad0a57'  # Replace 'YOUR_API_KEY' with your VirusTotal API key
        headers = {'x-apikey': api_key}
        data = {'url': url}
        response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data=data)
        if response.status_code == 200:
            result = response.json()

            analysis = requests.get(result['data']['links']['self'],headers=headers)
            analysis = (analysis.json())

            harmless_count = 0
            malicious_count = 0

            # Iterate through each engine's analysis result
            for engine, result in analysis['data']['attributes']['results'].items():
                category = result['category']
                verdict = result['result']
                if category == 'harmless' and verdict == 'clean':
                    harmless_count += 1
                elif category != 'harmless' or verdict != 'clean':
                    malicious_count += 1

            # Determine overall result based on counts
            if malicious_count > 0:
                print("phishing site",url)
                return JsonResponse({'result': "1"})
            
            
   return JsonResponse({'result': "1"})

mids = set()  # Initialize an empty set to store extension IDs

# Read extension IDs from the CSV file and store them in the set
with open(os.path.join(settings.BASE_DIR, 'mlist.csv'), 'r') as f:
    for line in f:
        # Append each line to the set after stripping newline characters
        mids.add(line.strip())

@csrf_exempt
def extension(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Access the 'id' key from the parsed data
        id = data.get('id')
        print(id)
        if id in mids:
            print(id)
            return JsonResponse({'result': "-1"})  # ID found in the set
    return JsonResponse({'result': "1"})  # ID not found in the set or invalid request



API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjdlZjlhY2UwLWUxYjAtNGRkYS1iZWEyLTk3MmRiZmE0NmUzYyIsIm9yZ0lkIjoiMzgyNTM2IiwidXNlcklkIjoiMzkzMDU5IiwidHlwZUlkIjoiZDAyN2E1NmYtMjcyZi00Y2JlLWIzZDktOGQzYTU5ZGEzMzA3IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTAyOTg3NzAsImV4cCI6NDg2NjA1ODc3MH0.B_DiZcYt5TTYEZBjXpbwpNyhuDmHw3dg5Xh7eQEbUwo'
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit
def moralis_auth(request):
    return render(request, 'login.html', {})
def my_profile(request):
    return render(request, 'profile.html', {})
def request_message(request):
    data = json.loads(request.body)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": "2025-01-01T00:00:00.000Z",
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})
    return JsonResponse(json.loads(x.text))
def verify_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    
    if x.status_code == 201:
        response_data = json.loads(x.text)
        print(response_data)
        eth_address = response_data.get('address')

        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            # Create a new instance of secretkeys model to store the secret key
            c = codes.objects.last()
            c.user = user
            c.save()

            s = UserSubscription(user = user)
            s.save()

        if user is not None:
            if user.is_active:
                # Log in the user after successful verification
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = response_data
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))
    

def transact(request,id):
   return render(request, 'transact.html',context={'id':id})

def subscribe(request,id):
   c = get_object_or_404(codes,id=id)
   s = UserSubscription.objects.get(user= c.user)
   s.issubscibed = True
   s.save()
   return HttpResponse("Subscribed")


@csrf_exempt
def gencode(request):
   l = len(codes.objects.all()) + 1
   c = codes(id = l)
   c.save()
   return JsonResponse({'code':str(l)})


@csrf_exempt
def usersub(request,id):
   c = get_object_or_404(codes,id=id)
   s = UserSubscription.objects.get(user= c.user)
   return JsonResponse({'result':s.issubscibed})