# Testing

## Validation

### HTML

### CSS
I used the [Autoprefixer Tool](https://autoprefixer.github.io/) to apply browser prefixes.
I validated all the CSS files with the [W3 CSS Validation Service](https://jigsaw.w3.org/css-validator/) for CSS Level 3 + SVG and no errors were found, though it warned me about the vendor prefixes that the Autoprefixer had added.

### Javascript

I ran my javascript files through [JSHint](jshint.com)

## Colour Constrast Checking
I used [WebAIM's](https://webaim.org/resources/contrastchecker/) contrast checker to ensure that text on coloured backgrounds is readable and to WCAG AA Standard, especially white text on coloured backgrounds.

## Automatic Testing

I have written a number of tests to test the key functionality of each app. These can be run with the command:

`python manage.py test`

Or to test an individual app:

`python manage.py test <appname>`

e.g. `python manage.py test pages`

I have detailed some of the automatic tests that are run on each app below.

### Pages App

As most of these pages are just displaying content from a template, most tests are just to test that the pages load ok, or return a status code of 200.

There is a test for the homepage to test that the homepage uses the class HomePageView view.

The contact page has additional tests to test the form. There is a test to check that the contact page is using the ContactUsForm, and then 2 tests which test the form validation for blank fields, and submitting the form when required fields are filled in.

### News App

The tests for the news app test creating a new news post. There is some set up for the tests, a test user and a test post are created, and the tests check for the new post content, status code 200 and correct template for the news listings and news post detail page. There is a test for a 404 response from a non-existing news post.

## Manual Testing

### Testing Save info in webhook handler
I commented out the form.submit() action in the stripe_elements javascript file and placed an order with the save info box checked, while changing some profile information. This breaks the normal payment process (as the form is not submitted) and the fallback relies on the webhook handler to save the information. Checking the payments in Stripe dashboard shows the payment still succeeded. Then checking the orders in the site admin shows that the order was created and the profile details updated. Also, by checking the site front-end user profile, it shows that the order succeeded and the details were updated. Finally, going to the checkout page again with the same user shows their pre-filled details has been updated too.

## Issues I had to overcome

### Allowing admin to set sizes
I wanted the admin to be able to set different sizes on clothing and shoes, and the shoe sizes would be different from the clothing sizes. I tried using django's built in CharField choices, but this only allowed you select 1 from a dropdown list, where I needed to be able to set multiple sizes for a product. So I used the Django [MultiSelectField package](https://pypi.org/project/django-multiselectfield/). This allows the admin to select multiple options (set in the product model) in the form of checkboxes.

### Getting multiple sizes to work in the bag app
I was able to get a single size attribute (e.g. shoe size) to be stored in the shopping bag session and listed in the bag page. But it proved more difficult to also get the clothing sizes to be stored. At first I tried just duplicating what I had done for the shoe sizes and checking for the clothing size. I had it that the bag app was assuming that if the item's dictionary value was not an integer, then look for the value of the shoe sizes or clothing size. But I was getting a KeyError for the clothing key. Finally I realised that the program was trying to get the shoe size and clothing size for all items, which of course is not possible. I needed to check which it was.

So in the view, I had to check did shoe or clothing size exist in the POST object, check which one it was and then add (or increment) the item to the bag session. In the bag context file, I commented out the erroring code and worked out some simple if statements, so if the specific size key is in the bag item, print out what size is present and the value. I could see the dictionary that was being printed out and used [JSON Formatter](https://jsonformatter.org/) to view the structure clearer. This helped me determine how to access the correct key, value pairs. Once that was working I could place the code for adding the items to the bag within the 'if key' structure.

### Unable to get Stripe CLI to run
For testing locally, Stripe recommends using Stripe CLI for testing webhook responses. But following installation instructions for Windows the program would just not run on my computer. If I tried running the .exe file it would open and then just close immediately (both 32 bit and 64 bit). I tried running it from the terminal, command line, moving the .exe file in to my project folder, my virtual environment, but nothing worked and I was unable to use the 'stripe login' command. Luckily the Ngrok program did work for me and allowed me to test webhooks in local development, but I had to manually create webhooks in the Stripe dashboard for the url that ngrok provided for me.

### Get return domain url for Stripe Subscriptions Checkout
I tried to get the return domain_url from the create_checkout_session view using the build_absolute_uri method and splitting it, in order to not have to set the variable DOMAIN_URL in settings. This worked locally, but testing in the likes of Gitpod only returned http://locahost:8000/ probably because of a proxy server, so this is not likely to work in all situations. I decided to leave the DOMAIN_URL as a setting to be changed upon deployment and made a note about it under the deployment section in the readme file.

### Sending different Subscription Plan Prices
When I got one Subscription Plan set up and working, I wanted to add another plan as an option for customers to sign up to. I obviously wanted to not have to repeat the code in the create_checkout_session view, which at that point was getting the Stripe Price Id from the settings. I wanted it to work so that the button clicked (on memberships page) would send the price to the view. 

I tried using JavaScript's Fetch api and sending the price_id, gotten from button's data attribute, via Fetch's POST method to the view but this required a POST method in the create_checkout_session view. I set up an `if request.method == 'POST'` and was able to get the price_id sent from the button by JavaScript. But I then realised I could not get the data/variable from the POST request to the GET request. It would also have caused a problem with the @csrf_excempt decorator on the view, as it would now require a csrf token. 

So I had to think then if I cannot do it server side, then maybe Javascript can work out the correct price_id before it is retrieved by the create_checkout_session. At first I was thinking I could put it in the url as a parameter and get it from the view. But then I was thinking about how views pass data to each other and could I pass the variable through the fetch url. After some research this [question on stack overflow](https://stackoverflow.com/questions/50983150/how-to-pass-a-variable-with-url-on-javascript-fetch-method) suggested that a variable can be passed with Fetch by using template literals (or back-ticks). So I just needed to adjust my create_checkout_session view and url to look for a price_id and use that as my stripe price_id. Once I had a different event listener for each button, this worked so depending on which button was clicked, the subscription price would be different.

### The community message board Edit Post urls
When viewing a topic I have the url as something like `/community/topic/1/`. THe number is the topic id. But to allow the user to edit a message they have already posted, I first tried with just the url as `edit_post/1/`. This allowed me to edit the message but then I could not return the user to that topic because the view_topic view required a topic id. Also the url was not consistent, as it did not have `community/topic/` in it. I did not know if I could even pass the topic id as well as the message id through the template tag.
But through trial an error I figured out how to do that and was able to get my edit message url to look like `community/topic/1/edit_post/6/` and return the user to the topic page.

### Delete News Post without needing the confirmation template
When using class based views for the news section I wanted to delete a post without needing the default _confirm_delete template, so it would match with how other items on the site are deleted, with a pop-up warning. - This post on [stackoverflow](https://stackoverflow.com/questions/17475324/django-deleteview-without-confirmation-template) helped me understand how to skip the _confirm_delete template when using DeleteView in a class based view.

### Using slugs instead of ids in news posts urls
I have news posts in my project, and I had it all working (CRUD), but I wanted to change the url to use a slug based on the page title instead of just an id like /news/1/, as having numbers in a url is very dated. I had auto generation of the slug from the title working and could view the news post using the slug, but for some reason when I went to create a new post (front-end) I got a 404 page not found error, even though the slug url was only used when viewing the post detail. The id or slug is not passed to the NewsPostCreateView so I don't know why that happens. If I change the url for the NewsPostDetailView view to use <int:pk> instead of <slug:slug>, everything works fine. But for some reason the slug affects the NewsPostCreateView. There were no other errors in the terminal and I was unable to find an answer for this in a reasonable time, so due to time constraints had to move on so have just reverted to use the <int:pk>. I have left the slug field in the model in case I have time to revisit this again later.

### Getting jQuery to work in the Django Admin
I wanted to add JavaScript to the Django admin so I could hide the shoe or clothing sizes options depending on the category selected in the add product page. Following 1 article [here](https://stackoverflow.com/questions/15978719/django-admin-show-field-only-if-checkbox-is-false) and the [django docs](https://docs.djangoproject.com/en/3.1/topics/forms/media/#media-objects), showed how to load the JavaScript file, and it was loading because I could get a console.log to show on the page. But it would not select the element and instead was showing an `Uncaught TypeError: $ is not a function`. It seemed that jQuery was not loaded before my script file. I wanted to use jQuery because I had used it quite simply on the front-end Add Product page, and did not want to have to re-write the same in native JavaScript. So I finally found something that worked, this [Stack Overflow question](https://stackoverflow.com/questions/58087470/django-jquery-is-not-a-function-message) showed how to not fire your JavaScript until Django's jQuery was defined.
