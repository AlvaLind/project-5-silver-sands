## Manual Testing

### General Testing

| Action | Expected results | Yes/No | Comments |
|--------|-----------------|--------|----------|
| Verify that the homepage loads correctly.| The page should load with all elements (logo, navigation bar and images). | Yes |  |
| Check the responsiveness on different devices (desktop, tablet, mobile). | The website should change images and styles to accomodate smaller screens | Yes |  |
| Ensure all navigation links work. | All the links should direct to the correct pages. | Yes |  |
| Test the dropdown menus and links within them. | Drop downs like navbar, status update, and filter function should redirect, update and filter. | Yes |  |


## User Testing
| Action | Expected results | Yes/No | Comments |
|--------|-----------------|--------|----------|
|  | Sign Up |  |  |
| Click on "Sign up" in the navbar. | User should get redirected to Sign up page. | Yes |  |
| Enter valid username. | Username has to be unique. | Yes |  |
| Enter valid emailadress. | Field will only accept email address format. | Yes |  |
| Enter valid password. | Field will only accept secure passwords, must contain at least 8 characters and it can't be entirely numeric. | Yes |  |
| Enter valid password confirmation. | Field will only accept the same password from the previous field. | Yes |  |
| Click on the Sign Up button. | User should see a message informing that they have to confirm the emailaddress through the link that has been sent to their email. | Yes |  |
|  | Log in |  |  |
| Click on Login in the navbar| User should get redirected to Login page. | Yes |  |
| Enter valid username. | Field will only accept a valid username | Yes |  |
| Enter valid password. | Field will only accept a valid password to the username. | Yes |  |
| Click on the Sign In button | User should be redirected to the homepage with a confirmation message saying that they are logged in.| Yes |  |
| Click on "Forgot Password?" | User should be asked to input their emailaddress so that a recoverylink may be sent to the user to change password.| Yes |  |
|  | Log out |  |  |
| Click Log out from navbar| User should get redirected to a log out page to confirm logout. | Yes |  |
| Click "Logout" button in the center of the page. | Redirects user to home page. | Yes |  |
| Click browser back button. | User should still be logged out from the account. | Yes |  |
|  | Navbar |  |  |
| Click on "Silver Sands" logo§. | User should be taken to the home page. | Yes | Available to everyone. |
| Click on "All Wines". | User should get taken to the product list page with all wines. | Yes | Available to everyone. |
| Click on "Our Story". | User should be taken to the "Our Story" page. | Yes | Available to everyone. |
| Click on "Visit Us". | User should be taken to the "Visit Us" page. | Yes | Available to everyone. |
| Click on the "magnifying glass". | The searchbar should open and the eser should be able to start typing to search for their preferred wine. | Yes | Available to everyone. |
| Click on the "user profile" icon. | User should be taken to their user profile and order history. | Yes | Only available to registered users. |
|  | All Wines page |  |  |
| Click on "Filter by". | User should be able to filer the list on category,price and availability | Yes | |
| Click on "next". | There should only be 9 winebottles per page. When clicking next user should get redirected to the next page of wines. | Yes |  |
| Click on "prev" | The user should get taken back to the previous page of wines. | Yes |  |
| Click on a wine | User should get taken to the wine details page. | Yes |  |
|  | Wine details |  |  |
| Click on the heart icon. | The wine bottle should get added to the users favourites and the heart icon should be filled in with red. | Yes | Only available to registered users. | 
| Click on the filled red heart. | The wine should get removed from the favourites and the icon update to a "empty" heart. | Yes | Only available for registered users. |
| Leave a review | User can leave a review on the winebottle. | Yes | Only available for registered users. | 
| Click "Submit" to submit the review. | Inofrmation saying that the review is awaiting approval should appear and the user can then see their pending review on the page. | Yes | Only available for registered users. |
| Click "Edit" button on review. | The user should be able to edit their review. If the review has already been approved the changes will have to await approval. The timestamp of the comment will update. | Yes | Only available for registered users. |
| Click "Delete" button on review. | There will be a pop-up asking you to verify that the review should be deleted. | Yes | Only available for registered users. |
| Click "Close" on the pop-up | The pop-up will close and the review will not be deleted. | Yes | Only available for registered users. |
| Click "delete" on the pop-up. | The review will be deleted. | Yes | Only available for registered users. |
| An avarage star rating per wine bottle | The star rating should be an average score from the customer reviews. | Yes | Available to everyone. |
| Clicking the back button. | Takes you back to the previous page. | Yes |  |
| Clicking the back button after submitting a review or added a wine to the favourites. | User should be taken back to the previous page without affecting the changes made by the user. | Yes |  |
|  | User Profile |  |  |
| Change delivery details field. | The form will not be submitted if not all the fields has been filled out. The form should validate the inputs and give information on what it is that is missing/incorrect. | Yes | Only available for Registered Users |
| Click on "Update Information". | The changes will only be updated if the form and the required fields are valid. | Yes | Only available for Registered Users |
|  | Favourites |  |  |
| Click on "View details" on winebottle | The user should get to the wine details page. | Yes | Only available for Registered Users |
| Click "Remove from Favourites". | The winebottle will be removed from the favourites page. | Yes | Only available for Registered Users |
| Click the back button on wine details page. | User should get taken back to the last page with the changes to the favourites unchanged. | Yes | Only available for Registered Users |

