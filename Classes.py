class Animals:
    def __init__(self,name):
        self.name = name
    
    def speak(self):
        pass

class Cat(Animals):
    def speak(self):
        return(f"{self.name} says meow")
    
class Dog(Animals):
    def speak(self):
        return(f"{self.name} says wolf")
    
dog_animal = Dog("Buddy")
cat_animal = Cat("Paula") 

animals = [dog_animal,cat_animal]
for animal in animals:
    print(animal.speak())
