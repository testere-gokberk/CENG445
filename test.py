from repo import Repo

sampleRepo = Repo()

sampleRepo.create("Map1", 10, 10, 64, "green")

print("sampleRepo.list()")
sampleRepo.list()

eren = sampleRepo.attach("Map1", "eren")

sampleRepo.list()

sampleRepo.detach("Map1", "eren")

#sampleRepo.delete("Map1")
#sampleRepo.list()

for i in range(9):
    eren[(0, i)] = sampleRepo.components.create("straight")
    eren[(0, i)].rotation = 0

eren[(0, 9)] = sampleRepo.components.create("turn90")
eren[(0, 9)].rotation = 1


eren[(1, 9)] = sampleRepo.components.create("fuel")

eren.draw()
sampleRepo.list()


for i in range(9):
    eren[(i, 9)] = sampleRepo.components.create("straight")
    eren[(i, 9)].rotation = 3

eren.draw()