# Django Automated Testing 

### Terminal Command
```
python3 manage.py test app_name.test_filename --settings=silver_sands.test_settings -v3
```

This terminal command was used to run each of the test files within the Silver Sands Estate project individually. The file path to each of the test python files is specified in 'app_name.test_filename'. 
For example to run the automated test_models.py in the products app created to test the products models.py the following was executed in the terminal:
```
python3 manage.py test products.test_models --settings=silver_sands.test_settings -v3
```
All models, forms and views have been tested within each app using automated testing.

### Django unit testing
The Silver Sands project consist of 7 main apps. Within these apps are automated testing files designed to test the models, forms and views within each app. We can run each of these tests seperately. I was aware of the want and need to implement automated testing from the begining of the porject. I chose to first complete the development of all funcitonality first and run the automated testing at the end. The automated tests found a few bugs related to the form handling and submission of invalid form entries making it quick and easy to locate and fix the bugs. On reflecton I found this to be a good method however I would like to have, and will in the future implement and run automated testing along side development in order to increase productivity.

# Django Unit Testing Results 

## Bag App - test_views.py

The `test_views.py` has been created to focus on ensuring the correct behaviour of adding, adjusting, viewing and removing items from the shopping bag. Below are the key tests performed, and they all passed successfully:

- **Successful Addition:** Verified that a product can be added to the bag when there is sufficient stock.

- **Exceeding stock:** Ensured that an error message is displayed when attempting to add a quantity exceeding the available stock of a product.

- **Out of Stock:** Checked that an error is raised when trying to add a product that is currently out of stock.

- **Adjusting Quantity:** Validated the functionality of adjusting the quantity of a product already in the bag.

- **Out of Stock on Adjustment:** Confirmed that attempting to adjust the quantity of a product that is out of stock results in an appropriate error message.

- **Successful Removal:** Tested the removal of an item from the bag to ensure it is correctly deleted.

- **Removing Non-existent items:** Verified the behavior when trying to remove an item not present in the bag, ensuring the application handles this gracefully.

- **Page Rendering:** Confirming that the bag page renders correctly and displays the necessary context for the user.

### Test Results 
All tests were executed successfully, with a total of 8 tests run and no failures reported. This indicates that the bag functionality behaves as expected, ensuring a robust shopping experience for users.

[See the bag view Terminal results Here.](documentation/testing/django_automated_results/bag-test-views.png)


## Checkout App - test_models.py

The `test_models.py` file has been created to ensure the correct behavior of `Order` and `OrderLine Item` functionalities within the application. Below are the key tests performed, and they all passed successfully:

- **Order Total Calculation Below Threshold:** Verified that the update_total method correctly calculates the order total and delivery cost when the total is below the defined free delivery threshold.

- **Line Item Total Calculation:** Ensured that the lineitem_total for an OrderLineItem is calculated correctly based on the price of the wine and the quantity ordered.

