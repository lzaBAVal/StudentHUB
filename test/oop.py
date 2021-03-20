
class Dog:

    # Class attribute
    species = "Canis familiars"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def descr(self):
        return f'Dog name - {self.name}'

class JackRassel(Dog):
    def __str__(self):
        return f'I am JackRassel. My name is {self.name}'


ben = Dog('Ben', 12)
jack = JackRassel('Nona', 5)


print(ben.descr())
print(jack)