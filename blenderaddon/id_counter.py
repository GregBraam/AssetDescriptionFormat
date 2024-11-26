

class IDCounter():
    id = 0
    def next_id(self):
        previous_id = self.id
        self.id+=1
        return previous_id
    
    def __init__(self, starting_id=0):
        self.id=starting_id
        return
        
