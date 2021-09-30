
import unittest

# Your name: Ajaeya Masti
# Your student id: 77624247
# Your email: ajmasti@umich.edu
# List who you have worked with on this homework:

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings
    
    def process_order(self, name, quantity):
        if name in self.inventory.keys():
            self.inventory[name] -= quantity
            self.earnings += self.cost * quantity
    
    def has_item(self, name, quantity):
        if name in self.inventory.keys():
            if self.inventory[name] >= quantity:
                return True
            else:
                return False
        else:
            return False

    def stock_up(self, name, quantity):
        if name in self.inventory.keys():
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

    def compute_cost(self, quantity):
        total = self.cost * quantity
        return total

    def __str__(self):
        return "Hello, we are " + self.name + ". This is the current menu " + self.inventory + ". We charge $" + self.cost + " per item. We have $" + self.earnings + " in total."


class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(self.s1.has_item(("Pancake"), 2))
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s2.has_item(("Burger"), 41))
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s2.has_item(("Burger"), 10))

	# Test validate order
    def test_validate_order(self):
        inventory2 = {"Burger":1}
        self.s4 = Stall("Empty Stall", inventory2)
        self.c1.add_stall(self.s4)
        self.s5 = Stall("Lone Stall", inventory2)
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.f1.validate_order(self.c1, self.s1, "Burger", 30)
        self.assertEqual(self.f1.wallet, 100)
		# case 2: test if the stall doesn't have enough food left in stock
        self.f2.validate_order(self.c1, self.s4, "Burger", 2)
        self.assertEqual(self.f2.wallet, 150)
		# case 3: check if the cashier can order item from that stall
        self.f2.validate_order(self.c1, self.s5, "Burger", 5)
        self.assertEqual(self.f2.wallet, 150)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.f1.reload_money(25)
        self.assertEqual(self.f1.wallet, 125)
    
### Write main function
def main():
    #Create different objects 
    i1 = {"Pizza":20, "Calzone":10, "Pasta":15}
    i2 = {"Steak":30, "Chicken":20, "Fish":10}
    f1 = Customer("Ajaeya", 110)
    f2 = Customer("Sally", 200)
    f3 = Customer("Jack", 50)
    s1 = Stall("Papa John's", i1, cost = 8)
    s2 = Stall("Fine Dining", i2, cost = 15)
    c1 = Cashier("Ben", directory = [s1])
    c2 = Cashier("Bob", directory = [s2])


    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    f1.validate_order(c1, s2, "Pizza", 5)
    f2.validate_order(c2, s1, "Pizza", 5)
    f3.validate_order(c1, s2, "Pizza", 5)
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    f1.validate_order(c1, s1, "Calzone", 11)
    f2.validate_order(c2, s2, "Fish", 15)
    f3.validate_order(c1, s1, "Pizza", 21)
    #case 3: the customer does not have enough money to pay for the order: 
    f1.validate_order(c1, s1, "Pasta", 14)
    f2.validate_order(c2, s2, "Steak", 29)
    f3.validate_order(c2, s2, "Fish", 7)
    #case 4: the customer successfully places an order
    f1.validate_order(c2, s2, "Chicken", 2)
    f2.validate_order(c1, s1, "Pizza", 3)
    f3.validate_order(c2, s2, "Fish", 3)
    

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
