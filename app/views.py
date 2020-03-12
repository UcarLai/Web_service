from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from  django.contrib.auth import login as auth_login
from  django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Professor, Module, Rate
from django.db.models import Q, Avg

def register(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'GET'):
        http_bad_response = 'Only GET requests are allowed for this resource\n'
        return http_bad_response


    username = input("Please input username: ")
    email = input("Please input email: ")
    password = input("Please input password: ")

    same_user = User.objects.filter(username=username)
    while same_user:
        print("The user exists!")
        username = input("Please input username: ")
        email = input("Please input email: ")
        password = input("Please input password: ")
        same_user = User.objects.filter(username=username)

    user = User.objects.create_user(username, email, password)

    the_list = {"username":username, "email":email}

    payload = {'Result': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

def login(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'GET'):
        http_bad_response = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    the_list = {"username": username}

    payload = {'Result': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

def logout(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'GET'):
        http_bad_response = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    payload = {'Result': {"username": user.username}}

    auth_logout(request)


    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

def list(request):
    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type']='text/plain'

    if(request.method!='GET'):
        http_bad_response='Only GET requests are allowed for this resource\n'
        return http_bad_response

    module_list = Module.objects.all()
    the_list = []
    for module in module_list:
        item = {"Code":module.module_code, "Name":module.module_name,
                "Year":module.module_year, "Semester":module.module_semester}
        prof_list = []
        for professor in module.module_taughtby.all():
            prof_list.append([professor.professor_id, professor.professor_name])
        item["Taught by"]=prof_list
        the_list.append(item)
    payload = {'Result':the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type']='application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

def view(request):
    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'GET'):
        http_bad_response = 'Only GET requests are allowed for this resource\n'
        return http_bad_response

    rate_list = Rate.objects.values('rate_professor').annotate(avg=Avg('rate_score'))

    the_list = []
    for rate in rate_list:
        prof = Professor.objects.get(id=rate['rate_professor'])
        score = int(rate['avg']+0.5)
        item = {"Name": prof.professor_name, "ID": prof.professor_id,
                "Score": score}
        the_list.append(item)
    payload = {'Result': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

@csrf_exempt
def average(request):
    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    params = json.loads(request.body)
    professor_id = params["professor_id"]
    module_code = params["module_code"]

    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'POST'):
        http_bad_response = 'Only POST requests are allowed for this resource\n'
        return http_bad_response


    select = Rate.objects.filter(Q(rate_professor__professor_id=professor_id) & Q(rate_module__module_code=module_code))
    select_list = select.values('rate_professor__professor_id', 'rate_module__module_code').annotate(avg=(Avg('rate_score')))[0]
    professor = Professor.objects.filter(professor_id=professor_id)[0]
    module = Module.objects.filter(module_code=module_code)[0]
    rate_list = {"professor_name":professor.professor_name, "professor_id":professor.professor_id,
     "module_name":module.module_name, "module_code":module_code, "average":int(select_list['avg']+0.5)}

    payload = {'Result': rate_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

@csrf_exempt
def rate(request):
    username = input("Please input username: ")
    password = input("Please input password: ")
    user = authenticate(request, username=username, password=password)
    while user is None:
        print("The user not exists!")
        username = input("Please input username: ")
        password = input("Please input password: ")
        user = authenticate(request, username=username, password=password)

    auth_login(request, user)

    params = json.loads(request.body)
    professor_id = params["professor_id"]
    module_code = params["module_code"]
    module_year = params["module_year"]
    module_semester = params["module_semester"]
    rate_score = params["rate_score"]
    user = User.objects.all()[0]

    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if (request.method != 'POST'):
        http_bad_response = 'Only POST requests are allowed for this resource\n'
        return http_bad_response

    professor = Professor.objects.filter(professor_id=professor_id)[0]
    module = Module.objects.filter(Q(module_code=module_code) & Q(module_year=module_year) & Q(module_semester=module_semester))[0]

    Rate.objects.create(rate_user=user, rate_module=module, rate_professor=professor, rate_score=rate_score)

    rate_list = {"professor_name": professor.professor_name, "professor_id": professor.professor_id, "module_name": module.module_name,
                 "module_code": module.module_code, "module_year": module.module_year, "module_semester": module.module_semester, "rate_score":rate_score}

    payload = {'Result': rate_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'Created'
    return http_response