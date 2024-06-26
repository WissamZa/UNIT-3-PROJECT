from django.db.models.manager import BaseManager
from django.shortcuts import redirect, render
from django.http import HttpRequest, QueryDict

from favorites.models import Favorite
from account.models import Cart
from .models import Product, Product_image
from main.validator import validat, ValidationError
from django.core.paginator import Paginator


def search_product_view(request: HttpRequest):
   try:
      if request.method == 'GET':
         products = Product.objects.filter(
            name__contains=request.GET.get('name'))
   except Exception as e:
      print(e)
   return render(request, "product/search_product.html", {'products': products})


def add_product_view(request: HttpRequest):
   if not (request.user.is_staff or request.user.has_perm("product.add_product")):
      return render(request, "main/no_permission.html")
   if request.method == "POST":
      images = request.FILES.getlist("images")
      new_product = Product.objects.create(
          name=request.POST.get("name"),
          model=request.POST.get("model"),
          category=request.POST.get("category"),
          price=request.POST.get("price"),
          in_stock=request.POST.get("in_stock")
      )

      for image in images:
         Product_image.objects.create(product=new_product, image=image)

      return redirect("product:product_detail_view", product_id=new_product.pk)

   return render(request, "product/add_product.html", {"categories": Product.categories_choices.choices})


def product_detail_view(request: HttpRequest, product_id):
   msg = None
   try:
      product = Product.objects.get(pk=product_id)
      is_favored = request.user.is_authenticated and Favorite.objects.filter(
         user=request.user, product=product).exists()
      if request.method == "POST":
         if request.user.is_authenticated:
            user_cart = Cart.objects.filter(user=request.user)
            if user_cart.filter(product=product).exists():
               product_in_cart = user_cart.get(
                  product=product)
               product_in_cart.quantity = request.POST.get('quantity')
               product_in_cart.save()
            else:
               user_cart.create(user=request.user, product=product,
                                quantity=request.POST.get('quantity'))
         else:
            msg = "يجب تسجيل الدخول لإضافة منتج الى السلة"

   except Exception as e:
      print(e)
   return render(request, "product/product_detail.html", {"product": product,
                                                          "is_favored": is_favored,
                                                          "msg": msg})


def product_by_category(request: HttpRequest, category: str):
   msg = None
   try:
      products: BaseManager[Product] = Product.objects.filter(
         category=category)
      print(Product_image.objects.get(pk=1).image.name)
      pages = Paginator(products.order_by('-created_at'), per_page=3)
      req = request.GET
      if "page" in req:
         if int(req.get("page")) in pages.page_range:
            products = pages.get_page(req.get("page"))
      else:
         products = pages.get_page(1)
      return render(request, "product/product_by_category.html",
                    {"products": products, "pages": pages, "category": category})
   except Product.DoesNotExist:
      msg = "لا يوجد منتجات حاليا"
      return render(request, "product/product_by_category.html", {"msg": msg})


def update_product_view(request: HttpRequest, product_id):
   try:
      product = Product.objects.get(pk=product_id)
      images = request.FILES.getlist("images")
      if not (request.user.has_perm("product.change_product") or request.user.is_superuser):
         return render(request, "main/no_permission.html")
      if request.method == "POST":
         product.name = request.POST.get("name")
         product.model = request.POST.get("model")
         product.category = request.POST.get("category")
         product.price = request.POST.get("price")
         product.in_stock = request.POST.get("in_stock")
         Product_image.delete(product=product)
         for image in images:
            product.Images.objects.create(image=image)
         product.save()
         return redirect("product:product_detail_view", product_id)

   except Product.DoesNotExist:
      return render(request, "404.html")
   except Exception as e:
      print(e)
   return render(request, 'product/update_product.html', {
       "product": product, "categories": Product.categories_choices.choices})


def delete_product_view(request: HttpRequest, product_id):
   try:
      if not (request.user.has_perm("product.delete_product") or request.user.is_superuser):
         return render(request, "main/no_permission.html")
      print("dsklfmsdlkmflkdsmkl")
      product = Product.objects.get(pk=product_id)
      product.delete()

   except Product.DoesNotExist:
      return render(request, "404.html")
   except Exception as e:
      print(e)
   return redirect("main:index_view")

   # def search(req: QueryDict):
   #    plants = Plant.objects.all()
   #    if "name" in req and req.get("name") != "":
   #       plants = plants.filter(name__contains=req["name"])
   #    if "edible" in req and req.get("edible") != "":
   #       plants = plants.filter(is_edible=req["edible"])
   #    if "category" in req and req.get("category") != "":
   #       plants = plants.filter(category=req["category"])
   #       active_cat = req["category"]

   #    else:
   #       active_cat = "All"
   #    pages = Paginator(plants, per_page=3)
   #    if "page" in req:
   #       if int(req.get("page")) in pages.page_range:
   #          plants = pages.get_page(req.get("page"))
   #    else:
   #       plants = pages.get_page(1)
   #    return pages, plants, active_cat

   # def all_plants_view(request: HttpRequest):
   #    pages, plants, active_cat = search(request.GET)
   #    return render(request, "main/all_plants.html",
   #                  {"plants": plants, "pages": pages, "active_cat": active_cat,
   #                   "categories": Plant.category_choices.choices})

   # def search_plants_view(request: HttpRequest):
   #    pages, plants, active_cat = search(request.GET)
   #    return render(request, "main/search_plant.html",
   #                  {"plants": plants, "pages": pages, "active_cat": active_cat,
   #                   "categories": Plant.category_choices.choices})

   # def contactUs_messages_view(request: HttpRequest):
   #    if not request.user.is_superuser:
   #       return render(request, "main/no_permission.html")

   #    messages = Contact.objects.all()
   #    pages = Paginator(messages, per_page=8)
   #    req = request.GET
   #    if "page" in req:
   #       if int(req.get("page")) in pages.page_range:
   #          messages = pages.get_page(req.get("page"))
   #    else:
   #       messages = pages.get_page(1)
   #    return render(request, "main/messages.html", {"pages": pages, "messages": messages})

   # def add_comment_view(request: HttpRequest, plant_id):
   #    if request.method == "POST":
   #       plant = Plant.objects.get(pk=plant_id)
   #       Comment.objects.create(
   #           plant=plant,
   #           user_name=request.user.username,
   #           content=request.POST.get("content"))
   #    return redirect("main:plant_detail_view", plant_id=plant.pk)