- **Updating Order Total on Line Item Addition:** Checked that when a new line item is added to an order, the order's total and delivery cost are updated correctly to reflect the addition.

- **Order Creation Validation:** Tested that an Order is created successfully with the correct initial values, including a generated order number and default values for delivery cost and grand total.

- **Line Item Quantity Adjustment:** Verified that the quantity of an order line item is set correctly and that it interacts properly with the line item total when updated.

### Test Results 

All tests were executed successfully, with a total of 5 tests run and no failures reported. This indicates that the order and order line item functionalities behave as expected, ensuring accurate processing of customer orders.

[See the checkout model Terminal results Here.](documentation/testing/django_automated_results/checkout-test-models.png)


## Checkout App- test_forms.py

The `test_forms.py` file has been created to validate the functionality of the `OrderForm` within the checkout application. Below are the key tests performed, and they all passed successfully:

- **Valid Form Submission:** Verified that a valid order form with all required fields correctly passes validation and is accepted.

- **Invalid Email Handling:** Ensured that an invalid email format is correctly rejected, raising the appropriate validation error.

- **Required Fields Validation:** Checked that the form correctly enforces the presence of required fields (e.g., full name, email, phone number, etc.) and raises validation errors if they are missing.

- **Postcode Format Validation:** Verified that the postcode field only accepts numeric input within the specified length constraints.

- **Country Selection Validation:** Ensured that the country field is validated against a predefined set of choices, confirming that only valid country codes are accepted.

### Test Results

All tests were executed successfully, with a total of 5 tests run and no failures reported. This indicates that the `OrderForm` functionalities behave as expected, ensuring accurate data collection and validation for customer orders. 

More duplicate tests could have been created using the automated Django method to ensure every required field was tested and all format and length validations considered. However I have only run these duplicate validation tests on a maximum of two fields using this method as I have manually tested all all field validations successfully. This includes required field, format and length validations. 

[See the checkout form Terminal results Here.](documentation/testing/django_automated_results/checkout-test-forms.png)


## Home App - test_views.py

The `test_views.py` file has been created to ensure the correct behavior of the views within the home application. Below are the key tests performed, and they all passed successfully:

- **Home View Rendering:** Verified that the home view renders correctly with a status code of 200 and uses the correct template. Ensured that the `show_signup_form` context variable is set to `True`.

- **About Us View Rendering:** Ensured that the about us view renders correctly with a status code of 200 and uses the appropriate template. Confirmed the presence of the `show_signup_form` context variable with a value of `True`.

- **Access Denied View Rendering:** Checked that the access denied view renders correctly, returning a status code of 200 and using the correct template.

- **Visit Us View Rendering:** Verified that the visit us view is rendered properly with a status code of 200 and that it uses the correct template. Ensured that the `show_signup_form` context variable is present and set to `True`.

### Test Results

All tests were executed successfully, with a total of 4 tests run and no failures reported. This indicates that the home app views function as expected, providing the correct responses and context for users.

[See the home app Terminal results Here.](documentation/testing/django_automated_results/home-test-views.png)



## Management Dashboard App - test_forms.py

The `test_forms.py` file has been created to ensure the correct behavior of the forms within the management dashboard application. Below are the key tests performed, and they all passed successfully:

#### ProductForm Tests

- **Valid Product Form Submission:** Verified that a valid `ProductForm` can be submitted successfully, confirming that the form is valid without any errors.
  
- **Invalid Product Form - Empty Name:** Ensured that the form is invalid when the name field is empty. The test confirmed that the form correctly identifies this issue.

- **Invalid Product Form - Name Too Long:** Verified that the form is invalid when the name exceeds the maximum length of 50 characters. The test confirms that validation prevents submission.

- **Invalid Product Form - Non-Alphanumeric Name:** Checked that the form is invalid when the name contains non-alphanumeric characters. The test confirms the presence of an appropriate error.

- **Invalid Product Form - Negative Price:** Ensured that the form is invalid when the price is a negative value. The validation correctly identifies this issue.

- **Invalid Product Form - Stock Exceeds Limit:** Verified that the form is invalid when the stock exceeds the maximum allowed limit of 99,999. The test confirms that validation prevents submission.

