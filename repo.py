from map import Map
from components import Component
from components import ComponentFactory

class Repo:

    def __init__(self):

        self.objects = dict()   # id - object pairs
        self.users = dict()     # userid - list of ids of objects attched 
        self.objowners = dict()   # id - list of userids who use the object
        self.components = ComponentFactory()

    def create(self, *args):

        print(*args[1:])
        self.objects[args[0]] = Map(*(args[1:]))

    def list(self):

        print(list(self.objects.items()))

    def listattached(self, user:str):

        return self.users[user]

    def attach(self, id:int, user:str):

        #if user in list(self.users.keys()):

        if id in list(self.objects.keys()):

            if not user in list(self.users.keys()):
                self.users[user] = []

            if not id in list(self.objowners.keys()):
                self.objowners[id] = []

            self.users[user].append(id)
            self.objowners[id].append(user)

            return self.objects[id]

        else:
            raise f"Object with given id {id} does not exist."
        
        #else:
        #    raise f"User with given id {user} does not exist."

    def detach(self, id:int, user:str):
        
        if user in list(self.users.keys()):
            
            if id in list(self.objects.keys()):
                
                self.users[user].remove(id)
                self.objowners[id].remove(user)

            else:
                raise f"Object with given id {id} does not exist."
            
        else:
            raise f"User with given id {user} does not exist."

    def delete(self, id:int):
        
        del self.objects[id]
        
