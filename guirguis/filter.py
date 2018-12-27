#!/usr/bin/env python3
"""Custom filters"""

from typing import List, Callable, Dict


def _condition_indexing(data: str, condition_list: dict, ordered_list):
    """return indexed conditions"""
    for i in ordered_list:
        if condition_list[i]["test"](data):
            return i


def filter_dict(input_list: List[str], fdict: Dict[str, dict], ordered_list: List[str]):
    """Filters input array into a dictioary

    Rearanges a list of inputs into a dictionary based on
    the first test to evaluate to true.

    Args:
        input_list: list of strings to be filtered.
        list_of_filters: test functions
    Returns:
        A dictionary
    """
    for t in input_list:
        fdict[_condition_indexing(t, fdict, ordered_list)]["data"].append(t)


def _condition_index(data, condition_list):
    """return index of successful condition"""
    for i, cond in enumerate(condition_list, 0):
        if cond(data):
            return i
    return len(condition_list)


def filter_list(input_list: List[str], list_of_filters: List[Callable[[str], bool]]):
    """Filters input array into an 2-dimentional array

    Rearanges a list of inputs into a 2-dimentional output array based on
    the index of a first test to evaluate to true.

    Args:
        input_list: list of strings to be filtered.
        list_of_filters: test functions; order is significant.
    Returns:
        A 2-dimentional list of strings.
    """
    start_list = [[] for n in range(len(list_of_filters) + 1)]
    for t in input_list:
        start_list[_condition_index(t, list_of_filters)].append(t)
    return start_list
