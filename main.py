import random

class Individual:
  def __init__(self, number):
    self.decimal_number = number
    self.function_result = self.run_function(number)
    self.individual_in_bits = self.convert_to_bits(number)
    self.probability = 0
  
  def convert_to_bits(self,number):
    if (number >= 0):
      return "0"+'{0:04b}'.format(number)
    return "1"+'{0:04b}'.format(number*-1)

  def run_function(self,x):
    return (x*x - 3*x + 4)
  
  def set_probability(self,probability):
    self.probability = probability
  
  def set_individual_in_bits(self,bits):
    self.individual_in_bits = bits
  
  def set_decimal_number(self,number):
    self.decimal_number = number
  
  def set_function_result(self,number):
    self.function_result = number
  
  def get_function_result(self):
    return self.function_result
  
  def get_probability(self):
    return self.probability
  
  def get_individual_in_bits(self):
    return self.individual_in_bits
  
  def get_decimal_number(self):
    return self.decimal_number
  
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
    self.NUMBER_OF_GENERATIONS = 20000
    self.run()

  def run(self):
    self.individuals = self.generate_initial_population()
    for individual in self.individuals:
      print(individual.get_decimal_number(), end="->")
    print("end")
    current_generation = 0
    while current_generation < self.NUMBER_OF_GENERATIONS:
      self.set_probabilities()
      first_sample = self.run_tournament()
      second_sample = self.run_tournament()
      while first_sample == second_sample:
        second_sample = self.run_tournament()
      self.run_crossover(first_sample,second_sample)
      self.run_mutation()
      self.normalize()
      current_generation += 1
    
    for individual in self.individuals:
      print(individual.get_decimal_number(), end="->")

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
    
    for individual in self.individuals:
      probability = individual.get_function_result()/sum_individuals
      individual.set_probability(probability)
  
  #Get two random individuals and see which one has the greater probability
  def run_tournament(self):
    sample1, sample2 = random.sample(self.individuals, 2)
    if sample1.get_probability() > sample2.get_probability():
      return sample1
    return sample2
  
  #Make the crossover between two individulas
  def run_crossover(self, individual1, individual2):
    response = individual1 + individual2
    if response == None:
      return
    else:
      first_son, second_son = response
    individual1_index = self.individuals.index(individual1)
    individual2_index = self.individuals.index(individual2)
    self.individuals[individual1_index].set_individual_in_bits(first_son)
    self.individuals[individual2_index].set_individual_in_bits(second_son)
  
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
  
  def normalize(self):
    for individual in self.individuals:
      individual_bits = individual.get_individual_in_bits()
      first_bit = individual_bits[0]
      integer = int(individual_bits[1:5], 2)
      if integer > 10:
        integer = 10
        individual_bits = first_bit + "1010"
      if first_bit == 1:
        integer *= -1
      individual.set_decimal_number(integer)
      individual.set_function_result(individual.run_function(integer))
      individual.set_individual_in_bits(individual_bits)
      individual.set_probability(0)

if __name__ == "__main__":
  GeneticAlgorithm()
