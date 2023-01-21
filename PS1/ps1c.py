# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:59:17 2023

@author: Octavio Vega
"""

# portion of the cost of home needed for down payment
portion_down_payment = 0.25

# annual return on investments
r = 0.04

# semi-annual raise percentage
semi_annual_raise = 0.07

# total cost of the house we are saving for (in $)
total_cost = 10**6

def amount_saved(months, annual_salary, semi_annual_raise, portion_saved):
    '''
    Function to project future savings for fixed time period (in months)
        returns: amount saved after time (in $)
    '''
    monthly_salary = annual_salary/12
    current_savings = 0
    
    for m in range(months):
        current_savings += portion_saved*monthly_salary*(1 + semi_annual_raise) + current_savings*r/12
    return current_savings

# bisection search
def bisection_search(annual_salary, epsilon):
    num_guesses = 0
    low = 0.0
    high = 1.0
    guess = (low + high)/2.0

    # check for impossibility (i.e. even with max possible saving rate, not possible to save in time)
    if amount_saved(36, annual_salary, semi_annual_raise, 1.0) < portion_down_payment*total_cost:
        print("It is not possible to pay the down payment in three years with a salary of", annual_salary)
    else:
        while abs(amount_saved(36, annual_salary, semi_annual_raise, guess) - portion_down_payment*total_cost) >= epsilon:
            if amount_saved(36, annual_salary, semi_annual_raise, guess) < portion_down_payment*total_cost:
                low = guess
            else:
                high = guess
            guess = (low + high)/2.0
            num_guesses += 1
        print("Number of bisection steps:", num_guesses)
        print(guess, "is the best savings rate.")

# test cases
bisection_search(150000, 100)
bisection_search(300000, 100)
bisection_search(10000, 100)