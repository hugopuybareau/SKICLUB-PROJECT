import pandas as pd

sg_csv = pd.read_csv("sgstrmaine2.csv")
inv_csv = pd.read_csv("inv_prog.csv")

### ATTENTION POUR QUE ÇA MARCHE FAUT RAJOUTER UNE LIGNE ',,,,,,,,,' COMME ÇA À LA FIN DU CSV DU L'INVENTAIRE.

n_participant = len(sg_csv['Nom']) #Participant SG

#Indices pour l'inventaire

index_inv = {
    'ski' : 0,
    'chaussure_ski' : 0,
    'sb' : 0,
    'chaussure_sb' : 0,
    'casque' : 0,
}

for index, val in index_inv.items() : 
    while not pd.isna(inv_csv[index][val]) :
        val += 1
    index_inv[index] = val

# Création du dictionnaire pour le SG
# Le format c'est pas compliqué en sah faut juste pas être con    
    
data = { 
    'Rang SG' : [0 for i in range(n_participant)],
    'Nom' : ['' for i in range(n_participant)],
    'Prénom' : ['' for i in range(n_participant)],
    'Surnom' : ['' for i in range(n_participant)],
    'Niveau' : ['' for i in range(n_participant)],
    'Taille' : ['' for i in range(n_participant)],
    'Poids' : ['' for i in range(n_participant)],
    'Ski' : [[0 for i in range(3)] for i in range(n_participant)],
    'Chaussure ski' : [0 for i in range(n_participant)],
    'Snowboard' : [[0 for i in range(3)] for i in range(n_participant)],
    'Chaussure snowboard' : [0 for i in range(n_participant)],
    'Bâtons' : ['Non' for i in range(n_participant)], 
    'Casque' : [0 for i in range(n_participant)],
    'Réglés ?' : ['Non' for i in range(n_participant)],
    'À Contacter ?' : ['Non' for i in range(n_participant)],
}

# Création du dictionnaire pour l'inventaire
# Le format c'est le numéro de la pièce suivi de la taille de la pièce

data_inv = {
    'Ski' : [[0,0,''] for i in range(index_inv['ski'])],
    'Chaussure ski' : [[0,0] for i in range(index_inv['chaussure_ski'])],
    'Snowboard' : [[0,0] for i in range(index_inv['sb'])],
    'Chaussure snowboard' : [[0,0] for i in range(index_inv['chaussure_sb'])],
    'Casque' : [[0,0] for i in range(index_inv['casque'])],
}

#Je prends que les colonnes qui m'intéressent vraiment pour le SG

column_list_csv = list(sg_csv.columns[:5]) + list(sg_csv.columns[6:11]) + list(sg_csv.columns[12:16]) + list(sg_csv.columns[17:20])

#Génère les colonnes avec les données du CSV non-attribuées
    
for index, row in sg_csv.iterrows() : #Pour les data du SG
    data['Rang SG'][index]=(index+1)
    data['Nom'][index]=row[column_list_csv[1]]
    data['Prénom'][index]=row[column_list_csv[2]]
    data['Surnom'][index]=row[column_list_csv[3]]
    data['Niveau'][index]=row[column_list_csv[4]]
    if row[column_list_csv[4]] == 'Expert' : #Pas trouver d'autres solutions pour mieux formater les données sur le niveau dans le form
        data['Niveau'][index] = 'exp'
    if row[column_list_csv[4]] == 'Intermédiaire' :
        data['Niveau'][index] = 'int'
    if row[column_list_csv[4]] == 'Débutant' :
        data['Niveau'][index] = 'deb'
    data['Taille'][index]=row[column_list_csv[5]]
    data['Poids'][index]=row[column_list_csv[6]]
    data['Ski'][index] = [row[column_list_csv[7+i]] for i in range(3)]
    data['Snowboard'][index] = [row[column_list_csv[11+i]] for i in range(3)]
    data['Chaussure ski'][index]=row[column_list_csv[10]]
    data['Chaussure snowboard'][index]=row[column_list_csv[14]]
    if row[column_list_csv[15]] == 'OUI' :
        data['Bâtons'][index] = 'Oui' 
    data['Casque'][index]=row[column_list_csv[16]]

for index, row in inv_csv.iterrows() : #Pour l'inventaire
    if not pd.isna(row['ski']) :
        data_inv['Ski'][index] = [row['ski'], row['taille_ski'], row['lvl_ski']]
    if not pd.isna(row['chaussure_ski']):
        data_inv['Chaussure ski'][index] = [row['chaussure_ski'], row['taille_ch_ski']]
    if not pd.isna(row['sb']) and not pd.isna(row['taille_sb']):
        data_inv['Snowboard'][index] = [row['sb'], row['taille_sb']]
    if not pd.isna(row['chaussure_sb']):
        data_inv['Chaussure snowboard'][index] = [row['chaussure_sb'], row['taille_ch_sb']]
    if not pd.isna(row['casque']):
        data_inv['Casque'][index] = [row['casque'], row['taille_casque']]

#Attribution des skis en fonction des choix

