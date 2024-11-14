from repo import Repo

sampleRepo = Repo()

sampleRepo.create("F571", 10,10, 64, 'green')
sampleRepo.list() # F571 will be listed with an id


ogr = sampleRepo.attach("F571", "onur")
tgr = sampleRepo.attach("F571", "tolga") # these two are the same object

