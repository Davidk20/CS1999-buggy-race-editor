# Testing  
Integration Testing - Testing multiple components  
Unit Test - Testing of single components  

There are two .py test files included in the package *'test_form_validation.py' and 'test_cost_method.py'* These can be run without the need for the webserver to be running as they test classes run from python files that are not the *'app.py'* file. Test cases that check all the below criteria are met. Providing all files are downloaded correctly, these can be run inititially to ensure all methods are working correctly before using the program. The tests are written using the unittest module and should print the following message if there were no errors.
*'Ran 4 tests in 0.018s*
*OK'*
A possible improvement that could have been made to the testing script would have been to create a class which could create random buggies in cases both valid and invalid according to game rules and, while this would be simple, the difficulty would come in writing the script which was able to not only identify which buggy cases should pass or fail what tests, but also to calculate the values independent from the script being tested to ensure calculations are correct. This is something I didn't see possible but it would have meant many more tests could be run
## Front End Testing  
There is no testing in the front end in this case as certain string manipulations and changes are made before being passed into validation functions and therefore it was more logical to run these tests in the back-end as it intergrated better with the program logic. However, certain features of the form do allow for potential errors to be removed before submittion and therefore do not need to be tested. Some of these are still tested for, however, as it could be possible for the user to still enter these if something goes wrong with formatting and therefore it ensures no chance for errors to slip through. These include:
  
- All inputs have been made 'required' in the html to ensure no field is left blank  
- Any input requiring a number has been changed to a number input instead of a text input  
 - Using this has allowed other criteria to be met such as only being able to choose even numbers larger than 4 for the number of wheels or a minimum of one for the quantity of primary fuel  
- The choice of colour is made using a colour input type and therefore no incorrect option can be given as the user cannot enter something that isn't a valid css colour.  

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