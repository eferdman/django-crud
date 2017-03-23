from django.shortcuts import render, get_object_or_404
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.urls import reverse
from .forms import NameForm

def index(request):
    list_of_people = Person.objects.all()
    context = { 'list_of_people': list_of_people }
    return render(request, 'dylapp/index.html', context)

def insert(request):
    if request.method == 'POST': 
        
        # grab the bound form
        form = NameForm(request.POST)

        if form.is_valid():
            # Grab the user input
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            
            # This also works
            #last_name = request.POST.get('last_name', '')
            #first_name = request.POST.get('first_name', '')
            
            # Save a new row in the database
            person_obj = Person(last_name=last_name, first_name=first_name)
            person_obj.save()

            return HttpResponseRedirect('/dylapp')
    else:
        form = NameForm() # unbound form
        
    return render(request, 'dylapp/insert.html', {'form': form})

def delete(request):
    if request.method == 'POST':
        # get radio selection value
        pk = request.POST.get('choice', '')
        # store the user object
        user = get_object_or_404(Person, pk=pk)
        if request.POST.get("delete"):
            # Delete the user from the database
            user.delete()
            # Redirect to index page
            return HttpResponseRedirect('/dylapp')
        else: # send to update
            print(user.id)
            form = NameForm({ 'last_name': user.last_name, 'first_name': user.first_name, 'id': user.pk })
            return render(request, 'dylapp/update.html', {'form': form})
    else:
        # unbound radio choices
        users = Person.objects.all()
        context = { 'users': users }
        # populate the template with user data
        return render(request, 'dylapp/delete.html', context)

def update(request):
    if request.method == 'POST':
        # grab the bound form
        form = NameForm(request.POST)

        if form.is_valid():
            # Grab the user input
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            pk = form.cleaned
            print(request.POST)
        #     # Update row in the database
        #     person_obj = Person.objects.filter(pk=pk)
        #     print(person_obj)
        #     #person_obj.save()

        return HttpResponseRedirect('/dylapp')

def thanks(request):
    return render(request, 'dylapp/thanks.html', {'form': form})