#### OrderStatusForm Tests

- **Valid Order Status Form Submission:** Verified that a valid `OrderStatusForm` can be submitted successfully. The test confirmed that the form is valid without any errors.

- **Invalid Order Status Form - Empty Status:** Ensured that the form is invalid when the status field is empty. The test confirmed that this requirement is properly validated.

### Test Results

All tests were executed successfully, with a total of 8 tests run and no failures reported. This indicates that the forms in the management dashboard app function as expected, validating user inputs and ensuring that only correct data can be submitted.

[See the management dashboard app Terminal results Here.](documentation/testing/django_automated_results/management-dashboard-test-forms.png)


## Management Dashboard App - test_views.py

The `test_views.py` file has been created to ensure the correct behavior of the views within the management dashboard application. Below are the key tests performed, and they all passed successfully:

#### User Authentication and Permissions

- **Superuser Authentication:** Verified that a superuser can log in successfully to access the management dashboard views. This ensures that only authorized users can manage orders and products.

#### Product Management Tests

- **Add Product View:** Tested that a new product can be added successfully. The test confirmed that upon submitting a valid product form, a redirect occurs, and the product exists in the database afterward.

- **Edit Product View:** Verified that an existing product can be edited. The test confirmed that after submitting the updated product data, a redirect occurs, and the changes are reflected in the database.

- **Delete Product View:** Ensured that a product can be deleted successfully. The test confirmed that after submitting the deletion request, a redirect occurs, and the product no longer exists in the database.

#### Order Management Tests

- **Manage Orders View:** Verified that the manage orders view renders correctly and contains the expected order information. The test confirmed that the response status is 200 and includes the order number.

- **Order Details View:** Tested the order details view to ensure that the order information is displayed correctly. The test confirmed that the response status is 200 and contains the expected order number.

- **Delete Order View:** Ensured that an order can be deleted successfully when its status is set to 'pending.' The test confirmed that after submitting the deletion request, a redirect occurs, and the order no longer exists in the database.

### Test Results

All tests were executed successfully, with a total of 8 tests run and no failures reported. This indicates that the views in the management dashboard app function as expected, providing the necessary functionality for managing products and orders.

[See the management dashboard app Terminal results Here.](documentation/testing/django_automated_results/management-dashboard-test-views.png)



## Products App - test_models.py

**Category and Wine Model Tests**

The following tests were created to ensure the correct behavior of the `Category` and `Wine` models within the product management application. Below are the key tests performed, and they all passed successfully:

#### CategoryModel Tests

- **Unique Category Name Validation:**  
  Verified that attempting to create a `Category` with a duplicate name raises a `ValidationError`. This ensures the uniqueness constraint on the `name` field is respected, preventing the insertion of categories with identical names.

#### WineModel Tests

- **Slug Generation on Wine Creation:**  
  Tested that the slug is correctly generated based on the wine's name if a slug is not explicitly provided. When a `Wine` instance with the name `New Wine Name` was created, the generated slug was `new-wine-name`, ensuring that slugs follow the expected format.

- **Unique Slug Validation:**  
  Ensured that attempting to create a `Wine` instance with a non-unique slug (a slug already used by another wine) raises a `ValidationError`. This test confirms the uniqueness constraint on the `slug` field, preventing duplicate slugs in the database.

- **Wine Creation with Blank Slug:**  
  Verified that a `Wine` instance can be created without explicitly providing a slug, and that one is automatically generated based on the wine's name. For a wine named `Blank Slug Wine`, the generated slug was `blank-slug-wine`.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that both the `Category` and `Wine` models function as expected, respecting unique constraints and generating correct string representations and slugs.

[See the product management app test results Here.](documentation/testing/django_automated_results/products-test-models.png)


## Products App - test_views.py

The following tests were created to ensure the correct behavior of the views within the products application. Below are the key tests performed, and they all passed successfully:

#### Product List View Tests

- **Basic Product Listing:** Tested that the product listing page loads successfully and displays all the wines. It confirms that wines like `Test Wine 1` and `Test Wine 2` are visible.

