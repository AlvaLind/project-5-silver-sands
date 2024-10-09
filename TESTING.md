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

## Automated Testing 

### Terminal Command
```
python3 manage.py test app_name.test_filename --verbosity=3 --settings=products.test_settings
```

This terminal command was used to run each of the test files within the Silver Sands Estate project individually. The file path to each of the test python files is specified in 'app_name.test_filename'. 
For example to run the automated test_models.py in the products app created to test the products models.py the following was executed in the terminal:
```
python3 manage.py test products.test_models --verbosity=3 --settings=products.test_settings
```
All models, forms and views have been tested within each app using automated testing.

## Automated Testing
### Django unit testing

add text here

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
