from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing
from django.urls import reverse_lazy

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True) 

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings' : paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    
    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)


    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html',context)


from .forms import ListingForm 
 
def add_listing(request): 
    context ={} 
    if request.method == 'POST':
 
        print("Before creteing form obj")
        # create object of form 
        form = ListingForm(request.POST or None, request.FILES or None) 
    
        print("After creteing form obj") 
        # check if form data is valid 
        print(form.errors.as_data())
        if form.is_valid(): 
        # save the form data to model 
            print("Before saving form")
            form.save() 
    
            print("After saving form") 
        else:
            messages.error(request, 'Invalid Data Input')
    
    
        context['form']= form 
        p=reverse_lazy("listings")
        return redirect(p)
        #else:
        # print("Invalid") 
    else:
 
        print('abc')
        form=ListingForm()
        context['form']= form 
        return render(request, "listings/add_listing.html", context)