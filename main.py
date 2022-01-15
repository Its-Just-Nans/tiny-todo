#!/bin/python3

"""
to-do list manager
"""

from pathlib import Path
import os.path
import json
import sys

HOME = str(Path.home())

todolist = os.path.join(HOME, ".todolist")

options = {}

for one_option in sys.argv:
    if "-v" in one_option or "--verbose" in one_option:
        options["v"] = True
    elif "add" in one_option:
        options["add"] = True
    elif "del" in one_option:
        options["del"] = True


def load(path_to_load):
    ''' Load the list from a file '''
    list_elements = []
    if os.path.isfile(path_to_load):
        with open(path_to_load, "r", encoding="utf-8") as file:
            try:
                list_elements = json.load(file)
            except json.JSONDecodeError:
                print("Error with the file")
    else:
        write_todolist(path_to_load, "[]")
    return list_elements


def write_todolist(todolist_path, list_elements):
    ''' Write list (as json) into file'''
    with open(todolist_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(list_elements))


def is_option(option_name):
    ''' Check if the option exists'''
    try:
        return bool(options[option_name])
    except KeyError:
        return False


def print_question(questions, answers):
    ''' Print a question to the console and return the index of the answer '''
    def possible_answer(to_check, answers):
        ''' Check possible answers in a table '''
        if to_check is False:
            return False
        index = False
        for index_in_list, one_answer in enumerate(answers):
            if "/" in one_answer:
                sub_answers = one_answer.split("/")
                for one_subanswer in sub_answers:
                    if to_check == one_subanswer:
                        index = index_in_list
                        break
            if to_check == one_answer:
                index = index_in_list
                break
        return index+1, index
    possible_choice = False
    while not possible_choice:
        print(questions)
        for one_answer in answers:
            if "/" in one_answer:
                print(one_answer.split("/")[0], end="")
            else:
                print(one_answer, end="")
            if one_answer == answers[-1]:
                print()
            else:
                print(" - ", end="")
        res = input()
        possible_choice, final_index = possible_answer(res, answers)
    return final_index


def add_item(list_elements):
    ''' Add a new item to the list '''
    res = input("Enter the new item\n")
    list_elements.append(res)
    write_todolist(todolist, list_elements)


def print_list(list_elements):
    '''' Print the list '''
    if len(list_elements) == 0:
        print("No elements in the list")
        if is_option("v"):
            res = print_question("Do you want to add an element ?",
                                 ["Yes/Y/y", "No/N/n"])
            {
                0: lambda: add_item(list_elements),
                1: sys.exit(),
            }[res]()
            sys.exit()
    print("Your TODO list is :")
    for index_of_element, one_element in enumerate(list_elements):
        print(f"{index_of_element} - {one_element}")


def delete_item(list_of_task):
    ''' Delete an item of the list '''
    print_list(list_of_task)
    res = print_question("Which element to delete ?", [
        str(x) for x in range(len(list_of_task))])
    del list_of_task[res]
    return list_of_task


def main():
    ''' main function '''
    list_of_task = load(todolist)
    if is_option("add"):
        add_item(list_of_task)
    if is_option("del"):
        list_of_task = delete_item(list_of_task)
        write_todolist(todolist, list_of_task)
        print_list(list_of_task)
    else:
        print_list(list_of_task)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit()
