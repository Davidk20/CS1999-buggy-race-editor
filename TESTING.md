# Testing  
There are two .py test files included in the package:

	'test_form_validation.py' and 'test_cost_method.py'
	
These should be run before initialising the webserver to ensure
that there are no errors with either the database or the functions.
These tests are run using the *unittest* module in python and should
print the following statement if the tests were successful:

	*'Ran 4 tests in 0.018s*
	*OK'*

Ideally, tests would have been run so that buggies were randomly created
by a function which would also be able to detect whether or not they were
valid, therefore being a completely random test. However, while a random
buggy generator is used in the *fill_form.py* method, it only generates
random buggies and then also would have to be validated to ensure it was
accurate before being used to generate tests. There is also no way to create
or verify buggies which should fail tests. Therefore in this case it 
is more logical to run custom tests to ensure all cases are met.



## Front End Testing  

There is no testing server-side as it is easier to run this in python
as python handles a majority of errors and user interaction due to
the configuration of my program.

There were certain cases where a potential error could be nulled
by changing the properties of elements in the form. This includes:

-  changing inputs from *text* type to different properties such as
   *color*, *number* or *select* 
- All inputs have been made 'required' in the html to ensure no field is left blank.  

This meant that the user could be limited to only allowed values
in the majority of cases, meaning that certain errors could be
prevented entirely without needing to be caught.


## Back End Testing  

The two test files mentioned above are run to ensure the following conditions are met during data manipulation before being inserted into the database:

- The number of wheels ('*qty_wheels*') on a buggy must be more than 4 and also an even number  
- The types of power (power_type and aux_power_type) must not be the same  
- The user can only select a quantity of 1 for fuels which are non-consumable  
- There must be a suitable amount of power (>=1) for each power type selected  
	- This can be ignored for the auxiliary power if only one power type is selected  
	- For buggies with a non-consumable power type, they should only be able to carry a quantity of 1 fuel  
- Two different, valid CSS colours must be chosen for the flag  
	- This maybe ignored if the flag pattern is *'plain'*  
- The number of tyres '*qty_tyres*' must be equal to or greater than the number of wheels  
	- '*qty_tyres >= qty_wheels*'  
- The *'cost_method.py'* file correctly calculates both the cost per unit and cost per kilogram of each buggy created
	- The cost of armour per unit and kg are increased by 10% for each wheel over the default 4  
		 - For example - a six-wheeled buggy would mean a 20% increase in cost of armour  
		 - This is calculated for in the *'cost_method.py'* file
