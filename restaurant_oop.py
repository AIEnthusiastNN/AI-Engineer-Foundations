"""

Object-Oriented Programming in Python: The Restaurant Story
Each section follows the order:
        1. Why OOP 
        2. Class & Object
        3. Attributes  
        4. __init__ and self
        5. Methods  
        6. Encapsulation  
        7. Inheritance  
        8. Polymorphism
        9. Abstraction  
        10. Composition

"""

from abc import ABC, abstractmethod


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


# ---------------------------------------------------------------
# 1. WHY OOP? - one function doing everything = spaghetti code
# ---------------------------------------------------------------
section("1. Why OOP? (spaghetti vs. roles)")


def run_restaurant_alone(order):
    # Ordering, cooking, cleaning all tangled in one place
    print(f"Taking order: {order}")
    print(f"Cooking: {order}")
    print("Cleaning up")


run_restaurant_alone("pasta")
# Change one thing and something else may quietly break.
# OOP fix: give every role (waiter, chef, cleaner) its own responsibility.


# ---------------------------------------------------------------
# 2. CLASS & OBJECT - a class is a blueprint, an object is built from it
# ---------------------------------------------------------------
section("2. Class & Object")


class Waiter:  # the blueprint
    pass


raj = Waiter()     # an object (a real staff member)
simran = Waiter()  # same blueprint, different object
print(type(raj), raj is simran)  # False -> two separate objects


# ---------------------------------------------------------------
# 3. ATTRIBUTES - class attributes are shared, instance attributes are not
# ---------------------------------------------------------------
section("3. Attributes (class vs. instance)")


class WaiterAttr:
    tables = []  # CLASS attribute: created once, visible to every object


raj = WaiterAttr()
simran = WaiterAttr()

# Neither has its own 'tables' yet -> both look at WaiterAttr.tables
print(raj.tables is WaiterAttr.tables)  # True

# Assigning creates a NEW attribute inside the object (class untouched)
raj.tables = [4, 5, 6]
simran.tables = [1, 2, 3]
print("Raj:", raj.tables)
print("Simran:", simran.tables)
print("Class:", WaiterAttr.tables)  # still empty

# Lookup order: 1) inside the object, 2) inside the class.

# The trap: forgetting to assign -> shared mutation!
a = WaiterAttr()
b = WaiterAttr()
a.tables.append(10)  # finds class attribute and MODIFIES it
print("b sees a's table:", b.tables)  # [10]  <- shared mutation
WaiterAttr.tables.clear()  # clean up for later sections


# ---------------------------------------------------------------
# 4. __init__ and self - every object automatically gets its own data
# ---------------------------------------------------------------
section("4. __init__ and self")


class WaiterInit:
    def __init__(self, name):
        self.name = name
        self.tables = []  # each object gets its OWN list


raj = WaiterInit("Raj")
simran = WaiterInit("Simran")
raj.tables.append(4)
print("Raj:", raj.tables, "| Simran:", simran.tables)  # no sharing
# 'self' simply means "this particular object".


# ---------------------------------------------------------------
# 5 & 6. METHODS and ENCAPSULATION - data + behavior together
# ---------------------------------------------------------------
section("5 & 6. Methods and Encapsulation")


class WaiterMethods:
    def __init__(self, name):
        self.name = name
        self.tables = []  # state: the object's current data

    def take_order(self, table):
        # The object changes its OWN data via a method
        self.tables.append(table)
        print(f"{self.name} took the order from table {table}")


raj = WaiterMethods("Raj")
simran = WaiterMethods("Simran")

raj.take_order(4)
raj.take_order(5)
simran.take_order(1)

print("Raj remembers:", raj.tables)        # [4, 5]
print("Simran remembers:", simran.tables)  # [1]
# Encapsulation: ask the object to change its data through a method,
# instead of modifying it from outside.


# ---------------------------------------------------------------
# 7. INHERITANCE - common things live in one place (Staff)
# ---------------------------------------------------------------
section("7. Inheritance")

#Base Class
class Staff:
    def __init__(self, name, shift):
        self.name = name
        self.shift = shift

    def start_work(self):
        print(f"{self.name} started the {self.shift} shift")

#Child Class
class WaiterInh(Staff):  # a waiter IS A staff member
    def take_order(self, table):
        print(f"{self.name} takes the order from table {table}")


