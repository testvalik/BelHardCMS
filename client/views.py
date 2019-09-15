from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import csrf


def client_main_page(request):
    response = csrf(request)

    response['client'] = 'client/img/user_1.png'

    return render(request, 'client/client_main_page.html', response)


def client_profile(request):
    response = csrf(request)

    response['client'] = 'client/img/user_1.png'

    return render(request, 'client/client_profile.html', response)


def client_edit(request):
    response = csrf(request)

    response['client'] = 'client/img/user_1.png'

    return render(request, 'client/client_edit_main.html', response)


def save_client_edit_main(request):
    if request.POST:
        print("save_client_edit_main - request POST")

    return redirect('/client/profile')
