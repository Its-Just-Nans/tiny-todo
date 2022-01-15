#!/bin/python3


from pathlib import Path
import os.path
import json
import sys

home = str(Path.home())

todolist = os.path.join(home, ".todolist")

options = {}

for oneOption in sys.argv:
    if "-v" in oneOption or "--verbose" in oneOption:
        options["v"] = True
    elif "add" in oneOption:
        options["add"] = True
    elif "del" in oneOption:
        options["del"] = True


def load(pathToLoad):
    listElements = []
    if os.path.isfile(pathToLoad):
        file = open(pathToLoad)
        try:
            listElements = json.load(file)
        except Exception as error:
            print("Error with the file")
    else:
        writeToDoList(pathToLoad, "[]")
    return listElements


def writeToDoList(todolist, listElements):
    file = open(todolist, "w")
    file.write(json.dumps(listElements))
    file.close()


def isOption(optionName):
    try:
        if options[optionName]:
            return True
        else:
            return False
    except KeyError:
        return False


def printQuestion(questions, answers):
    def possibleAnswer(toCheck, answers):
        if toCheck == False:
            return False
        index = False
        for indexInList, oneAns in enumerate(answers):
            if "/" in oneAns:
                subAnswers = oneAns.split("/")
                for oneSubAns in subAnswers:
                    if toCheck == oneSubAns:
                        index = indexInList
                        break
            if toCheck == oneAns:
                index = indexInList
                break
        return index+1, index
    possibleChoice = False
    while(not possibleChoice):
        print(questions)
        for oneAns in answers:
            if "/" in oneAns:
                print(oneAns.split("/")[0], end="")
            else:
                print(oneAns, end="")
            if oneAns != answers[-1]:
                print(" - ", end="")
        print()
        res = input()
        possibleChoice, finalIndex = possibleAnswer(res, answers)
    return finalIndex


def addItem(listElements):
    res = input("Enter the new item\n")
    listElements.append(res)
    writeToDoList(todolist, listElements)


def printList(listElements, options):
    if len(listElements) == 0:
        print("No elements in the list")
        if isOption("v"):
            res = printQuestion("Do you want to add an element ?",
                                ["Yes/Y/y", "No/N/n"])
            {
                0: lambda: addItem(listElements),
                1: lambda:  exit(),
            }[res]()
            exit()
    print("Your TODO list is :")
    for indexOfElement, oneElement in enumerate(listElements):
        print("{} - {}".format(indexOfElement, oneElement))


def deleteItem(listOfTask):
    printList(listOfTask, {})
    res = printQuestion("Which element to delete ?", [
                        str(x) for x in range(len(listOfTask))])
    del listOfTask[res]
    return listOfTask


def main():
    listOfTask = load(todolist)
    if isOption("add"):
        addItem(listOfTask)
    if isOption("del"):
        listOfTask = deleteItem(listOfTask)
        writeToDoList(todolist, listOfTask)
        printList(listOfTask, options)
    else:
        printList(listOfTask, options)


main()
