from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))
    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

def get_dealerships(request, state="All"):
    # We will simulate the dealership data since we don't have the microservice running
    dealerships = [
        {"id": 1, "city": "Dallas", "state": "Texas", "st": "TX", "address": "123 Main St", "zip": "75001", "lat": 32.7767, "long": -96.7970, "short_name": "Dallas Dealer", "full_name": "Dallas Car Dealership"},
        {"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Oak St", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "Wichita Dealer", "full_name": "Wichita Car Dealership"}
    ]
    if state != "All":
        dealerships = [d for d in dealerships if d['state'] == state or d['st'] == state]
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    # Simulated reviews
    reviews = [
        {"id": 1, "name": "John Doe", "dealership": dealer_id, "review": "Fantastic services", "purchase": True, "purchase_date": "01/01/2023", "car_make": "Audi", "car_model": "A4", "car_year": 2023, "sentiment": "positive"}
    ]
    return JsonResponse({"status": 200, "reviews": reviews})

def get_dealer_details(request, dealer_id):
    dealer = {"id": dealer_id, "city": "Dallas", "state": "Texas", "st": "TX", "address": "123 Main St", "zip": "75001", "lat": 32.7767, "long": -96.7970, "short_name": "Dallas Dealer", "full_name": "Dallas Car Dealership"}
    if dealer_id == 2:
        dealer = {"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Oak St", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "Wichita Dealer", "full_name": "Wichita Car Dealership"}
    return JsonResponse({"status": 200, "dealer": [dealer]})

@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

def analyzereview(request):
    text = request.GET.get('text')
    sentiment = "positive"
    if "bad" in text.lower():
        sentiment = "negative"
    return JsonResponse({"sentiment": sentiment})
