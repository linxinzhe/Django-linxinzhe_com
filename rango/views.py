from django.shortcuts import render, HttpResponseRedirect, reverse

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


# Create your views here.
def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {'categories': category_list, "pages": page_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {}
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