- **Category Filter:** Tested filtering by category. The test confirmed that wines from the category "Test Category" are correctly displayed.

- **Sorting by Price:** Tested the sorting functionality by price in ascending order. The wines are correctly sorted with the cheapest wine displayed first, ensuring that the sorting logic works as expected.

#### Product Details View Tests

- **Basic Product Details Display:** Tested that the product details page for `Test Wine 1` loads successfully and displays the correct wine details, such as name, description, and vintage.

- **Review Submission:** Tested that authenticated users can successfully submit a review for a product. After posting a review, the page redirects correctly, and the new review appears on the product's details page.

- **Average Rating Calculation:** Verified that the average rating is correctly calculated and displayed on the product details page.

#### Review Management Tests

- **Review Deletion (Owner Only):** Tested that users who own a review can delete it. After deletion, the review is removed from the database, and the user is redirected back to the product details page.

- **Review Deletion Not Authorized:** Tested that users who are not the owner of a review cannot delete it. This test confirmed that a `403 Forbidden` error is returned for unauthorized delete attempts.

- **Review Editing:** Verified that review owners can edit their reviews and that edited reviews are marked as unapproved. This ensures that reviews must be reapproved after editing.

#### Product Search Tests

- **Basic Search Functionality:** Tested the search functionality to ensure it returns the correct products based on a search query (e.g., `Test Wine`). Both wines containing the search term were returned in the results.

- **Price Filtering:** Tested the price filtering feature. The test confirmed that filtering by a minimum price of `15` correctly returns `Test Wine 2` and excludes `Test Wine 1`.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the views for product listing, product details, and review management work as expected, handling sorting, filtering, and review operations appropriately.

[See the product management app test results Here.](documentation/testing/django_automated_results/products-test-views.png)


## Reviews App - test_models.py

The following tests were created to ensure the correct behavior of the `Review` model within the reviews application. Below are the key tests performed, and they all passed successfully:

### Review Model Tests

- **Creating Valid Review:** Tested the creation of a valid review to ensure that the model correctly associates reviews with their respective wines and users. Confirmed that all attributes are set as expected.

- **Rating Out of Range Validation:** Ensured that a `ValidationError` is raised when an invalid rating (less than 1 or greater than 5) is submitted. This confirms that the rating field enforces the specified range.

- **Comment Maximum Length Validation:** Tested that the `comment` field respects the maximum length constraint of 150 characters. The test successfully raised a `ValidationError` for comments exceeding this length.

- **Approved Default Value:** Verified that the `approved` field defaults to `False` when a review is created. This ensures that newly created reviews are not approved until explicitly set.

- **Timestamps Validation:** Confirmed that the `created_at` and `updated_at` fields are populated correctly upon review creation and are updated properly when the review is modified. A deliberate sleep delay was implemented to ensure that timestamps differ after an update.

- **String Representation:** Tested the `__str__` method of the `Review` model to ensure it returns the expected string format, indicating the wine name and user.

- **Review Ordering:** Verified that reviews are ordered by their creation date in descending order. This confirms that the most recent reviews appear first when fetched.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the `Review` model functions as expected, enforcing constraints and maintaining data integrity for user reviews of wines.

[See the review model test results here.](documentation/testing/django_automated_results/reviews-test-models.png)


## Reviews App - test_forms.py

The following tests were created to ensure the correct behavior of the `ReviewForm` within the reviews application. Below are the key tests performed, and they all passed successfully:

### Review Form Tests

- **Valid Review Submission:** Tested that the `ReviewForm` accepts valid input data, confirming that a rating of 5 and a descriptive comment successfully validate and produce expected cleaned data.

- **Invalid Rating Submission:** Verified that the form raises a validation error when an invalid rating (greater than 5) is submitted. This ensures that the rating field enforces the specified range and prevents incorrect data entry.

- **Boundary Rating Testing:** Ensured that the form correctly handles boundary conditions for ratings. Tests confirmed that ratings below 1 and above 5 are marked as invalid, while ratings of exactly 1 and 5 are accepted as valid inputs.

- **Comment Length Validation:** Tested that the `comment` field respects the maximum length constraint of 150 characters. The test successfully raised a `ValidationError` for comments that exceeded this length, enforcing the integrity of user input.

