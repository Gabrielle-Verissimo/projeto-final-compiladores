class Token:
    def __init__(self, content, type, dep, morph):
        self.type = type
        self.dep = dep
        self.content = content
        self.morph = morph

    def getType(self):
        return self.type
    
    def setType(self, type):
        self.type = type
        
    def getDep(self):
        return self.dep
    
    def setDep(self, dep):
        self.dep = dep

    def getContent(self):
        return self.content
    
    def setContent(self, content):
        self.content = content
        
    def getMorph(self):
        return self.morph
    
    def setMorph(self, morph):
        self.morph = morph

    def __str__(self):
        return f"Token [content = {self.content}, type = {self.type}, dep = {self.dep}, morph = {self.morph}]"