class ChefInh(Staff):  # a chef IS A staff member
    def cook(self, dish):
        print(f"{self.name} is cooking {dish}")


raj = WaiterInh("Raj", "morning")
amit = ChefInh("Amit", "evening")

raj.start_work()   # defined once in Staff, works for both
amit.start_work()
raj.take_order(4)  # role-specific behavior
amit.cook("pasta")


# ---------------------------------------------------------------
# 8. POLYMORPHISM - same command, different behavior
# ---------------------------------------------------------------
section("8. Polymorphism")


class StaffPoly:
    def __init__(self, name):
        self.name = name

    def work(self):  # the "promise": every staff member can work
        print(f"{self.name} is working")


class WaiterPoly(StaffPoly):
    def work(self):  # overrides parent's version
        print(f"{self.name} is serving tables")


class ChefPoly(StaffPoly):
    def work(self):
        print(f"{self.name} is cooking food")


team = [WaiterPoly("Raj"), ChefPoly("Amit")]
for member in team:
    member.work()  # manager says "Everyone work!" - each object decides how
# Python checks the object's own class first, then the parent class.


# ---------------------------------------------------------------
# 9. ABSTRACTION - enforce what must exist, not how it's done
# ---------------------------------------------------------------
section("9. Abstraction")


class StaffAbstract(ABC):
    def __init__(self, name):
        self.name = name

    def start_work(self):  # shared behavior
        print(f"{self.name} started working")

    @abstractmethod
    def experience(self):  # the rule: every staff member MUST define this
        pass


class WaiterNoExp(StaffAbstract):
    def take_order(self):
        print(f"{self.name} takes an order")


# Python refuses to create an object that breaks the contract
try:
    WaiterNoExp("Raj")
except TypeError as e:
    print("Blocked by Python:", e)


class WaiterAbstract(StaffAbstract):
    def experience(self):  # contract satisfied
        return "2 years of experience"

    def take_order(self):
        print(f"{self.name} takes an order")


raj = WaiterAbstract("Raj")
raj.start_work()                   # from StaffAbstract
print(raj.name, "-", raj.experience())
raj.take_order()                   # waiter-specific


# ---------------------------------------------------------------
# 10. COMPOSITION - a waiter HAS A chef (not IS A chef)
# ---------------------------------------------------------------
section("10. Composition")


class Chef:
    def __init__(self, name):
        self.name = name

    def cook(self, dish):
        print(f"Chef {self.name} cooks {dish}")


class WaiterComp:
    def __init__(self, name, chef):
        self.name = name
        self.chef = chef  # has-a relationship

    def take_order(self, dish):
        print(f"{self.name} takes the order for {dish}")
        self.chef.cook(dish)  # forwards the work to the chef


amit = Chef("Amit")
raj = WaiterComp("Raj", amit)  # connect the two objects
raj.take_order("pasta")

# Inheritance = "is a"  (Waiter is a Staff)
# Composition = "has a" (Waiter has a Chef to work with)


# ---------------------------------------------------------------
# BONUS: everything together - a mini restaurant
# ---------------------------------------------------------------
section("Bonus: Putting it all together")


class Employee(ABC):                       # Abstraction + Inheritance base
    def __init__(self, name, shift):
        self.name = name                    # Encapsulation: own data
        self.shift = shift

    def start_work(self):
        print(f"{self.name} started the {self.shift} shift")

    @abstractmethod
    def experience(self): ...

    @abstractmethod
    def work(self): ...                     # Polymorphism


class Cook(Employee):
    def experience(self):
        return "5 years"

    def work(self):
        print(f"{self.name} is cooking")

    def cook(self, dish):
        print(f"{self.name} cooks {dish}")


class Server(Employee):
    def __init__(self, name, shift, cook):
        super().__init__(name, shift)
        self.cook_ref = cook                # Composition
        self.tables = []

    def experience(self):
        return "3 years"

    def work(self):
        print(f"{self.name} is serving tables")

    def take_order(self, table, dish):
        self.tables.append(table)
        print(f"{self.name} takes order from table {table}")
        self.cook_ref.cook(dish)


cook = Cook("Amit", "evening")
server = Server("Raj", "evening", cook)

for person in (server, cook):
    person.start_work()
    person.work()                           # same command, different behavior

server.take_order(4, "pasta")
print("Raj's tables:", server.tables)
