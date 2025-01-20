import socket
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import tcp_client
from django.http import JsonResponse
from repo import  Repo
from django.shortcuts import render
import json


@csrf_exempt
def logout(request):
    if 'username' in request.session:
        del request.session['username']
        
    request.session["map_id"] = None
    request.session["username"] = None
    request.session.modified = True
    
    return redirect('home')


def home(request):
    username = request.session.get('username', None)

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
            request.session.modified = True

    print("NEW USER ", username )

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
        "merso": "A sports car"
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
        response_json = json.loads(response)
        

        print("POST REQUEST ", request.POST)
        
        if request.POST['action'] == 'attach_map':
            
            print("ATTACHED MAP")
            context['map_id'] = map_id
            tcp_client.send_to_server(username, 'attach', map_id)
            request.session["map_id"] = map_id
        
        context['message'] = f'Map {map_id} created successfully.'
        #request.session["map_id"] = map_id

        #return render(request, 'maps/view_map.html', context)
        #return view_map(request)
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

        print("ADDING ADDING COPMONNET ")
        
        if selected_option and rows and cols:
            print("ADDING COMPONENT ", username, selected_option, rows, cols)
            response = tcp_client.send_to_server(username, 'create', selected_option, rows, cols)

            return render(request, 'maps/create_component.html', context)

    return render(request, 'maps/create_component.html', context)

def view_map(request):

    print("VIEW MAP ")
    
    svg_mapping={
        "ferrari":"/static/maps/images/car_topview.svg",
        "rock": "/static/maps/images/rock.svg",
        "booster":"maps\\images\\booster.svg",
        "checkpoint":"/static/maps/images/  checkpoint.png",
        "friction":"/static/maps/images/friction.svg",
        "slippery" : "/static/maps/images/slippery.png",
        "turn" : "static/maps/images/road_asphalt41.png",
        "straight": "/static/maps/images/road_asphalt01.png",
        "fuel" : "/static/maps/images/fuel.svg",
        "merso": "/static/maps/images/merso.svg",
    }

    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    #print("username ", username)
    #print("MAP ID ", map_id)
    
    response = tcp_client.send_to_server(username, 'attach', map_id)
    
    #print("RESPONSE RAW ", response)
    
    if "Error" in response:
        return render(request, 'maps/view_map.html', {
            'username_submitted': username is not None,
            "username":username,
            "map_id":map_id,
            "error": "You are not attached to any maps ! \n"
            #'n': n,
            })

    response_json = json.loads(response)

    if response_json.get('status') == 'error':
        return render(request, 'maps/view_map.html', {
            'username_submitted': username is not None,
            "username": username,
            "map_id": map_id,
            "error": response_json.get('message', "Error attaching to map")
        })

    size_response = tcp_client.send_to_server(username, "map_size", map_id)
    size_json = json.loads(size_response)

    #size_response = eval(size_response)

    #print("USER NAME", username)
    #print("MAP ID ", map_id)
    #print("RESPONSE ",response)
    #print("SIZE RESPONSE ", size_response)
    #print("BG COLOR ", size_response[-1])
    
    print("MAP INFO")
    print("response ", response_json)
    print("size response ", size_json)

    if size_json.get('status') == 'success':
        
        print("SIZE JSON SUCCESS")
        
        size_info = size_json.get('map_size', {})
        rows = size_info[0]
        cols = size_info[1]
        bgcolor = size_info[3]

        print("ROWS ", rows, " COLS ", cols)

        grid = [["" for j in range(cols)] for i in range(rows)]

        components = response_json.get('components', {})
        
        for comp_id, comp_info in components.items():
            row = int(comp_info[0])
            col = int(comp_info[1])
            rotation = comp_info[2] * 90
            comp_type = comp_info[3].lower()

            if comp_type in svg_mapping:
                grid[row][col] = svg_mapping[comp_type] # rotationu ayrı arraye koy

        print("GRID TO RENDER ", grid)

        return render(request, 'maps/view_map.html', {
            'username_submitted': username is not None,
            "username": username,
            "map_id": map_id,
            'grid': grid,
            "color": bgcolor,
        })
    
    
    #print("RESPONSE EWFPŞEHGBJNUIPMKJINDHFG", response)
    
    for key,value in zip(response.keys(), response.values()):
        #print("KEY", key)
        #print("VALUE ", value)
        grid[int(value[0])][int(value[1])] = (svg_mapping[value[3]], value[2]*90)
        
    #print("GRID ", grid)
    
    return render(request, 'maps/view_map.html', {
        'username_submitted': username is not None,
        "username":username,
        "map_id":map_id,
        'grid': grid,
        "color":size_response[-1],
        #'n': n,
    })

def list_maps(request):
    
    username = request.session.get('username', None)
    
    #response = tcp_client.
    
    response = tcp_client.send_to_server(username, "list_maps")
    response_json = json.loads(response)
    
    print("RESPONSE", response)


    print("MAP LIST ", response_json.get("maps", []))
    
    context = {
        'username_submitted': username is not None,
        'username': username,
        "map_list":response_json.get("maps", [])
    }
    
    if request.method == 'POST':
        selected_maps = request.POST.getlist('selected_map')

        if selected_maps:
            map_id = selected_maps[0]
            attach_response = tcp_client.send_to_server(username, "attach", map_id)
            attach_data = json.loads(attach_response)

            if attach_data.get('status') == 'success':
                request.session["map_id"] = map_id
                context["success_message"] = attach_data.get('message', f"Map {map_id} attached")
            else:
                context["error_message"] = attach_data.get('message', "Error attaching to map")

    return render(request, 'maps/list_maps.html', context)