- **Clean Rating Method Functionality:** Verified that the `clean_rating` method correctly processes and returns valid ratings. This included ensuring that the method appropriately flags invalid ratings and confirms the correct ratings are stored in cleaned data.

- **Edge Case Handling:** Tested edge cases for the rating submission, ensuring that boundary conditions are properly validated, and confirming that appropriate errors are raised for invalid inputs.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the `ReviewForm` functions as expected, ensuring data validation, integrity, and user feedback for the review submission process.

[See the review form test results here.](documentation/testing/django_automated_results/reviews-test-forms.png)


## Profiles App - test_models.py

The following tests were created to ensure the correct behavior of the `UserProfile` and `Favourite` models within the profiles application. Below are the key tests performed, and they all passed successfully:

### UserProfile Model Tests

- **User Profile Creation:** Tested that a `UserProfile` is created automatically when a `User` is created. This ensures that every user has an associated profile for storing default delivery information.

- **String Representation:** Verified that the string representation of the `UserProfile` returns the correct username. This is important for readability and debugging purposes.

- **Default Full Name:** Checked that the `default_full_name` field can be set and retrieved correctly. This allows users to store their full name in their profile.

### Favourite Model Tests

- **Favourite Creation:** Tested that a `Favourite` is created correctly when a user favourites a wine. This ensures proper association between users and their favourite wines.

- **String Representation:** Verified that the string representation of the `Favourite` returns the expected format, indicating which user favourited which wine.

- **Unique Favourite Constraint:** Ensured that a user cannot favourite the same wine more than once, enforcing uniqueness constraints for the `Favourite` model.

- **Added On Field:** Confirmed that the `added_on` field is populated with the current date and time when a `Favourite` is created. This helps track when a wine was added to the user's favourites.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the `UserProfile` and `Favourite` models function as expected, maintaining data integrity and enforcing relationships between users and wines.

[See the profiles model test results here.](documentation/testing/django_automated_results/profiles-test-models.png)

## Profiles App - test_forms.py

The following tests were created to ensure the correct behavior of the `UserProfileForm` within the profiles application. Below are the key tests performed, and they all passed successfully:

### UserProfileForm Tests

- **Valid User Profile Form Submission:** Verified that the form is valid when provided with correct data, ensuring that user profile details can be saved successfully.

- **Empty Full Name Validation:** Ensured that a `ValidationError` is raised when the full name field is left empty. This confirms that the full name is a required field.

- **Full Name Length Validation:** Confirmed that a `ValidationError` is raised when the full name exceeds 40 characters, enforcing the specified length constraint.

- **Empty Phone Number Validation:** Tested that the form raises a `ValidationError` if the phone number field is left empty, indicating that a phone number is mandatory.

- **Non-Numeric Phone Number Validation:** Ensured that the form raises a `ValidationError` when the phone number is non-numeric, confirming that only valid numeric input is allowed.

- **Phone Number Length Validation:** Verified that a `ValidationError` is raised if the phone number exceeds 15 digits, ensuring that the length constraint is enforced.

- **Non-Numeric Postal Code Validation:** Tested that the form raises a `ValidationError` if the postal code is non-numeric, ensuring only valid input is accepted.

- **Postal Code Length Validation:** Confirmed that a `ValidationError` is raised if the postal code exceeds 10 digits, reinforcing the length constraint.

- **Empty Street Address 1 Validation:** Verified that the form raises a `ValidationError` when the first street address is left empty, ensuring that it is a required field.

- **Street Address 1 Length Validation:** Ensured that a `ValidationError` is raised if the first street address exceeds 50 characters, enforcing the specified length limit.

- **Empty County Validation:** Tested that the form raises a `ValidationError` if the county field is left empty, indicating that it is required.

- **County Length Validation:** Verified that a `ValidationError` is raised if the county exceeds 40 characters, ensuring compliance with the length requirement.

- **Empty Town or City Validation:** Ensured that the form raises a `ValidationError` when the town or city field is left empty, confirming that it is a mandatory field.

- **Town or City Length Validation:** Confirmed that a `ValidationError` is raised if the town or city exceeds 40 characters, enforcing the length constraint.

