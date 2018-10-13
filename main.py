import random

class Individual:
  def __init__(self, number):
    self.original_number = number
    self.function_result = self.run_function(number)
    self.individual_in_bits = self.convert_to_bits(number)
    self.probability = 0
  
  def convert_to_bits(self,number):
    if (number >= 0):
      return "0"+'{0:04b}'.format(number)
    return "1"+'{0:04b}'.format(number*-1)

  def run_function(self,x):
    return (x*x - 3*x + 4)

  def get_function_result(self):
    return self.function_result
  
  def set_probability(self,probability):
    self.probability = probability
  
  def set_individual_in_bits(self,bits):
    self.individual_in_bits = bits
  
  def get_probability(self):
    return self.probability
  
  def get_individual_in_bits(self):
    return self.individual_in_bits
  
  #Operator overloading to make crossover
  def __add__(self, individual2):
    if (random.random() < 0.7):
      random_cut = random.randint(1,4)
      first_part_individual = self.individual_in_bits[0:random_cut]
      second_part_individual1 = self.individual_in_bits[random_cut:5]
      
      individual2_bits = individual2.get_individual_in_bits()
      
      first_part_individual2 = individual2_bits[0:random_cut]
      second_part_individual2 = individual2_bits[random_cut:5]

      first_son = first_part_individual + second_part_individual2
      second_son = first_part_individual2 + second_part_individual1

      return [first_son, second_son] 
    return None
  

class GeneticAlgorithm:
  def __init__(self):
    self.NUMBER_OF_GENERATIONS = 20
    self.individuals = self.generate_initial_population() 
    # self.run_tournament()
    # self.run_crossover(self.individuals[0],self.individuals[1])
    self.run_mutation()

  def run(self):
    self.individuals = self.generate_initial_population()
    self.set_probabilities()
    current_generation = 0
    while current_generation < self.NUMBER_OF_GENERATIONS:
      first_sample = self.run_tournament()
      second_sample = self.run_tournament()
      while first_sample == second_sample:
        second_sample = self.run_tournament
      first_son,second_son = self.run_crossover(first_sample,second_sample)
      self.run_mutation()
      #TODO: End algorithm 

  #Generate initial population with 30 individuals between -10 and 10
  def generate_initial_population(self):
    #List of individuals objects
    individuals_list = []
    while (len(individuals_list) < 30):
      randomNumber = random.randrange(-10,10)
      individuals_list.append(Individual(randomNumber))
    return individuals_list

  #Set the probabilities of each individual 
  def set_probabilities(self):
    sum_individuals = 0
    for individual in self.individuals:
      sum_individuals += individual.get_function_result()
      individual.set_probability(0)
    
    for individual in self.individuals:
      probability = individual.get_function_result()/sum_individuals
      individual.set_probability(probability)
  
  #Get two random individuals and see which one has the greater probability
  def run_tournament(self):
    sample1, sample2 = random.sample(self.individuals, 2)
    if sample1.get_probability() > sample2.get_probability():
      return sample1
    return sample2
  
  #TODO: Verify crossover criteria
  def run_crossover(self, individual1, individual2):
    return individual1 + individual2
  
  def run_mutation(self):
    for individual in self.individuals:
      individual_bits = individual.get_individual_in_bits()
      bits_after_mutation = ""
      for bit in individual_bits:
        if random.random() < 0.01:
          bits_after_mutation += "0" if bit == "1" else "1"
        else:
          bits_after_mutation += bit
      individual.set_individual_in_bits(bits_after_mutation)

if __name__ == "__main__":
  GeneticAlgorithm()