"""
def submit_maps(request):

    print("INSIDE SUNMIT MAPS")

    print("req method ", request.method)
    
    username = request.session.get("username", None)

    if request.method == 'POST':

        selected_maps = request.POST.getlist('selected_maps')  

        print("SELECTED MAPS ", selected_maps)

        for map_id in selected_maps:
            response = tcp_client.send_to_server(username, "attach", map_id)
            print(f"Processed map {map_id}: {response}")

        context = { 'username_submitted': username is not None,
                    'username': username}

        return render(request, 'maps/base.html', context)
        
    
    return render(request, 'maps/base.html', context)
"""
def create_component(request):
    print("asdas")
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    if not username:
        return redirect('home')

    options = {
        "friction": "Friction cell slows the car down",
        "booster": "Booster cell increases speed.",
        "rock": "Stops the car",
        "slippery": "Changes the angle",
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
            print("qweqwe")
            print("ADDING COMPONENT ", username, map_id, selected_option, rows, cols)
            
            response = tcp_client.send_component_to_server(username, map_id, selected_option, rows, cols)
            response_data = json.loads(response)
            
            if response_data.get('status') == 'error':
                context['error'] = response_data.get('message', "Error creating component")
            else:
                context['response'] = response_data.get('message', "Component created successfully")

            return render(request, 'maps/create_component.html', context)

    return render(request, 'maps/create_component.html', context)

def delete_component(request):
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    if not username:
        return redirect('home')

    context = {
        'username_submitted': username is not None,
        'username': username,
        'map_id': map_id,
    }

    if request.method == 'POST':
        component_id = request.POST.get('component_id')

        if component_id:
            response = tcp_client.send_delete_to_server(username, map_id,'delete','component', component_id)
            response_json = json.loads(response)
            context['response'] = response_json.get('message', "Component deleted")

            return render(request, 'maps/delete_component.html',context)

    return render(request, 'maps/delete_component.html', context)

def rotate_component(request):
    print("INSIDE ROTATE")
    
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    if not username:
        return redirect('home')

    context = {
        'username_submitted': username is not None,
        'username': username,
        'map_id': map_id,
    }

    if request.method == 'POST':
        component_id = request.POST.get('component_id')

        print("INSIDE ROTATE ROTATING ", component_id)

        if component_id:
            response = tcp_client.send_rotate_to_server(username, map_id,'rotate', component_id)
            response_json = json.loads(response)
            context['response'] = response_json.get('message', "Component rotated")

            return render(request, 'maps/rotate_component.html',context)

    return render(request, 'maps/rotate_component.html', context)

def save_repo(request):
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    if not username:
        return redirect('home')

    context = {
        'username_submitted': username is not None,
        'username': username,
        'map_id': map_id,
    }

    if request.method == 'POST':  # When Save Repo button is clicked
        response = tcp_client.send_save_to_server(username, map_id, 'save')
        context['response'] = response  # Pass the response to the template

    return render(request, 'maps/save_repo.html', context)


def start_game_mode(request):
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    if not username:
        return redirect('home')

    context = {
        'username_submitted': username is not None,
        'username': username,
        'map_id': map_id,
    }

    if request.method == 'POST':
        response = tcp_client.send_gamemode_to_server(username, map_id, 'game_mode')
        response_data = json.loads(response)
        context['response'] = response_data.get('message', "default gamemode message")

    return render(request, 'maps/list_maps.html', context)


def parse_url(input_string):
    
    last_slash = input_string.rfind('/')
    last_dot = input_string.rfind('.')
    
    if last_slash != -1 and last_dot != -1 and last_dot > last_slash:
        return input_string[last_slash + 1:last_dot]
    return ""


@csrf_exempt
def item_dropped(request):
    
    username = request.session.get('username', None)
    map_id = request.session.get('map_id', None)

    print("INSIDE DROP HANDLER ", "username ", username, "map_id", map_id)

    url_2_image ={
        "road_asphalt01" : "straight",
        "fuel": "fuel",
        "road_asphalt41" : "turn",
        "rock":"rock",
        "car_topview": "Ferrari",
        "checkpoint" : "checkpoint",
        "slippery":"slippery",
        "friction":"friction"
    }

    if request.method == 'POST':
        
        data = json.loads(request.body)
        x = data.get('x')
        y = data.get('y')
        item_name = data.get('item_name')
        
        item_name = parse_url(item_name)
        print(f"ITEM DROPPED {x} {y} name {item_name}")
        print("ADDING DROPPED COMPONENT ", username, item_name, x, " " ,y)
        
        
        
        response = tcp_client.send_component_to_server(username, map_id, url_2_image[item_name], y, x)
        # urlleri item adına dönüştür
        response_json = json.loads(response)
        
        print("DROP RESPONSE ", response_json)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)