- **Street Address 2 Length Validation:** Verified that the form raises a `ValidationError` if the second street address exceeds 50 characters, ensuring the length limit is respected.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the `UserProfileForm` functions as expected, enforcing validation rules and maintaining data integrity for user profiles.

[See the user profile form test results here.](documentation/testing/django_automated_results/profiles-test-forms.png)

## Profiles App - test_views.py

The following tests were created to ensure the correct behavior of the views within the profiles application. Below are the key tests performed, and they all passed successfully:

### Profile View Tests

- **Profile View Access:** Tested that logged-in users can access the profile view. This ensures that the correct template (`profiles/profile.html`) is rendered and a status code of 200 is returned.

- **Order History View Access:** Verified that users can view their order history. The test checks that the order history page is displayed correctly using the template (`checkout/checkout_success.html`) and returns a status code of 200.

### Favourite Functionality Tests

- **Add to Favourites:** Tested the functionality of adding a wine to the user's favourites. This ensures that the wine is successfully added, returns a status code of 200, and contains a success message confirming the addition.

- **Favourites View Display:** Checked that the favourites view displays the wines the user has favourited. The test verifies that the correct template (`profiles/favourites.html`) is used and that the favourited wine appears on the page.

### Test Results

All tests were executed successfully, with no failures. These tests confirm that the views within the profiles application function as expected, ensuring proper user interaction and data retrieval.

[See the profiles view test results here.](documentation/testing/django_automated_results/profiles-test-views.png)



## Validation
### HTML Validation

