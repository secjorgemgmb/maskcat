import pandas as pd
import json

def count_generations_repetitions (csvFile:str, outputFile:str):
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
    fd = open(outputFile, "w")
    json.dump(count, fd)
    fd.close()

def get_arrays_generations(csvFile:str, outputFileCSV:str, outputFileJSON:str):
    # Gets array solutions in one line by generation
    historico = pd.read_csv(csvFile, sep=";")
    historicoJSON = {}
    generationLine = []
    generationPreviousLine = []
    newSolutions = []
    fd = open(outputFileCSV, "w")
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
    fd2 = open(outputFileJSON, "w")
    json.dump(historicoJSON, fd2)
    fd2.close()

# for i in range(0, 30):
#     csvFile = "../results/2022-04-02/maskcatHistory_maskcat_2022-04-02_rep{}.csv".format(i)
#     outputFile1 = "../measurements/2022-04-02/repeticiones/repeticiones_maskcat_2022-04-02_rep{}.json".format(i)
#     outputFile2 = "../measurements/2022-04-02/generaciones_por_fila/generationByRow_maskcat_2022-04-02_rep{}.csv".format(i)
#     outputFile3 = "../measurements/2022-04-02/generaciones_por_fila/generationByRow_maskcat_2022-04-02_rep{}.json".format(i)
#     count_generations_repetitions(csvFile, outputFile1)
#     get_arrays_generations(csvFile, outputFile2, outputFile3)

csv_file = "../experiments/maskcat_population100_2022-04-26/results/maskcatHistory.csv"
output_file1 = "../experiments/maskcat_population100_2022-04-26/post-processed/repeticiones.json"
output_file2 = "../experiments/maskcat_population100_2022-04-26/post-processed/generationByRow.csv"
output_file3 = "../experiments/maskcat_population100_2022-04-26/post-processed/generationByRow.json"
count_generations_repetitions(csv_file, output_file1)
get_arrays_generations(csv_file, output_file2, output_file3)