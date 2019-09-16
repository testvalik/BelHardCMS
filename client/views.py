from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import csrf


def client_main_page(request):
    response = csrf(request)

    response['client_img'] = 'client/img/user_1.png'

    return render(request, 'client/client_main_page.html', response)


def client_profile(request):
    response = csrf(request)

    response['client_img'] = 'client/img/user_1.png'

    return render(request, 'client/client_profile.html', response)


def client_edit_main(request):
    response = csrf(request)

    response['client_img'] = 'client/img/user_1.png'

    return render(request, 'client/client_edit_main.html', response)


def save_client_edit_main(request):
    if request.POST:
        print("save_client_edit_main - request POST")

    return redirect('/client/profile')


def client_edit_skills(request):
    response = csrf(request)

    response['client_img'] = 'client/img/user_1.png'

    return render(request, 'client/client_edit_skills.html', response)


def save_client_edit_skills(request):
    if request.POST:
        print("save_client_edit_skills - request POST")
        skill_1 = request.POST['skill_1']
        print("skill_1: %s" % skill_1)

    return redirect('/client/edit')
