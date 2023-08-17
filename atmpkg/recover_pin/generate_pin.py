# Define the Pin class
pin = int
pin_length = int
class Pin:
    def __init__(self, pin_length):
        self.pin_length = pin_length

    def generate_pin(self):
        pass

    def verify_pin(self, pin):
        pass
#Implement the Pin class
from random import randint

class Pin:
    def __init__(self, pin_length):
        self.pin_length = pin_length

    def generate_pin(self):
        pin = ""
        for _ in range(self.pin_length):
            pin += str(randint(0, 9))
        return pin

    def verify_pin(self, pin):
        return pin.isdigit() and len(pin) == self.pin_length
    
    
# ## Test, how create a Pin object with a pin length of X and show generated pin by console
# pin = Pin(4)

# # Generate a pin
# generated_pin = pin.generate_pin()

# # Print the generated pin
# print("Generated pin:", generated_pin)


