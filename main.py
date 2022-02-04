import os 
import random
import numpy as np

path = r'C:\Users\Riccardo\Desktop\Altri progetti\Hashcode2022_ONEpizza\inputs'
path_save = r'C:\Users\Riccardo\Desktop\Altri progetti\Hashcode2022_ONEpizza\results'

def evaluate_population(population,clients_like,clients_dislike):
    # Population now is a vector! 
    all_likes = np.sum(clients_like,axis=1)
    all_likes = np.vstack([all_likes.reshape(1,-1)]*population.shape[0])
    clients_like = np.dot(population,clients_like.T)
    clients_dislike = np.dot(population,clients_dislike.T)
    clients_dislike = (clients_dislike==0)
    clients_like = np.equal(clients_like,all_likes)
    evaluation = clients_like.astype(int)*clients_dislike.astype(int)
    evaluation = np.sum(evaluation,axis=1)
    best_score = np.max(evaluation)
    best_ingredients = population[np.argmax(evaluation),:]
    
    return best_score, best_ingredients

def create_population(n_,n_ingredients):
    # Create random lists of ingredients
    return np.random.randint(low=0,high=2,size=(n_,n_ingredients))

def select_best(population,evaluations):
    new_population = np.zeros((population.shape))
    weights = evaluations/(np.sum(evaluations))
    random_indexes = np.random.choice([i for i in range(population.shape[0])],population.shape[0],replace=True,p=np.reshape(weights,(-1,)))
    
    new_population[random_indexes,:] = population[random_indexes,:]
    
    return new_population

def mutate(population):
    # change random ingredient
    random_index = np.random.choice([i for i in range(population.shape[1])],1)
    population[0,random_index] = not population[0,random_index]
    
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
        population = create_population(10000,len(ingredients))
        i=0
        while True:
            score, best_ingredients = evaluate_population(population,clients_like,clients_dislike)
            if(score>output_best):
                output_best = score
                output_ingredients_coded = best_ingredients
                i=0
                print(score)

            population = create_population(10000,len(ingredients))
            i+=1
            
            if(score==output_best and i>100000):
                break


        output_ingredients = [ingredients[i] for i in range(len(ingredients)) if output_ingredients_coded[i]==1]

        # Save the final ingrediens 
        with open(os.path.join(path_save,file),'w') as fileout:
            fileout.write(str(len(output_ingredients)))
            for ingredient in output_ingredients:
                fileout.write(' '+ingredient)
        fileout.close()



        

            