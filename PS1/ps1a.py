# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:27:13 2023

@author: Octavio Vega
"""

# portion of the cost of home needed for down payment
portion_down_payment = 0.25

# monthly return on investments
r = 0.04

def time(annual_salary, portion_saved, total_cost):
    '''
    function to calculate how many months it will take to save up 
    enough money for a down payment
    '''
    
    # total down payment needed
    down_payment = portion_down_payment * total_cost
    
    # monthly salary
    monthly_salary = annual_salary/12
    
    # amount saved thus far (in $)
    current_savings = 0
    
    # iterate forward over months and accumulate total savings
    month = 0
    while current_savings < down_payment:
        current_savings += portion_saved*monthly_salary + current_savings*r/12
        month += 1
    return month

# test cases
print(time(120000, 0.10, 1000000))
print(time(80000, 0.15, 500000))
