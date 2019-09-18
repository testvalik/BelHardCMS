from django.shortcuts import redirect
from django.shortcuts import render
from django.template.context_processors import csrf

from .forms import UploadImgForm
from .models import Client, Sex, Citizenship, FamilyState, Children, City, Telephone, State, Skills


def client_main_page(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    return render(request, 'client/client_main_page.html', response)


def client_profile(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    return render(request, 'client/client_profile.html', response)


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
            sex=Sex(sex_word=request.POST['sex']),
            date_born=request.POST['date_born'],
            citizenship=Citizenship(country_word=request.POST['citizenship']),
            family_state=FamilyState(state_word=request.POST['family_state']),
            children=Children(children_word=request.POST['children']),
            country=Citizenship(country_word=request.POST['country']),
            city=City(city_word=request.POST['city']),
            street=request.POST['street'],
            house=request.POST['house'],
            flat=request.POST['flat'],
            telegram_link=request.POST['telegram_link'],
            skills_id=request.POST['skills_id'],
            email=request.POST['email'],
            link_linkedin=request.POST['link_linkedin'],
            state=State(state_word=request.POST['state']),
        )
        # client.save()     # TODO uncomment after 'UserLogin' module done!!!

        Telephone(telephone_number=request.POST['phone'])
        # .save()   # TODO uncomment after 'UserLogin' module done!!!

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
            request.POST['phone'],
            request.POST['telegram_link'],
            request.POST['skills_id'],
            request.POST['email'],
            request.POST['link_linkedin'],
            request.POST['state'],
        )

        print('client_edit_main - OK')

        return redirect('/client/profile')
    else:
        print('client_edit_main - request.GET')

    return render(request, 'client/client_edit_main.html', response)


def client_edit_skills(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    if request.POST:
        print("save_client_edit_skills - request.POST")

        skill = Skills(skills=request.POST['skill_1'])
        # skill.save()      # TODO uncomment after 'UserLogin' module done!!!

        print("skill: %s" % request.POST['skill_1'])

        return redirect('/client/edit')
    else:
        print('client_edit_skills - request.GET')

    return render(request, 'client/client_edit_skills.html', response)


def client_edit_photo(request):
    response = csrf(request)

    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        response['form'] = form

        # uploaded_file = request.FILES['photo']
        # fs = FileSystemStorage()
        # file = fs.save(uploaded_file.name, uploaded_file)
        # file_url = fs.url(file)
        # response['file_url'] = file_url

        if form.is_valid():
            # form.save()       # TODO uncomment after 'UserLogin' module done!!!
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        response['form'] = UploadImgForm()

    return render(request=request,
                  template_name='client/client_edit_photo.html',
                  context=response)
