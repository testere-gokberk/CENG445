# main.py

from repo import Repo

def main():
    # Create a map in Repo
    repo = Repo()
    map_id = repo.create("RaceMap", 10, 10, 64, 'green')
    print("Map created with ID:", map_id)
    
    # List all objects in Repo to confirm the creation
    print("Repo List:", repo.list())
    
    # Attach users 'onur' and 'tolga' to the map
    onur_map = repo.attach(map_id, "onur")
    tolga_map = repo.attach(map_id, "tolga")
    
    # Build the race track with road components
    # Example: Add a 90-degree turn at (1,1)
    rt = repo.components.create('turn90')
    onur_map[(1, 1)] = rt
    rt.rotation = 0
    
    '''
    # Add straight road sections from (1,2) to (1,7)
    for j in range(2, 8):
        straight_road = Repo.components.create('straight')
        onur_map[(1, j)] = straight_road
        straight_road.rotation = 0
    
    # Continue building the track with more turns and straight sections
    dt = Repo.components.create('turn90')
    dt.rotation = 1
    onur_map[(1, 8)] = dt

    for i in range(2, 8):
        onur_map[(i, 1)] = Repo.components.create('straight')
        onur_map[(i, 8)] = Repo.components.create('straight')
        onur_map[(i, 1)].rotation = 1
        onur_map[(i, 8)].rotation = 1

    rt = Repo.components.create('turn90')
    onur_map[(8, 1)] = rt
    rt.rotation = 3
    
    for j in range(2, 8):
        onur_map[(8, j)] = Repo.components.create('straight')
        onur_map[(8, j)].rotation = 0

    dt = Repo.components.create('turn90')
    dt.rotation = 2
    onur_map[(8, 8)] = dt

    # Add boosters, rocks, and fuel components
    onur_map[(8, 3)] = Repo.components.create('booster')
    onur_map[(8, 9)] = Repo.components.create('rock')
    onur_map[(7, 1)] = Repo.components.create('fuel')

    # Create and place a car on the map
    car = Repo.components.create('Ferrari')
    car.driver = "Alonso"
    car.map = onur_map
    car.pos = (1.0, 1.0)
    car.topspeed = 300.0
    car.topfuel = 100.0

    # Print car details
    print("Car initialized:", car.model, car.pos, car.topspeed, car.topfuel)

    # Draw the map and display the view
    onur_map.draw()
    cv = onur_map.view(500, 500, 200, 200)
    cv.draw()

    # Simulate some car actions
    car.start()
    car.tick()  # Update car position, fuel, speed, etc.
    car.accel()
    car.left()
    car.tick()  # Update after turning left

    car.right()
    car.accel()
    car.tick()  # Update after turning right and accelerating

    car.stop()
    cv.draw()
    onur_map.draw()'''

if __name__ == "__main__":
    main()
