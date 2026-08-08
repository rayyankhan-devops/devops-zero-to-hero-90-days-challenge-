import os
import sys
import json


name="Rayyan"

unused_variable = 100


def greet(Name):
 print("Hello " + Name)
 return


def add(a,b):
    c=a+b
    return c


def divide(a,b):
    try:
        return a/b
    except:
        print("Error")


class person:

    def __init__(self,name,age):
        self.name=name
        self.age=age

    def display(self):
      print(f"{self.name} is {self.age} years old")


def process():
    numbers=[1,2,3,4,5]
    for i in range(len(numbers)):
        print(numbers[i])

    if len(numbers)>0:
        print("Not Empty")

    x = True
    if x == True:
        print("True")

    message="Lint me!"
    print(message)


if __name__=="__main__":
 greet(name)
 print(add(2,3))
 divide(10,0)

 p=person("Alice",25)
 p.display()
 process()
