import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from registration.backends.simple.views import RegistrationView

from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, User

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


def category(request, category_name_slug):
    context_dict = {}
    context_dict["result_list"] = None
    context_dict["query"] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = Page.objects.filter(title__icontains=query)
            context_dict['result_list'] = result_list
            context_dict['query'] = query
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by("-views")
        context_dict["pages"] = pages
        context_dict["category"] = category
        if not context_dict["query"]:
            context_dict["query"] = category.name
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


# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return reverse("rango:add_profile")


def track_url(request):
    url = reverse("rango:index")
    if request.method == "GET":
        if "page_id" in request.GET:
            page_id = request.GET["page_id"]
            try:
                page = Page.objects.get(pk=page_id)
                if page:
                    page.views = F("views") + 1
                    page.save()
                    url = page.url
                    return HttpResponseRedirect(url)
            except Page.DoesNotExist:
                pass
    return HttpResponseRedirect(url)


def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:  # Run our Bing function to get the results list!
            pass  # result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})


@login_required
def register_profile(request):
    form = UserProfileForm()
    if "user_id" in request.POST:
        user_id = request.POST["user_id"]
        user = User.objects.get(pk=user_id)
        user_profile = user.userprofile
        if user_profile:
            return HttpResponseRedirect(reverse("rango:index"))
        else:
            if request.method == "POST":
                profile_form = UserProfileForm(data=request.POST)
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    if "picture" in request.FILES:
                        profile.picture = request.FILES["picture"]
                    profile.save()
                    return HttpResponseRedirect(reverse("rango:index"))
    return render(request, "registration/profile_registration.html", {"form": form})


@login_required
def profile(request):
    form = UserProfileForm()
    if request.method == "GET":
        if "user_id" in request.GET:
            user_id = request.GET["user_id"]
            user = User.objects.get(pk=user_id)
            user_profile = user.userprofile
            if user_profile:
                return render(request, "rango/profile.html", {"user_profile": user_profile})

    if request.method == "POST":
        if "user_id" in request.POST:
            user_id = request.POST["user_id"]
            user = User.objects.get(pk=user_id)
            user_profile = user.userprofile
            if user_profile:
                user_profile.website = request.POST["website"]
                if "picture" in request.FILES:
                    user_profile.picture = request.FILES["picture"]
                user_profile.save()
                return HttpResponseRedirect(reverse("rango:index"))


@login_required
def like_category(request):
    likes = 0
    if request.method == "GET":
        if "category_id" in request.GET:
            category_id = request.GET["category_id"]
            category_obj = get_object_or_404(Category, pk=category_id)
            category_obj.likes = F("likes") + 1
            category_obj.save()
            category_obj = get_object_or_404(Category, pk=category_id)
            likes = category_obj.likes
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=""):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ""
    if request.method == "GET":
        starts_with = request.GET["suggestion"]
    cat_list = get_category_list(8, starts_with)

    return render(request, "rango/category_list.html", {"cat_list": cat_list})
