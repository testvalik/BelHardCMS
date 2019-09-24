import logging
import re

from django.shortcuts import redirect, render
from django.template.context_processors import csrf

from BelHardCRM.settings import MEDIA_URL
from .forms import UploadImgForm, AddEducationFormSet
from .models import *


def client_main_page(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    return render(request=request, template_name='client/client_main_page.html', context=response)


def client_profile(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    return render(request=request, template_name='client/client_profile.html', context=response)


def client_edit_main(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print('client_edit_main - request.POST')

        client_first_name = request.POST['client_first_name'].title()
        date = request.POST['date_born']

        client = Client(
            user_client=request.user,
            name=request.POST['client_first_name'].title(),  # вАленТиН -> Валентин
            lastname=request.POST['client_last_name'].title(),
            patronymic=request.POST['client_middle_name'].title(),
            sex=Sex(sex_word=request.POST['sex']).save(),
            date_born=date if date else None,
            citizenship=Citizenship(country_word=request.POST['citizenship']).save(),
            family_state=FamilyState(state_word=request.POST['family_state']).save(),
            children=Children(children_word=request.POST['children']).save(),
            country=Citizenship(country_word=request.POST['country']).save(),
            city=City(city_word=request.POST['city']).save(),
            street=request.POST['street'],
            house=request.POST['house'],
            flat=request.POST['flat'],
            telegram_link=request.POST['telegram_link'],
            skype=request.POST['skype_id'],
            email=request.POST['email'],
            link_linkedin=request.POST['link_linkedin'],
            state=State(state_word=request.POST['state']).save(),
        )
        # client.save()

        cl = Client.objects.get(user_client=request.user)
        cl.name = client_first_name
        cl.save()

        tel = request.POST.getlist('phone')
        for t in tel:
            if re.match("^[+][0-9]{1,20}$", string=t):
                print("phone to save: %s" % t)

                phone = Telephone(telephone_number=t)
                phone.client = cl
                phone.save()
            else:
                print("incorrect phone number")

        print(
            request.POST['client_first_name'].title(),
            request.POST['client_last_name'].title(),
            request.POST['client_middle_name'].title(),
            request.POST['sex'],
            date,
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

    return render(request=request, template_name='client/client_edit_main.html', context=response)


def client_edit_skills(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print("client_edit_skills - request.POST")

        skills_arr = request.POST.getlist('skill')
        print("skill: %s" % skills_arr)

        for s in skills_arr:
            if s:
                skill = Skills(skills=s)
                skill.save()

                """ОБЪЕДИНЕНИЕ модуля Навыки с конкретным залогиненым клиентом!!!"""
                client = Client.objects.get(user_client=request.user)
                client.skills = skill
                client.save()

        return redirect(to='/client/edit')
    else:
        print('client_edit_skills - request.GET')

    return render(request=request, template_name='client/client_edit_skills.html', context=response)


def client_edit_photo(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print('client_edit_photo - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img')
            client = Client.objects.get(user_client=request.user)
            client.img = img
            client.save()
            """
            в БД сохраняется УНИКАЛЬНОЕ имя картинки (пр. user_2_EntrmQR.png)
            в папке MEDIA_URL = '/media/'
            """
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        print('client_edit_photo - request.GET')
        response['form'] = UploadImgForm()

    return render(request=request, template_name='client/client_edit_photo.html', context=response)


def client_edit_cv(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        cv = CV(
            position=request.POST['position'],
            time_job=TimeJob(time_job_word=request.POST['time_job']).save(),
            salary=request.POST['salary'],
            type_salary=TypeSalary(type_word=request.POST['type_salary']).save(),
        )
        cv.save()

        print(
            request.POST['position'],
            request.POST['time_job'],
            request.POST['salary'],
            request.POST['type_salary']
        )

        return redirect(to='/client/edit')

    return render(request, 'client/client_edit_cv.html', response)


def client_edit_education(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print("save_client_education - request.POST")

        education = Education(
            education=request.POST['education'],
            subject_area=request.POST['subject_area'],
            specialization=request.POST['specialization'],
            qualification=request.POST['qualification'],
            date_start=request.POST['date_start'],  # mast be NOT '' - НУжна проверка на пустое значение!
            date_end=request.POST['date_end'],  # mast be NOT '' - НУжна проверка на пустое значение!
            certificate=Certificate(
                img=request.POST['certificate_img'],
                link=request.POST['certificate_url']
            ).save(),
        )
        education.save()

        print(
            request.POST['education'],
            request.POST['subject_area'],
            request.POST['specialization'],
            request.POST['qualification'],
            request.POST['date_start'],
            request.POST['date_end'],
            request.POST['certificate_img'],
            request.POST['certificate_url'],
        )

        return redirect('/client/edit')
    else:
        print('client_edit_education - request.GET')

    return render(request, 'client/client_edit_education.html', response)


def client_edit_experience(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print("save_client_edit_experience - request POST")

        experiences = Experience(
            name=request.POST['experience_1'],
            position=request.POST['experience_3'],
            start_date=request.POST['exp_date_start'],  # mast be NOT '' - НУжна проверка на пустое значение!
            end_date=request.POST['exp_date_end'],  # mast be NOT '' - НУжна проверка на пустое значение!
            duties=request.POST['experience_4'],
        )
        experiences.save()

        spheres = request.POST.getlist('experience_2')
        for s in spheres:
            if s:
                """ Save ManyToManyField 'sphere' """
                sp = Sphere(sphere_word=s)
                sp.save()
                experiences.sphere.add(sp)

        print(
            request.POST['experience_1'],
            spheres,
            request.POST['experience_3'],
            request.POST['exp_date_start'],
            request.POST['exp_date_end'],
            request.POST['experience_4'],
        )

        return redirect('/client/edit')

    return render(request, 'client/client_edit_experience.html', response)


def form_education(request):
    """ Test Code - Module Form Set """
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        form_set_edu = AddEducationFormSet(request.POST)
        if form_set_edu.is_valid():
            print('form_set_edu - OK')
            for f in form_set_edu:
                f_items = f.cleaned_data.items()
                print("items: %s" % f_items)
                if f_items:
                    edu = f.cleaned_data.get('education')
                    s_a = f.cleaned_data.get('subject_area')
                    sp = f.cleaned_data.get('specialization')
                    qu = f.cleaned_data.get('qualification')
                    ds = f.cleaned_data.get('date_start')
                    de = f.cleaned_data.get('date_end')

                    print("edu: %s, s_a: %s, sp: %s, qu: %s, ds: %s, de: %s"
                          % (edu, s_a, sp, qu, ds, de))

                    education = Education(education=edu,
                                          subject_area=s_a,
                                          specialization=sp,
                                          qualification=qu,
                                          date_start=ds,
                                          date_end=de,
                                          )
                    education.save()
                    client = Client.objects.get(user_client=request.user)
                    client.education = education
                    client.save()
        else:
            print('form_set_edu not valid')

        return redirect(to='/client/edit/form_edu')
    else:
        response['edu_form'] = AddEducationFormSet()
    return render(request, 'client/form_edu.html', response)


def load_client_img(req):
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    try:
        print("user: %s, id: %s" % (req, req.id))
        client_img = Client.objects.get(user_client=req).img
        if client_img:
            logging.info("Client.img: %s" % client_img)
            return "%s%s" % (MEDIA_URL, client_img)
        else:
            return '/media/user_1.png'
    except Exception as ex:
        logging.error("Exception in - load_client_img()\n %s" % ex)
        return '/media/user_1.png'
