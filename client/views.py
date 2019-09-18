from django.shortcuts import redirect
from django.shortcuts import render
from django.template.context_processors import csrf

from .forms import UploadImgForm
from .models import Client, Sex, Citizenship, FamilyState, Children, City, Telephone, State, Skills


def client_main_page(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    return render(request=request,
                  template_name='client/client_main_page.html',
                  context=response)


def client_profile(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    return render(request=request,
                  template_name='client/client_profile.html',
                  context=response)


def client_edit_main(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'
    response['sex'] = Sex.objects.all()

    if request.method == 'POST':
        print('client_edit_main - request.POST')

        client = Client(
            name=request.POST['client_first_name'],
            lastname=request.POST['client_last_name'],
            patronymic=request.POST['client_middle_name'],
            sex=Sex(sex_word=request.POST['sex']),  # .save()
            date_born=request.POST['date_born'],
            citizenship=Citizenship(country_word=request.POST['citizenship']),  # .save()
            family_state=FamilyState(state_word=request.POST['family_state']),  # .save()
            children=Children(children_word=request.POST['children']),  # .save()
            country=Citizenship(country_word=request.POST['country']),  # .save()
            city=City(city_word=request.POST['city']),  # .save()
            street=request.POST['street'],
            house=request.POST['house'],
            flat=request.POST['flat'],
            telegram_link=request.POST['telegram_link'],
            skype=request.POST['skype_id'],
            email=request.POST['email'],
            link_linkedin=request.POST['link_linkedin'],
            state=State(state_word=request.POST['state']),  # .save()
        )
        # client.save()  # TODO uncomment after 'UserLogin' module done!!!

        tel = request.POST.getlist('phone')
        for t in tel:
            Telephone(telephone_number=t).save()

        print(
            request.POST['client_first_name'],
            request.POST['client_last_name'],
            request.POST['client_middle_name'],
            request.POST['sex'],
            request.POST['date_born'],
            request.POST['citizenship'],
            request.POST['family_state'],
            request.POST['children'],
            request.POST['country'],
            request.POST['city'],
            request.POST['street'],
            request.POST['house'],
            request.POST['flat'],
            request.POST.getlist('phone'),
            request.POST['telegram_link'],
            request.POST['skype_id'],
            request.POST['email'],
            request.POST['link_linkedin'],
            request.POST['state'],
        )

        print('client_edit_main - OK')

        return redirect(to='/client/profile')
    else:
        print('client_edit_main - request.GET')

    return render(request=request,
                  template_name='client/client_edit_main.html',
                  context=response)


def client_edit_skills(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("client_edit_skills - request.POST")

        skills_arr = request.POST.getlist('skill')
        print("skill: %s" % skills_arr)

        for s in skills_arr:
            skill = Client(skills=Skills(skills=s))  # Skill().save())
            # skill.save()  # TODO uncomment after 'UserLogin' module done!!!

        # form = AddSkillForm(request.POST)
        # response['form'] = form
        # if form.is_valid():
        #     form.save()

        return redirect(to='/client/edit')
    else:
        print('client_edit_skills - request.GET')
        # response['form'] = AddSkillForm()

    return render(request=request,
                  template_name='client/client_edit_skills.html',
                  context=response)


def client_edit_photo(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print('client_edit_photo - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        response['form'] = form

        if form.is_valid():
            # form.save()  # TODO uncomment after 'UserLogin' module done!!!
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        print('client_edit_photo - request.GET')
        response['form'] = UploadImgForm()

    return render(request=request,
                  template_name='client/client_edit_photo.html',
                  context=response)
