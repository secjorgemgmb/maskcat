import pandas as pd
import json

def countGenerationsRepetitions (csvFile:str):
    # Counts repetitions of solutions by generations
    historico = pd.read_csv(csvFile, sep=";")
    historico["Mask"] = historico["Mask"].fillna("_")
    count = {}
    for i in range (1, historico["Generacion"].max()+1):
        generation = historico.loc[historico["Generacion"]==i]
        generation_counter = {}
        for index, row in generation.iterrows():
            if row["Mask"] in generation_counter:
                generation_counter[row["Mask"]] = generation_counter[row["Mask"]] + 1
            else:
                generation_counter[row["Mask"]] = 1
        count[i] = generation_counter
    fd = open("../measurements/prueba.json", "w")
    json.dump(count, fd)
    fd.close()

def getArraysGenerations(csvFile:str):
    # Gets array solutions in one line by generation
    historico = pd.read_csv(csvFile, sep=";")
    historicoJSON = {}
    generationLine = []
    generationPreviousLine = []
    newSolutions = []
    fd = open("../measurements/generations_by_row.csv", "w")
    fd.write("Generation;Array solutions;New solutions\n")
    for i in range (1, historico["Generacion"].max()+1):
        generation = historico.loc[historico["Generacion"]==i]
        for index, row in generation.iterrows():
            generationLine.append(row["Array"])
        
        if i > 1:
            for solution in generationLine:
                if solution not in generationPreviousLine:
                    newSolutions.append(solution)
        fd.write("{};{};{}\n".format(i, generationLine, newSolutions))
        historicoJSON[i]={"Array solutions":generationLine, "New solutions":newSolutions}
        generationPreviousLine = generationLine
        generationLine = []    
        newSolutions = []
    fd.close()
    fd2 = open("../measurements/generations_by_row.json", "w")
    json.dump(historicoJSON, fd2)
    fd2.close()

# countGenerationsRepetitions("../results/2022-03-26/maskcatHistory_maskcatLoop_0pred_2022-03-26_rep0.csv")
getArraysGenerations("../results/2022-04-02/maskcatHistory_maskcat_2022-04-02_rep0.csv")