from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ContactForm
from .models import contact
from django.contrib.auth.models import User
from .SmsSender import sendSms
from os import getcwd
from .mail import send_mail
import sys
from sys import platform

import base64
import numpy as np
import cv2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import User
from . import bard

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_data(api_key, location, start_date, end_date):
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
        f"timeline/{location}/{start_date}/{end_date}"
        f"?unitGroup=metric&include=days&key={api_key}&contentType=json"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Weather API Error:", str(e))
        return None


# ================= INDEX =================
def index(request):
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        start_date = request.POST.get("date")
        end_date = request.POST.get("return")

        no_of_day = (
            datetime.strptime(end_date, "%Y-%m-%d") -
            datetime.strptime(start_date, "%Y-%m-%d")
        ).days

        if no_of_day < 0:
            messages.error(request, "Return date must be after start date.")
            return redirect("index")

        weather_data = get_weather_data(
            WEATHER_API_KEY, destination, start_date, end_date
        )

        if not weather_data:
            messages.error(request, "Unable to fetch weather data.")
            return redirect("index")

        plan = bard.generate_itinerary(
            source, destination, start_date, end_date, no_of_day
        )

        return render(request, "main_app/dashboard.html", {
            "weather_data": weather_data,
            "plan": plan
        })

    return render(request, "main_app/index.html")


# ================= TRANSLATE =================
def translate(request):
    translated_text = ""
    languages = GoogleTranslator().get_supported_languages(as_dict=True)

    if request.method == "POST":
        text = request.POST.get("text")
        src_lang = request.POST.get("src_lang")
        dest_lang = request.POST.get("dest_lang")

        try:
            translated_text = GoogleTranslator(
                source=src_lang,
                target=dest_lang
            ).translate(text)
        except:
            messages.error(request, "Translation failed")

    return render(request, "main_app/translate.html", {
        "translated_text": translated_text,
        "languages": languages
    })
# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'main_app/home.html', context)




def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created Successfully: {username}")
            login(request, user)
            messages.info(request, f"Logged in as {username}")
            return redirect('main_app:home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")

    form = UserCreationForm
    return render(request, 'main_app/register.html', context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main_app:home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username} !")
                return redirect("main_app:home")
            else:
                messages.error(request, f"Invalid username or password {username} ")
        else:
            messages.error(request, "Invausername or password  ")

    form = AuthenticationForm
    return render(request, "main_app/login.html", {'form': form})

def emergency_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr==0:
        return redirect("main_app:login")
    user = curr
    contacts = contact.objects.filter(user=user)
    total_contacts = contacts.count()
    context = {'contacts': contacts, 'total_contacts': total_contacts, 'user':user}

    return render(request, 'main_app/emergency_contact.html', context)


def create_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    inst = contact(user=curr)
    form = ContactForm(instance=inst)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.info(request, f"New contact created successfully!!")
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('email')
            message = "Hello, " + name + "\nYour contact information has been saved as emergency contact by " + curr.username + "."
            send_mail(mail, message)
            messages.info(request, f"An email has been sent to your contact!!")
            return redirect('main_app:emergency_contact')

        messages.error(request, f"Invalid username or password")
    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def update_contact(request, pk):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break

    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    form = ContactForm

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=curr_contact)
        if form.is_valid():
            form.save()
            messages.error(request, f"{name} updated successfully!!")
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('email')
            message = "Hello, " + name + "\nYour contact information as emergency contact by " + curr.username + " has been updated."
            send_mail(mail, message)
            messages.info(request, f"An email has been sent to your contact!!")

            return redirect('main_app:emergency_contact')

    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def delete_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    if request.method == "POST":
        curr_contact.delete()
        messages.error(request, f"{name} deleted successfully!!")
        return redirect('main_app:emergency_contact')

    context = {'item': curr_contact}
    return render(request, 'main_app/delete_contact.html', context)

