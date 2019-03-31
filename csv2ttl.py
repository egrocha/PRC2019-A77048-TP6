#!/usr/bin/env python3
# coding=utf-8

import csv

fregs = 'datasets/freguesias-metadata.csv'
globalDict = {}

with open(fregs, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line = 0
    for row in csv_reader:
        if not (row['distrito'] in globalDict):
            distritoDict = {}
            distritoDict[row['concelho']] = []
            distritoDict[row['concelho']].append(row['freguesia'])
            globalDict[row['distrito']] = distritoDict
        else:
            concelhos = globalDict[row['distrito']]
            if not (row['concelho'] in concelhos):
                concelhos[row['concelho']] = []
                concelhos[row['concelho']].append(row['freguesia'])
                globalDict[row['distrito']] = concelhos
            else:
                freguesias = concelhos[row['concelho']]
                freguesias.append(row['freguesia'])
                concelhos[row['concelho']] = freguesias
                globalDict[row['distrito']] = concelhos
        line += 1

distCount = g_cidadeCount = g_fregCount = 0
a_cidadeCount = a_fregCount = 0

for key in globalDict:
    distCount += 1
    distritoDict = globalDict[key]

    for cidade in distritoDict:
        g_cidadeCount += 1
        a_cidadeCount += 1
        lstFreg = distritoDict[cidade]

        for freg in lstFreg:
            g_fregCount += 1
            a_fregCount += 1
            print('\n###  http://prc.di.uminho.pt/2019/mapa#F' + str(g_fregCount))
            print(':F' + str(g_fregCount) + ' rdf:type owl:NamedIndividual,\n :Freguesia ;\n :nome \"' + freg + '\".')

        print('\n###  http://prc.di.uminho.pt/2019/mapa#C' + str(g_cidadeCount))
        print(':C' + str(g_cidadeCount) + ' rdf:type owl:NamedIndividual,\n :Cidade ;\n :pertenceDistrito :D' + str(distCount) 
                + ' ;\n :nome \"' + cidade + '\" ;\n :populacao \"10000\" ;\n :temFreguesia ', end='')

        while a_fregCount > 1:
            print(':F' + str(g_fregCount - a_fregCount + 1) + ', ', end='')
            a_fregCount -= 1
        print(':F' + str(g_fregCount - a_fregCount + 1) + ' .\n')
        a_fregCount = 0
    
    print('\n###  http://prc.di.uminho.pt/2019/mapa#D' + str(distCount))
    print(':D' + str(distCount) + ' rdf:type owl:NamedIndividual,\n :Distrito ;\n :pertencePaís :pt ;\n :nome \"' + key + '\" ;\n :temCidade ', end='')
    
    while a_cidadeCount > 1:
        print(':C' + str(g_cidadeCount - a_cidadeCount + 1) + ', ', end='')
        a_cidadeCount -=1
    
    print(':C' + str(g_cidadeCount - a_cidadeCount + 1) + ' .\n')
    
a_cidadeCount = 0