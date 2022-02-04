import os 
import random
import numpy as np

path = r'C:\Users\Riccardo\Desktop\Hashcode 2022\Sample problem\inputs'
path_save = r'C:\Users\Riccardo\Desktop\Hashcode 2022\Sample problem\results'

def evaluate_population(population,clients_like,clients_dislike):
    evaluations = np.zeros((1,population.shape[0]))
    for i in range(population.shape[0]):
        tot = 0 
        for j in range(clients_like.shape[0]):
            if(np.sum(population[i]*clients_like[j])==np.sum(clients_like[j]) and np.sum(population[i]*clients_dislike[j])==0):
                tot+=1
        evaluations[0,i]=tot
    
    return evaluations, population[np.argmax(evaluations,axis=1),:], evaluations[0,np.argmax(evaluations,axis=1)]

def create_population(n_,n_ingredients):
    # Create random lists of ingredients
    population = np.zeros((n_,n_ingredients))
    for i in range(n_):
        # Get number of ingredients 
        n_ing = random.randint(1,n_ingredients)
        random_indexes = np.random.choice([i for i in range(n_ingredients)],n_ing,replace=False)
        population[i,random_indexes] = 1
    
    return population

def select_best(population,evaluations):
    new_population = np.zeros((population.shape))
    weights = evaluations/(np.sum(evaluations))
    random_indexes = np.random.choice([i for i in range(population.shape[0])],population.shape[0],replace=True,p=np.reshape(weights,(-1,)))
    
    new_population[random_indexes,:] = population[random_indexes,:]
    
    return new_population

def mutate(population,n_mutations):
    for _ in range(n_mutations):
        # change random ingredient(s)
        individual_to_change = random.randint(0,population.shape[0]-1)
        random_indexes = np.random.choice([i for i in range(population.shape[1])],1,replace=False)
        for i in random_indexes:
            population[individual_to_change,i] = not population[individual_to_change,i]
            
    return population


if __name__ == "__main__":
    for file in os.listdir(path):
        print('Processing file ',file)
        input_path = os.path.join(path,file)
        
        with open(input_path,'r') as fileopen:
            lines = fileopen.readlines()
        fileopen.close()
        
        n_clients = int(lines[0])
        # Get total number of ingredients 
        ingredients = []
        for line in lines[1:]:
            pieces = line.replace('\n','').split(' ')
            for ingredient in pieces[1:]:
                if(ingredient not in ingredients):
                    ingredients.append(ingredient)   

        clients_like = np.zeros((n_clients,len(ingredients)))
        clients_dislike = np.zeros((n_clients,len(ingredients)))
        
        
        for z in range(n_clients):
            pieces = lines[z*2+1].replace('\n','').split(' ')
            clients_like[z,:] = [1 if ingredient in pieces else 0 for ingredient in ingredients]
            pieces = lines[z*2+2].replace('\n','').split(' ')
            clients_dislike[z,:] = [1 if ingredient in pieces else 0 for ingredient in ingredients]
        
        output_best = 0
        output_ingredients_coded = 0
        population = create_population(1,len(ingredients))
        #print(population)
        i=0
        while True:
            scores, best_ingredients, best_result = evaluate_population(population,clients_like,clients_dislike)
            #population = select_best(population,scores)
            population = mutate(population,n_clients)
            if(best_result>output_best):
                output_best = best_result
                output_ingredients_coded = best_ingredients
                i=0
            print(output_best)
            i+=1
            if(best_result==output_best and i>1000):
                break


        output_ingredients = [ingredients[i] for i in range(len(ingredients)) if output_ingredients_coded[0][i]==1]
        print(output_ingredients)

        # Save the final ingrediens 
        with open(os.path.join(path_save,file),'w') as fileout:
            fileout.write(str(len(output_ingredients)))
            for ingredient in output_ingredients:
                fileout.write(' '+ingredient)
        fileout.close()



        

            