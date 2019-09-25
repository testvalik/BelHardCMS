from django.shortcuts import redirect, render
from django.template.context_processors import csrf

from BelHardCRM.settings import MEDIA_URL
from .forms import UploadImgForm, AddEducationFormSet
from .models import *
from .utility import *


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

    """ Загрузка из БД списков для выбора """
    response['client_img'] = load_client_img(request.user)
    response['sex'] = Sex.objects.all()
    response['citizenship'] = Citizenship.objects.all()
    response['family_state'] = reversed(FamilyState.objects.all())
    response['children'] = reversed(Children.objects.all())
    response['country'] = response['citizenship']
    response['city'] = reversed(City.objects.all())
    response['state'] = reversed(State.objects.all())

    if request.method == 'POST':
        print('client_edit_main - request.POST')

        """ Входные данные для сохранения: """
        user = request.user
        user_name = check_input_str(request.POST['client_first_name'])
        last_name = check_input_str(request.POST['client_last_name'])
        patronymic = check_input_str(request.POST['client_middle_name'])
        sex = Sex.objects.get(sex_word=request.POST['sex'])
        date = request.POST['date_born']
        citizenship = Citizenship.objects.get(country_word=request.POST['citizenship'])
        family_state = FamilyState.objects.get(state_word=request.POST['family_state'])
        children = Children.objects.get(children_word=request.POST['children'])
        country = Citizenship.objects.get(country_word=request.POST['country'])
        city = City.objects.get(city_word=request.POST['city'])
        street = check_input_str(request.POST['street'])
        house = check_home_number(request.POST['house'])
        flat = check_home_number(request.POST['flat'])
        telegram_link = check_telegram(request.POST['telegram_link'])
        skype = check_input_str(request.POST['skype_id'])
        email = request.POST['email']
        link_linkedin = request.POST['link_linkedin']
        state = State.objects.get(state_word=request.POST['state'])

        print(user_name, last_name, patronymic, sex, date, citizenship, family_state, children, country, city,
              street, house, flat, telegram_link, skype, email, link_linkedin, state)

        """ проверка - сохранена ли карточка клиента в БД. 
        users_id_list - список карточек c id клиента. """
        users_id_list = [i['user_client_id'] for i in Client.objects.all().values()]
        print("users_id_list: %s" % users_id_list)

        if user.id not in users_id_list:
            """ Если карточки нету - создаём. """
            print('User Profile DO NOT exists - creating!')

            client = Client(
                user_client=user,
                name=user_name,
                lastname=last_name,
                patronymic=patronymic,
                sex=sex,
                date_born=date if date else None,
                citizenship=citizenship,
                family_state=family_state,
                children=children,
                country=country,
                city=city,
                street=street,
                house=house,
                flat=flat,
                telegram_link=telegram_link,
                skype=skype,
                email=email,
                link_linkedin=link_linkedin,
                state=state,
            )
            client.save()
        else:
            """ Если карточка есть - достаём из БД Объект = Клиент_id.
            Перезаписываем (изменяем) существующие данныев. """
            print('User Profile exists - Overwriting user data')

            client = Client.objects.get(user_client=user)  # Объект = Клиент_id

            client.name = user_name
            client.lastname = last_name
            client.patronymic = patronymic
            client.sex = sex
            client.date_born = date if date else None
            client.citizenship = citizenship
            client.family_state = family_state
            client.children = children
            client.country = country
            client.city = city
            client.street = street
            client.house = house
            client.flat = flat
            client.telegram_link = telegram_link
            client.skype = skype
            client.email = email
            client.link_linkedin = link_linkedin
            client.state = state
            client.save()

        """ Сохранение телефонных номеров клиента """
        tel = request.POST.getlist('phone')
        print("tel: %s" % tel)
        for t in tel:
            t = check_phone(t)
            if t:
                phone = Telephone(telephone_number=t)
                phone.client = client
                phone.save()

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
                skill = Skills(skills=check_input_str(s))
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

        arr = pars_exp_request(request.POST)
        for dic in arr:
            organisation = dic['experience_1']
            position = dic['experience_3']
            start_date = dic['exp_date_start']
            end_date = dic['exp_date_end']
            duties = dic['experience_4']

            if any([organisation, position, start_date, end_date, duties]):
                experiences = Experience(
                    name=organisation,
                    position=position,
                    start_date=start_date if start_date else None,
                    end_date=end_date if end_date else None,
                    duties=duties if duties else None)

                experiences.save()

                spheres = dic['experience_2']
                for s in spheres:
                    if s:
                        """ Save ManyToManyField 'sphere' """
                        sp = Sphere(sphere_word=s)
                        sp.save()
                        experiences.sphere.add(sp)

                print(organisation, spheres, position,
                      start_date if start_date else None,
                      end_date if end_date else None,
                      duties if duties else None)

                client = Client.objects.get(user_client=request.user)
                client.organization = experiences
                client.save()
            else:
                print('No Experience data!')

        return redirect('/client/edit')
    else:
        print('save_client_edit_experience - request GET')

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
                                          date_end=de)
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