ski_used = []  

for s in range(n_participant) :
    if pd.isna(data['Ski'][s][0]) :
        data['Ski'][s] = data['Ski'][s][0]
        continue
    for i in range(2, -1, -1) : 
        if data['Ski'][s][i] in ski_used : 
            data['Ski'][s][i] = 'x'
    if set(data['Ski'][s]) == {'x'} : 
        data['Ski'][s] = 'x'
        continue
    for k in range(3) : 
        if data['Ski'][s][k] != 'x' : 
            ski_used.append(data['Ski'][s][k])
            data['Ski'][s] = data['Ski'][s][k]
            break

# Remplissage avec le reste de l'inventaire en fonction de la taille

for s in range(n_participant) :
    if pd.isna(data['Ski'][s]) :
        continue
    if data['Ski'][s] == 'x' : 
        for spec in data_inv['Ski'] : 
            if (spec[0] not in ski_used) and (data['Taille'][s] - 10 <= spec[1] <= data['Taille'][s]) and (data['Niveau'][s] == spec[2]) : 
                data['Ski'][s] = spec[0]
                ski_used.append(spec[0])
    if data['Ski'][s] == 'x' : 
        data['À Contacter ?'][s] = 'Oui'

#Attribution des snowboards en fonctions des choix

sb_used = []  

for s in range(n_participant) :
    if pd.isna(data['Snowboard'][s][0]) :
        data['Snowboard'][s] = data['Snowboard'][s][0]
        continue
    for i in range(2, -1, -1) : 
        if data['Snowboard'][s][i] in sb_used : 
            data['Snowboard'][s][i] = 'x'
    if set(data['Snowboard'][s]) == {'x'} : 
        data['Snowboard'][s] = 'x'
        continue
    for k in range(3) : 
        if data['Snowboard'][s][k] != 'x' : 
            sb_used.append(data['Snowboard'][s][k])
            data['Snowboard'][s] = data['Snowboard'][s][k]
            break

# Remplissage avec le reste de l'inventaire en fonction de la taille 
        
size_mapping_casque = {
    'XL': 0,
    'L': 1,
    'M': 2,
    'S': 3,
    'XS': 4
}

size_mapping_ch_ski = {
    '310' : 0,
    '305' : 1,
    '300' : 2,
    '295' : 3,
    '290' : 4,
    '285' : 5,
    '280' : 6,
    '275' : 7,
    '270' : 8,
    '265' : 9,
    '260' : 10,
    '255' : 11,
    '250' : 12,
    '245' : 13,
    '240' : 14,
    '235' : 15,
    '230' : 16,
}

size_mapping_ch_sb = {
    '37' : 0,
    '38' : 1,
    '39' : 2,
    '40' : 3,
    '41' : 4,
    '42' : 5,
    '43' : 6,
    '44' : 7,
    '45' : 8,
    '46' : 9,
}

# Attribution des casques 

c_used = []

for c in range(n_participant) :
    if data['Casque'][c] != 'NON' :
        size_needed = data['Casque'][c].split(' ')[-1].replace('(','').replace(')','')
        for spec in data_inv['Casque'] :
            if spec[0] not in c_used and spec[1] == size_needed:
                data['Casque'][c] = spec[0]
                c_used.append(spec[0])
                break
        if type(data['Casque'][c]) == str : 
            data['Casque'][c] = 'x ' + size_needed
            data['À Contacter ?'][c] = 'Oui'

# Attribution des chaussures de ski

ch_ski_used = []

for ch_ski in range(n_participant) :
    if not pd.isna(data['Chaussure ski'][ch_ski]) :
        size_needed = int(data['Chaussure ski'][ch_ski].split(' ')[0])
        for spec in data_inv['Chaussure ski'] :
            if (spec[0] not in ch_ski_used) and (spec[1] == size_needed):
                data['Chaussure ski'][ch_ski] = spec[0]
                ch_ski_used.append(spec[0])
                break
        if type(data['Chaussure ski'][ch_ski]) == str : 
            data['Chaussure ski'][ch_ski] = 'x ' + str(size_needed)
            data['À Contacter ?'][ch_ski] = 'Oui'

# Attribution des chaussures de snowboard
        
ch_sb_used = []

for ch_sb in range(n_participant) :
    if not pd.isna(data['Chaussure snowboard'][ch_sb]) :
        size_needed = data['Chaussure snowboard'][ch_sb]
        for spec in data_inv['Chaussure snowboard'] :
            if (spec[0] not in ch_sb_used) and (spec[1] == size_needed):
                data['Chaussure snowboard'][ch_sb] = spec[0]
                ch_sb_used.append(spec[0])
                break
        if data['Chaussure snowboard'][ch_sb] not in ch_sb_used : 
            data['Chaussure snowboard'][ch_sb] = 'x ' + str(size_needed)
            data['À Contacter ?'][ch_sb] = 'Oui'

# Renvoyer un excel en sortie

df = pd.DataFrame(data)  
df.to_excel('invSTRMAINE_final.xlsx', sheet_name='SG STRMAINE')  