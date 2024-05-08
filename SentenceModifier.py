import spacy
from bs4 import BeautifulSoup
import requests
from Token import Token
# Carregue o modelo de linguagem
nlp = spacy.load('pt_core_news_sm')

class SentenceModifier:
    
    passive_sentence = ''
    synonym_sentence = ''
    
    def __init__(self, scanner):
        self.buffer_tokens = scanner.tokenizar()
        self.original_sentence = scanner.claim
        self.nouns = scanner.nouns
        self.verbs = scanner.verbs
        self.token = Token
        self.next = 0
    
    def read_token(self):
        if self.next < len(self.buffer_tokens):
            self.token = self.buffer_tokens[self.next]
            self.next += 1
            return self.token
        else:
            return None
        
    def back(self):
        self.next -= 1
    
    def modifier(self):
        self.passive_voice()
        self.synonym()
        print(f'Frase original: {self.original_sentence}')
        print(f'Frase na voz passiva: {self.passive_sentence}')
        print(f'Frase com sinônimos: {self.synonym_sentence}')
        
    def passive_voice(self):
        artigo = ""
        sujeito = ""
        verbo = ""
        objeto = ""
        gender_subj = ""
        num_subj = ""
        num_root = ""
        tense_root = ""
        gender_obj = ""
        num_obj = ""
        while self.read_token() != None:
            #print(f"Token: {self.token.getContent()}, POS: {token.pos_}, DEP: {self.token.getDep()}")  # Depuração para ver todos os tokens e suas dependências
            if self.token.getDep() == "nsubj":
                sujeito = self.token.getContent()
                morph = self.token.getMorph()
                position = morph.find("Gender")
                gender_subj = morph[position+7:position+11]
                if gender_subj[-1] == '|': gender_subj = morph[position+7:position+10]
                position = morph.find("Number")
                num_subj = morph[position+7:position+11]
            elif self.token.getDep() == "ROOT":
                verbo = self.token.getContent()
                morph = self.token.getMorph()
                position = morph.find("VerbForm")
                verb_form = morph[position+9:position+12] 
                position = morph.find("Number")
                num_root = morph[position+7:position+11]
                position = morph.find("Tense")
                tense_root = morph[position+6:position+10]
                if tense_root[-1] == '|': tense_root = morph[position+6:position+9]
            elif self.token.getDep() == "obj":
                objeto = self.token.getContent()
                morph = self.token.getMorph()
                position = morph.find("Gender")
                gender_obj = morph[position+7:position+11]
                if gender_obj[-1] == '|': gender_obj = morph[position+7:position+10]
                position = morph.find("Number")
                num_obj = morph[position+7:position+11]
                # Cria a frase na voz passiva
        aux = ''
        preposicao = ''
        participio = '' 
        resposta = requests.get(f'https://www.conjugacao.com.br/busca.php?q={verbo}')

        # Criar um objeto BeautifulSoup
        soup = BeautifulSoup(resposta.text, 'html.parser')
        # Encontrar todas as tags com id 'meu_id'
        tags = soup.find_all(class_='f')
        participio = tags[2].text

        if num_obj == 'Sing':
            if tense_root == 'Pres': aux = 'é'
            elif tense_root == 'Fut': aux = 'será'
            elif tense_root == 'Past': aux = 'foi'
        elif num_obj == 'Plur':
            if tense_root == 'Pres': aux = 'são'
            elif tense_root == 'Fut': aux = 'serão'
            elif tense_root == 'Past': aux = 'foram'
            
        suj = sujeito.lower()
        if suj in('eu', 'tu', 'ele', 'nós', 'vós', 'eles'): 
            preposicao = 'por'
            if suj == 'eu': suj = 'mim'
        elif num_subj == 'Sing':
            if gender_subj == 'Fem': preposicao = 'pela'
            else: preposicao = 'pelo'
        elif num_subj == 'Plur':
            if gender_subj == 'Fem': preposicao = 'pelas'
            else: preposicao = 'pelos'

        artigo = {'Sing': {'Fem': 'A', 'Masc': 'O'},
                'Plur': {'Fem': 'As', 'Masc': 'Os'}
                }[num_obj][gender_obj]

        verbo_participio = {'Sing': {'Fem': participio[:-1] + 'a', 'Masc': participio},
                            'Plur': {'Fem': participio[:-1] + 'as', 'Masc': participio + 's'}
                            }[num_obj][gender_obj]

        # Montando a frase na voz passiva
        self.passive_sentence = f"{artigo} {objeto} {aux} {verbo_participio} {preposicao} {suj}"

    def synonym(self):
        noun_response = requests.get(f'https://www.sinonimos.com.br/{self.nouns[0]}')
        verb_response = requests.get(f'https://www.sinonimos.com.br/{self.verbs[0]}')
        # Criar um objeto BeautifulSoup
        noun_soup = BeautifulSoup(noun_response.text, 'html.parser')
        verb_soup = BeautifulSoup(verb_response.text, 'html.parser')

        # Encontrar todas as tags com id 'meu_id'
        noun_arr = noun_soup.find_all(class_='sinonimo')
        verb_arr = verb_soup.find_all(class_='sinonimo')
        
        noun_synonym = noun_arr[0].text
        verb_synonym= verb_arr[0].text

        modified_sentence = str(self.original_sentence).replace('show', noun_synonym)
        self.synonym_sentence = modified_sentence.replace('fez', verb_synonym)

