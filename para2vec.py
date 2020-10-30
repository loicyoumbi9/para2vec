from os import listdir
import os
import re
import string
from os.path import isfile, join, isdir
from pathlib import Path
import re
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from gensim.test.utils import get_tmpfile
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score

a = string.punctuation
ma_ponctuation = ['if', 'else', 'final', 'else if', 'private', 'android', 'import', 'abstract',
                  'package', 'class', 'return', 'public', 'static', 'void', 'boolean', 'String', 'null', 'this']
ma_ponctuation2 = ['if ', 'else ', 'final ', 'else if ', 'private ', 'android ', 'import ', 'abstract ',
                  'package ', 'class ', 'return ', 'public ', 'static ', 'void ', 'boolean ', 'String ', 'null ', 'this ']
chemin = ""


def nom_dossier(chemin):
    dossiers = [f for f in listdir(chemin) if isdir(join(chemin, f))]
    return dossiers


def nom_fichier(chemin):
    fichier = [f for f in listdir(chemin) if isfile(join(chemin, f))]
    return fichier


def concatener_fichier_java():
    for element in nom_dossier('test_traite_dossier/'):
        if isdir('test_traite_dossier/'+element):
            with open('dosier_fichier_concat/'+element+'.txt', 'w+') as file:
                for p in Path('test_traite_dossier/'+element).glob('./**/*.java'):
                    if p.is_file():
                        a = str(open(p, 'r').read())
                        file.write(a)
    return 0


def commentaire():
    exp = r'/\*.*\*/|//.*'
    fichier = [f for f in listdir(
        'dosier_fichier_concat/') if isfile(join('dosier_fichier_concat/', f))]
    for fichier_txt in fichier:
        with open('dosier_fichier_concat/'+fichier_txt, 'r') as f1, open('dosier_fichier_concat_traite/'+fichier_txt, 'w') as f2:

            # Reading the file and remove inline comments (i.e /*-----*/ or //----------)
            result = re.sub(exp, '', f1.read())

            # Preprocessing for remove multiline comments
            result = result.replace('\n', ')(').replace('*/', '*/\n')

            # Remove multiline comments (i.e /*--------
            #								   --------
            #								   --------*/)
            result = re.sub(exp, '', result)

            # Inversing the preprocessing
            result = result.replace('\n', '').replace(')(', '\n')

            # Storing the result in result.txt file
            f2.write(result)
        lines = open('dosier_fichier_concat_traite/' +
                     fichier_txt, 'r').readlines()
        with open('dossier_pre_final/'+fichier_txt, "w+") as file:
            for line in lines:
                if line != '\n':
                    for word in ma_ponctuation:
                        if word in line:
                            line = line.replace(word, '')
                    if line != '\n':
                        new_line = " ".join(
                            "".join([" " if ch in string.punctuation else ch for ch in line]).split())
                        file.write(new_line + "\n")
        with open('dossier_pre_final/'+fichier_txt, "r") as f3, open('dossier_final/'+fichier_txt, "w+") as f4:
            for line in f3:
                if not line.isspace():
                    f4.write(line)
        with open('dossier_final/'+fichier_txt, "r") as f5, open('dossier/'+fichier_txt, "w+") as f6:
            for line in f5.readlines():
                for word in line:
                    print(word)
                    
    return file


def nombre_de_ligne(fichier_a_compter):
    nombre_de_ligne = 0
    lines = open('dossier_final/'+fichier_a_compter, 'r').readlines()
    for line in lines:
        nombre_de_ligne += 1
    return nombre_de_ligne


def bloc_fichier_en_tableau():
    tab = []
    content = []
    n = 0
    i = 0
    k = 0
    tableau = []
    line = []
    lines = ""
    
    for element in nom_fichier('dossier_final/'):
        nb_ligne = nombre_de_ligne(element)
        #nb_ligne= 500
        nombre_ligne = (nb_ligne // 300) 
        m = (nb_ligne // 300) 
        lines = open('dossier_final/'+element, 'r')
        while (i <= nb_ligne and nombre_ligne <= nb_ligne):
            for k in range(i, nombre_ligne) :
            	tab +=readline(k,lines).split()
            content.append(tab)	           	
            i+=m
            nombre_ligne += m
            print(tab)
            tab = []
        
        tableau += content
        content = []
        tab = []
        i = 0
        nombre_ligne = 0
    print(len(tableau))
    
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(tableau)]
    model = Doc2Vec(documents, vector_size=100,
                    window=5, min_count=1, workers=4)
    print("Fin de la construction du modèle Doc2Vec")
    for epoch in range(20):
    	model.train(documents,epochs=model.iter,total_examples=model.corpus_count)
    	print("Epoch #{} is complete.".format(epoch+1))
    for element in model:
        print(element)  
    fname = get_tmpfile("para2vec.kv")
    model.save(fname)
    return model
    #return model


def readline(n, lines):
    for lineno, line in enumerate(lines):
        return line


if __name__ == "__main__":
    #concatener_fichier_java()
    #commentaire()
    bloc_fichier_en_tableau()
    # print(nombre_de_ligne())
    
