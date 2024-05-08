import spacy
from Token import Token

class Lexical:
    tokens = []
    def  __init__(self, claim):
        self.claim = claim
        self.nouns = []
        self.verbs = []
# Carregue o modelo de linguagem portuguesa
    def tokenizar(self):    
        nlp = spacy.load('pt_core_news_sm')
        # Processar um texto
        sentence = nlp(self.claim)
        # Classificação das palavras
        for token in sentence:
            tk = Token(token.text, token.pos_, token.dep_, str(token.morph))
            if token.pos_ == "NOUN":
                self.nouns.append(token.text)
            if token.pos_ == "VERB":
                self.verbs.append(token.text)
            self.tokens.append(tk)
           # print(f"{token.text}: {token.pos_}, {token.dep_}")
            # print("sintatico:", self.nouns)nt(f"Relação sintática:{token.text}: {token.dep_} --> {token.head.text}")
        return self.tokens
    
# lx = Lexical('./claim.txt')
# lx.tokenizar()