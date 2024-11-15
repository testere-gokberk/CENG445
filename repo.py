from map import Map

class Repo:

    def __init__(self):

        self.objects = dict()   # id - object pairs
        self.users = dict()     # userid - list of ids of objects attched 
        self.objowners = dict()   # id - list of userids who use the object
        self.next_id = 1
    def create(self, name: str, *args):
       
        obj_id = self.next_id
        self.next_id += 1

        new_obj = Map(*args)  # args unpacks (cols, rows, cellsize, bgcolor) for Map constructor
       
        # Store the object in the repository with its unique ID and name
        self.objects[obj_id] = (obj_id, new_obj)
        self.objowners[obj_id] = []   # Initialize an empty list for tracking attached users

        return obj_id  # Return the unique ID for the created object
    def list(self):

        return list(self.objects.items())

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
        
        #anlamadım bunu
        pass