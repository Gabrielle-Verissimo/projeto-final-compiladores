class Syntactic: 
    def __init__(self, buffer):
        self.buffer = buffer
        self.next = 0
        
    def read_token(self):
        if self.next < len(self.buffer):
            self.token = self.buffer[self.next]
            self.next += 1
            return self.token
        else:
            return None
        
    def back(self):
        self.next -= 1
        
    def parser(self):
        self.read_token()
        if(self.token == None): return
        self.back()
        self.texto()
        return
        
        
    def texto(self):
        self.sentenca()
        self.read_token()
        if(self.token.getType() == "PUNCT"):
            if self.next < len(self.buffer):
                self.texto()
            else:
                return
    
    def sentenca(self):
        self.sintagma_nominal()
        self.sintagma_verbal()
        return
    
    def sintagma_nominal(self):
        self.read_token()
        if self.token.getType() == "NOUN":
            return
        elif self.token.getType() == "DET":
            self.read_token()
            if self.token.getType() == "NOUN":
                return
            raise Exception(f"Erro sintático.")
        else:
            self.back()
            return
        
        
    def sintagma_verbal(self):
        self.read_token()
        if self.token.getType() == "VERB":
            self.sintagma_verbal()
            return
        else:
            self.back()
            return