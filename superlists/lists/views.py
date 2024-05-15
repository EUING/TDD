from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, "home.html")
    
def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
    
def new_list(request):
    lists_ = List.objects.create()
    Item.objects.create(text=request.POST.get("item_text", ''), list=lists_)
    return redirect("/lists/the-only-list-in-the-world")