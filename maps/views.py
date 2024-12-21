import socket
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import tcp_client
from django.http import JsonResponse
from repo import  Repo


@csrf_exempt
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    request.session.modified = True
    return redirect('home')


from django.shortcuts import render


def home(request):
    username = request.session.get('username', None)

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
            request.session.modified = True

    options = {
        "friction": "Friction cell slows the car down",
        "Booster": "Booster cell increases speed.",
        "Rock": "Stops the car",
        "Slippery": "Changes the angle",
        "turn90": "Rotates the car",
        "straight": "Goes straight",
        "fuel": "Fuel cell to refuel the cars",
        "Ferrari": "A sports car",
        "Merso": "A sports car"
    }

    context = {
        'username_submitted': username is not None,
        'username': username,
        'options': options
    }

    return render(request, 'maps/base.html', context)

def some_view(request):
    options = {
        "friction": "Friction cell slows the car down",
        "Booster": "Booster cell increases speed.",
        "Rock": "Stops the car",
        "Slippery": "Changes the angle",
        "turn90": "Rotates the car",
        "straight": "Goes straight",
        "fuel": "Fuel cell to refuel the cars",
        "Ferrari": "A sports car",
        "Merso": "A sports car"
    }
    return render(request, 'maps/base.html', {'options': options})

def create_map(request):
    username = request.session.get('username', None)

    if not username:
        return redirect('home')

    options = {
        "friction": "Friction cell slows the car down",
        "Booster": "Booster cell increases speed.",
        "Rock": "Stops the car",
        "Slippery": "Changes the angle",
        "turn90": "Rotates the car",
        "straight": "Goes straight",
        "fuel": "Fuel cell to refuel the cars",
        "Ferrari": "A sports car",
        "Merso": "A sports car"
    }

    context = {
        'username_submitted': username is not None,
        'username': username,
        'options': options,
    }

    if request.method == 'POST':
        print("POST METHOD")
        map_id = request.POST.get('map_id')
        cols = request.POST.get('cols')
        rows = request.POST.get('rows')
        cellsize = request.POST.get('cellsize')
        bgcolor = request.POST.get('bgcolor')
        
        response = tcp_client.send_to_server(username, 'create_map', map_id, cols, rows, cellsize, bgcolor)

        context['map_id'] = map_id
        context['message'] = f'Map {map_id} created successfully.'
        request.session["map_id"] = map_id

        #return render(request, 'maps/view_map.html', context)
        return view_map(request)
        #return redirect("view_map", map_id=map_id)

    return render(request, 'maps/create_map_form.html', context)

def create_component(request):
    print("asdas")
    username = request.session.get('username', None)

    if not username:
        return redirect('home')

    options = {
        "friction": "Friction cell slows the car down",
        "Booster": "Booster cell increases speed.",
        "Rock": "Stops the car",
        "Slippery": "Changes the angle",
        "turn90": "Rotates the car",
        "straight": "Goes straight",
        "fuel": "Fuel cell to refuel the cars",
        "Ferrari": "A sports car",
        "Merso": "A sports car"
    }
    context = {
        'username_submitted': username is not None,
        'username': username,
        'options': options,
    }

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        rows = request.POST.get('rows')
        cols = request.POST.get('cols')

        if selected_option and rows and cols:
            response = tcp_client.send_to_server(username, 'create', selected_option, rows, cols)

            return render(request, 'maps/create_component.html', context)

    return render(request, 'maps/create_component.html', context)

def view_map(request):
    
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)
    
    response = tcp_client.send_to_server(username, 'attach', map_id)
    
    print("USER NAME", username)
    print("MAP ID ", map_id)
    print(response)
    
    n = 5
    grid = [[(i + 1) * (j + 1) for j in range(n)] for i in range(n)]
    
    return render(request, 'maps/view_map.html', {
        "map_id":map_id,
        'grid': grid,
        'n': n,
    })