def emergency(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr==0:
        return redirect("main_app:login")
    user = curr
    contacts = contact.objects.filter(user=user)
    emails = []
    for j in contacts:
        emails.append(j._meta.get_field("email"))
    name = user.username
    message = name+" is in emergency situation and need your help immediately!!"

    errors = ""
    try:
        sendSms("9790525051", message)
    except:
        errors += "Message not send to  9790525051"
        pass
    try:
        sendSms("7539915423", message)
    except:
        errors += "Message not send to 7539915423"
        pass

    for c in contacts:
        send_mail(c.email, message)

    admin = [["Vasanth", "9790525051"], ["Aakash", "7539915423"]]
    context = {'contacts':contacts, 'admin':admin, 'error':errors, 'emails':emails}

    return render(request, 'main_app/emergency.html', context)



def city_map(request):
    return render(request, 'main_app/city_map.html', {'title':'city_map'})

def find_me(request):
    return render(request, 'main_app/find_me.html', {'title':'current location'})


def helpline_numbers(request):
    return render(request, 'main_app/helpline_numbers.html', {'title': 'helpline_numbers'})

from django.core.files.storage import FileSystemStorage
from .violence import detect_violence, detect_frame_violence

def violent(request):
    if not request.user.is_authenticated:
        return redirect("main_app:login")

    if request.method == "POST":
        video = request.FILES.get("video")
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        video_path = fs.path(filename)

        violence, screenshot = detect_violence(video_path)


        if violence:
            request.session['violence_detected'] = True
            request.session['screenshot'] = screenshot
            messages.error(request, "⚠ Violence detected! Redirecting to live location...")
            return redirect("main_app:find_me")

            
        else:
            return render(request, "main_app/violent.html", {
                "message": " No violence detected in the video"
            })

    return render(request, "main_app/violent.html")

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMessage
from geopy.geocoders import Nominatim
from datetime import datetime
import json, os

@csrf_exempt
def send_location(request):

    print("✅ send_location() CALLED")  # DEBUG

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # DEBUG session
    print("🔥 SESSION:", dict(request.session.items()))

    # Must have violence flag
    if not request.session.get("violence_detected"):
        return JsonResponse({
            "status": "no_alert",
            "message": "Violence flag missing in session"
        }, status=200)

    try:
        data = json.loads(request.body)
        lat = data.get("lat")
        lng = data.get("lng")

        if lat is None or lng is None:
            return JsonResponse({
                "status": "error",
                "message": "Latitude/Longitude missing"
            }, status=400)

        # Reverse geo
        place = "Unknown location"
        try:
            geolocator = Nominatim(user_agent="women_safety_app")
            location = geolocator.reverse(f"{lat}, {lng}", timeout=10)
            if location:
                place = location.address
        except Exception as geo_err:
            print("❌ GEO ERROR:", geo_err)

        time_now = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        screenshot = request.session.get("screenshot")

        subject = "🚨 TOURIST SAFETY ALERT – VIOLENCE DETECTED"
        body = f"""
EMERGENCY ALERT 🚨

Violence detected by AI system.

📍 Latitude  : {lat}
📍 Longitude : {lng}

📌 Place:
{place}

🕒 Time:
{time_now}

🔗 Google Maps:
https://www.google.com/maps?q={lat},{lng}

-- 
Women Safety AI Monitoring System
"""

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=["aakashbabu75399@gmail.com"]
        )

        # Attach screenshot
        if screenshot and os.path.exists(screenshot):
            email.attach_file(screenshot)
            print("📸 Screenshot attached:", screenshot)
        else:
            print("⚠ Screenshot missing:", screenshot)

        email.send(fail_silently=False)

        print("✅ EMAIL SENT SUCCESSFULLY")

        # Clear session AFTER SUCCESS
        request.session["violence_detected"] = False
        request.session["screenshot"] = None
        request.session.modified = True

        return JsonResponse({
            "status": "success",
            "message": "Admin alerted successfully"
        }, status=200)

    except Exception as e:
        print(" SEND LOCATION ERROR:", e)
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64
import numpy as np
import cv2

from .violence import detect_frame_violence


@csrf_exempt
def live_detect(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            frame_data = data.get("frame")

            # Base64 → OpenCV
            img_bytes = base64.b64decode(frame_data.split(",")[1])
            img_bytes = base64.b64decode(frame_data.split(",")[1])
            nparr = np.frombuffer(img_bytes, np.uint8)

            if nparr.size == 0:
                return JsonResponse({"violence_detected": False, "frame": ""})

            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                return JsonResponse({"violence_detected": False, "frame": ""})


            violence_detected, frame_with_boxes, screenshot = detect_frame_violence(frame)

            # Save session ONLY ONCE
            if violence_detected and not request.session.get("violence_detected"):
                request.session["violence_detected"] = True
                request.session["screenshot"] = screenshot

            # OpenCV → Base64
            _, buffer = cv2.imencode(".jpg", frame_with_boxes)
            frame_base64 = base64.b64encode(buffer).decode("utf-8")

            return JsonResponse({
                "violence_detected": violence_detected,
                "frame": frame_base64
            })

        except Exception as e:
            print("LIVE DETECTION ERROR:", e)
            return JsonResponse({"error": "processing failed"}, status=500)

    return JsonResponse({"error": "invalid request"}, status=400)


def live_camera(request):
    if not request.user.is_authenticated:
        return redirect("main_app:login")
    return render(request, "main_app/live_camera.html")


from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def test_email(request):
    send_mail(
        "TEST EMAIL",
        "Email system working",
        settings.EMAIL_HOST_USER,
        [" aakashbabu75399@gmail.com"],
        fail_silently=False
    )
    return HttpResponse("Email sent")