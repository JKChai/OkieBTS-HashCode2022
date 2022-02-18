# mydict = dict()
# key = "KEY"
# listOfValues = ["1" , "2", "3"]
# mydict.setdefault(key, [])
# mylist = [1, 2, 3, 4, 5, 6, 7]
# for e in mylist:
#     print(e)
#     if e == 1:
#         mylist.remove(6)
#         mylist.remove(5)

class Test:
    name = ""
    age = 123
    address = ""
    
someDict = dict()

obj = Test()
obj.name = "Hello"
someDict["some"] = obj

print(someDict["some"].name)