The project HTML templates have been thoroughly checked by validating each deployed page using the [W3C Validator](https://validator.w3.org/nu/). To do this, I copied the deployed URL of each page directly from the browser's address bar. After obtaining the URL, I navigated to the W3C Validator, where I pasted the copied URL into the designated input field for validation. Once submitted, the validator checked the HTML structure of each page, ensuring compliance with web standards. This process confirmed that no warnings or errors were present in any of the HTML templates as shown in the reports below.

Although there were no error or warning messages displayed when after validating the html templates there was the occasional 'Info' tag that indicted the same 'trailing slash on void elements has no effect'. This comes from the Allauth templates and as a result of its passive nature has not been changed in the multiple templates it occurs in. See the 'Edit Product' report in the list below for reference.

### Complete HTML Validation Reports

#### Bag App - Reports

- [Bag - "/bag/"](documentation/testing/html_checks/html-checks-bag.png)

#### Checkout App - Reports

- [Check Out - "/checkout/"](documentation/testing/html_checks/html-checks-checkout.png)

- [Checkout Success - "/checkout/checkout_success/order_number"](documentation/testing/html_checks/html-checks-checkout-success.png)

#### Home App - Reports

- [Homepage - "/"](documentation/testing/html_checks/html-checks-homepage.png)

- [Our Story - "/our_story/"](documentation/testing/html_checks/html-checks-our-story.png)

- [Visit Us - "/visit_us/"](documentation/testing/html_checks/html-checks-visit-us.png)

- [Access Denied - "/access-denied/"]

#### Management Dashboard App - Reports

- [Add Product - "/management_dashboard/add/"](documentation/testing/html_checks/html-checks-add-product.png)

- [Edit Product - "/management_dashboard/edit/wine_id"](documentation/testing/html_checks/html-checks-edit-product.png)

- [Manage Orders - "/management_dashboard/manage_orders/"](documentation/testing/html_checks/html-checks-manage-orders.png)

#### Products App - Reports

- [All Wines - "/products/"](documentation/testing/html_checks/html-checks-product-list.png)

- [Product Details - "/products/wine_id/"](documentation/testing/html_checks/html-checks-product-details.png) 

- [Search - "/products/search/"](documentation/testing/html_checks/html-checks-search.png)

#### Profiles App - Reports

- [Profile - "/profile/"](documentation/testing/html_checks/html-checks-profile.png) 

- [Favourites - "profile/favourites/"](documentation/testing/html_checks/html-checks-favourite.png)

- [Order History - "/profile/order_history/"](documentation/testing/html_checks/html-checks-order-history.png)


### CSS Validation

No warnings or errors were found when passing the css through the [W3C (Jigsaw)](https://jigsaw.w3.org/css-validator/#validate_by_uri). I have manually run these checks by copying each of the deployed page URLs and pasting them into the validator.

#### Complete CSS Validation Reports

- [Homepage - Report](documentation/testing/css_checks/css-check-home.png)

- [Our Story - Report](documentation/testing/css_checks/css-check-about.png)

- [Visit Us - Report](documentation/testing/css_checks/css-check-visit.png)

- [All Wines - Report](documentation/testing/css_checks/css-check-productlist.png)

- [Wines Detail - Report](documentation/testing/css_checks/css-check-details.png)

- [Profile - Report](documentation/testing/css_checks/css-check-profiles.png)

- [Checkout - Report](documentation/testing/css_checks/css-check-checkout.png)

- [Bag - Report](documentation/testing/css_checks/css-check-bag.png)

- [Favourites - Report](documentation/testing/css_checks/css-check-favourites.png)

- [Add Prodcut - Report](documentation/testing/css_checks/css-check-add-product.png)

- [Edit Product - Report](documentation/testing/css_checks/css-check-edit-product.png)

- [Manage Orders - Report](documentation/testing/css_checks/css-check-manage-orders.png)


### JS Validation

All javascript files were validated and no warning or error messages were found when passing the java script files through the [JSHint](https://www.jshint.com/) validator. However there were informational messages/notices indicating  useful insights into code that does not necesarily affect its functionality.

During the validation of JavaScript code using JSHint, a handfull of 'unused variable' messages were found. It is important to note that these variables correspond to functions invoked within the HTML templates, which were not included in the JSHint validation context. Consequently, JSHint is unable to recognize that these functions are actively utilized in the application's user interface. To confirm the use of these functions the corresponding html templates have been manually checked for the function invoking. 

To ensure JSHint correctly validated jQuery \$ functions within some of the javascript files, JSHint has been configured to recognise \$ as a global variable by adding,
```
/* jshint jquery: true */
/* global $ */
```
to the top of the javascript file being validated.

To ensure JSHint recognises the bootstrap variable (from the bootstrap library/framework) refered to in the manage_orders.js file a similar approach has been taken to configure JSHint it recognise bootstrap as a global variable by adding,
```
/* global bootstrap */
```
to the top of the javascript file being validated.


#### Complete Java Script Validation Reports

- [Age Verification JS - Report](documentation/testing/js_checks/js-checks-age-verification.png)

- [Back Button JS - Report](documentation/testing/js_checks/js-checks-back-button.png)

- [Bag Quantity Update JS - Report](documentation/testing/js_checks/js-checks-bag-quantity-update.png)

- [Base JS - Report](documentation/testing/js_checks/js-checks-base.png)

- [Country Field JS - Report](documentation/testing/js_checks/js-checks-countryfield.png)

- [Manage Orders JS - Report](documentation/testing/js_checks/js-checks-manage-orders.png)

- [Product Details JS - Report](documentation/testing/js_checks/js-checks-product-details.png)

- [Product List JS - Report](documentation/testing/js_checks/js-checks-product-list.png)

- [Quantity Input JS- Report](documentation/testing/js_checks/js-checks-quantity-input.png)

- [Ratings JS - Report](documentation/testing/js_checks/js-checks-ratings.png)

- [Stripe Elements JS - Report](documentation/testing/js_checks/js-checks-stripe-elements.png)


### Python Validation

No warnings or errors were found when the python code was passed through [Code institutes Python Linter validation tool](https://pep8ci.herokuapp.com/). According to the reports, the code is [Pep 8-compliant](https://legacy.python.org/dev/peps/pep-0008/). This checking was done manually by copying python code and pasting it into the validator. 

Pasting in each of the python files within the project ultimately rendered the same results/report. [Click here](documentation/testing/py_checks/py-checks-checkout-views.png) to see the results from pasting in the checkout apps views.py file, returning a result of 'All clear, no errors found'. As mentioned this same method and results were followed for all python files within the project including all views, forms and models.


### Lighthouse validation
