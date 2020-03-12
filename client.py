import sys
import requests
import json

def register(url):
    url = url+"register/"
    r = requests.get(url)
    result = json.loads(r.content)["Result"]

    username = result["username"]
    email = result["email"]

    print("Username: {}\nEmail: {}".format(username, email))

def login(url):
    url = url+"login/"
    r = requests.get(url)
    result = json.loads(r.content)["Result"]
    username = result["username"]
    print("Username: {}".format(username))

def logout(url):
    url = url + "logout/"
    r = requests.get(url)
    result = json.loads(r.content)["Result"]
    username = result["username"]
    print("User {} logged out".format(username))


def list(url):
    url = url + "list/"
    r = requests.get(url)

    result = json.loads(r.content)["Result"]

    print("{:^20}{:^30}{:^20}{:^20}{:^20}".format("Code", "Name", "Year", "Semester", "Taught by"))
    for list in result:
        print("{:^20}{:^30}{:^20}{:^20}".format(list["Code"], list["Name"], list["Year"], list["Semester"]), end="")
        prof_list = list["Taught by"]
        for i in range(len(prof_list)):
            prof = prof_list[i]
            if i == 0:
                print("{:^20}".format(prof[0] + ", " + prof[1]))
            else:
                print(" " * 90 + "{:^20}".format(prof[0] + ", " + prof[1]))

def view(url):
    url = url + "view/"
    r = requests.get(url)
    result = json.loads(r.content)["Result"]

    for list in result:
        print("The rating of Professor {} ({}) is {}".format(list["Name"], list["ID"], list["Score"]))


def average(url, professor_id, module_code):
    url = url + "average/"
    parameter = {"professor_id": professor_id, "module_code": module_code}
    r = requests.post(url, json=parameter)
    result = json.loads(r.content)["Result"]

    professor_name = result["professor_name"]
    professor_id = result["professor_id"]
    module_name = result["module_name"]
    module_code = result["module_code"]
    average = result["average"]

    print("The rating of Professor {} ({}) in module {} ({}) is {}".format(professor_name, professor_id, module_name,
                                                                           module_code, average))


def rate(url, professor_id, module_code, module_year, module_semester, rate_score):
    url = url + "rate/"

    parameter = {"professor_id": professor_id, "module_code": module_code,
                 "module_year": module_year, "module_semester": module_semester,
                 "rate_score": rate_score}
    r = requests.post(url, json=parameter)
    result = json.loads(r.content)["Result"]

    professor_name = result["professor_name"]
    professor_id = result["professor_id"]
    module_name = result["module_name"]
    module_code = result["module_code"]
    module_year = result["module_year"]
    module_semester = result["module_semester"]
    rate_score = result["rate_score"]

    print("professor_name: {}\nprofessor_id: {}\nmodule_name: {}\nmodule_code: {}\n"
          "module_year: {}\nmodule_semester: {}\nrate_score: {}".format(
            professor_name, professor_id, module_name, module_code, module_year, module_semester, rate_score))


if __name__ == '__main__':
    url = "http://127.0.0.1:8000/"
    if len(sys.argv)==2:
        if sys.argv[1] == 'register':
            register(url)
        elif sys.argv[1] == 'logout':
            logout(url)
        elif sys.argv[1] == 'list':
            list(url)
        elif sys.argv[1] == 'view':
            view(url)
    elif len(sys.argv)==3:
        login(url)
    elif len(sys.argv)==4:
        professor_id = sys.argv[2]
        module_code = sys.argv[3]
        average(url, professor_id, module_code)
    elif len(sys.argv)==7:
        professor_id = sys.argv[2]
        module_code = sys.argv[3]
        year = int(sys.argv[4])
        semester = int(sys.argv[5])
        rating = int(sys.argv[6])
        rate(url, professor_id, module_code, year, semester, rating)