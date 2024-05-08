from Lexical import Lexical
from SentenceModifier import SentenceModifier

sc = Lexical("A Madonna fez um show no Brasil")
sentence = SentenceModifier(sc)
try:
    sentence.modifier()
except Exception as e:
    print(f"Erro: {e}")
    raise