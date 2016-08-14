import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from registration.backends.simple.views import RegistrationView

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page

logger = logging.getLogger(__name__)


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(request, "last_visit", str(datetime.datetime.now()))
    last_visit_time = datetime.datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session["last_visit"] = str(datetime.datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie

    request.session["visits"] = visits


# Create your views here.
def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {'categories': category_list, "pages": page_list}

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    if request.session.test_cookie_worked():
        logger.debug("Test cookie worked")
        print("Test cookie worked")
        request.session.delete_test_cookie()
    visits = int(request.session.get("visits", 0))
    visits += 1
    request.session["visits"] = visits
    context_dict = {"visits": visits}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:
        context_dict["pages"] = None
        context_dict["category"] = None
    return render(request, "rango/category.html", context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse("rango:index"))
        else:
            print(form.errors)
    return render(request, "rango/add_category.html", {"form": form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return HttpResponseRedirect(reverse("rango:category", args=(category_name_slug,)))
        else:
            print(form.errors)
    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context_dict)


# def register(request):
#     registered = False
#     if request.method == "POST":
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if "picture" in request.FILES:
#                 profile.picture = request.FILES["picture"]
#
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     return render(request, "rango/register.html",
#                   {"user_form": user_form, "profile_form": profile_form, "registered": registered})
#
#
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("rango:index"))
#             else:
#                 return HttpResponse("You Rango account is disabled.")
#         else:
#             print("Invalid login details: {0}, {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, "rango/login.html", {})
#
#
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return "/rango/"
