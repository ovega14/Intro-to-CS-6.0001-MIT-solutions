# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:52:48 2023

@author: Octavio Vega
"""

class SavingsPlan:
    
    def __init__(self, portion_down_payment, r, total_cost, semi_annual_raise, 
                 annual_salary, portion_saved):
        self.portion_down_payment = portion_down_payment
        self.r = r
        self.total_cost = total_cost
        self.semi_annual_raise = semi_annual_raise
        self.annual_salary = annual_salary
        self.portion_saved = portion_saved
        
    
    def time_to_save(self):
        '''
        function to calculate how many months it will take to save up 
        enough money for a down payment
        '''
        # total down payment needed
        down_payment = self.portion_down_payment * self.total_cost
        
        # monthly salary
        monthly_salary = self.annual_salary/12
        
        # amount saved thus far (in $)
        current_savings = 0
        
        # iterate forward over months and accumulate total savings
        month = 0
        while current_savings < down_payment:
            # account for salary increases
            if month % 6 == 0 and month != 0:
                monthly_salary += self.semi_annual_raise*monthly_salary
            else:
                pass
            
            # increase current savings by saved amount and ROI
            current_savings += self.portion_saved*monthly_salary + current_savings*self.r/12
            month += 1
        return month
        
    
    def test_time():
        case1b_pars = [0.25, 0.04, 500000, 0.03, 120000, 0.05]
        case2b_pars = [0.25, 0.04, 800000, 0.03, 80000, 0.10]
        case3b_pars = [0.25, 0.04, 1500000, 0.05, 75000, 0.05]
        
        if SavingsPlan(*case1b_pars).time_to_save() == 142:
            print("Test Case 1B passed")
        elif SavingsPlan(*case1b_pars).time_to_save() != 142:
            print("Test Case 1B failed")
        if SavingsPlan(*case2b_pars).time_to_save() == 159:
            print("Test Case 2B passed")
        elif SavingsPlan(*case2b_pars).time_to_save() != 159:
            print("Test Case 2B failed")
        if SavingsPlan(*case3b_pars).time_to_save() == 261:
            print("Test Case 3B passed")
        elif SavingsPlan(*case3b_pars).time_to_save() != 261:
            print("Test Case 3B failed")

PlanB = SavingsPlan
PlanB.test_time()     
