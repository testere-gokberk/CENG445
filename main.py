from repo import Repo

sampleRepo = Repo()
    
sampleRepo.create("F571", 10,10, 64, 'green')
sampleRepo.list() # F571 will be listed with an id

ogr = sampleRepo.attach("F571", "onur")
tgr = sampleRepo.attach("F571", "tolga") # these two are the same object
for j in range(2,8):
    ogr[(1,j)] = sampleRepo.components.create('straight')
    ogr[(1,j)].rotation = 0
ogr.draw()
ogr.view(65,65,310,310).draw()

"""sampleRepo.components.list()

rt = sampleRepo.components.create('turn90')

ogr[(1,1)] = rt
rt.rotation = 0

for j in range(2,8):
    ogr[(1,j)] = sampleRepo.components.create('straight')
    ogr[(1,j)].rotation = 0


##ogr.draw()

dt = sampleRepo.components.create('turn90')
dt.rotation = 1
ogr[(1,8)] = dt

for i in range(2,8):
    ogr[(i,1)] = sampleRepo.components.create('straight')
    ogr[(i,8)] = sampleRepo.components.create('straight')
    ogr[(i,1)].rotation = 1
    ogr[(i,8)].rotation = 1

rt = sampleRepo.components.create('turn90')
ogr[(8,1)] = rt
rt.rotation = 3

for j in range(2,8):
    ogr[(8,j)] = sampleRepo.components.create('straight')
    ogr[(8,j)].rotation = 0

dt = sampleRepo.components.create('turn90')
dt.rotation = 2
ogr[(8,8)] = dt
ogr[(8,3)] = sampleRepo.components.create('booster')
ogr[(8,9)] = sampleRepo.components.create('rock')
ogr[(8,9)] = sampleRepo.components.create('rock')
ogr[(8,9)] = sampleRepo.components.create('rock')
ogr[(0,8)] = sampleRepo.components.create('rock')
ogr[(1,0)] = sampleRepo.components.create('rock')
ogr[(7,1)] = sampleRepo.components.create('fuel')

##ogr.draw()
##print("COMPONENT LIST")
##print(sampleRepo.components.list())


frr = ogr.components.create('Ferrari')
frr.driver = "Alonso"
frr.angle = 0
frr.speed = 50

##print(frr.model, frr.pos, frr.topspeed, frr.topfuel)

ogr.draw()

cv = ogr.view(500,500,200,200)
##cv.draw()

frr.start()
frr.tick()
frr.accel()
frr.tick()
frr.accel()
frr.tick()
frr.accel()
frr.tick()
frr.accel()
frr.tick()
frr.right()


frr.tick()
<<<<<<< Updated upstream
frr.stop()
cv.draw()
ogr.draw()"""


frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.left()
frr.tick()
frr.tick()
frr.left()
frr.tick()
frr.tick()
frr.right()

frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.left()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.left()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.left()
frr.tick()
frr.tick()
frr.tick()
frr.tick()








"""frr.right()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()"""



"""frr.left()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()"""




















ogr.draw()
frr.stop()
##cv.draw()
##ogr.draw()
>>>>>>> Stashed changes


