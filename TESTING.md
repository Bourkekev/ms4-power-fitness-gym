# Testing

## Validation

### HTML

### CSS
I used the [Autoprefixer Tool](https://autoprefixer.github.io/) to apply browser prefixes.
I validated the CSS with the [W3 CSS Validation Service](https://jigsaw.w3.org/css-validator/) for CSS Level 3 and no errors were found, though it warned me about the vendor prefixes that the Autoprefixer had added.

### Javascript

I ran my javascript files through [JSHint](jshint.com)

## Colour Constrast Checking
I used [WebAIM's](https://webaim.org/resources/contrastchecker/) contrast checker to ensure that text on coloured backgrounds is readable and to WCAG AA Standard, especially white text on coloured backgrounds.

## Issues I had to overcome

### Allowing admin to set sizes
I wanted the admin to be able to set different sizes on clothing and shoes, and the shoe sizes would be different from the clothing sizes. I tried using django's built in CharField choices, but this only allowed you select 1 from a dropdown list, where I needed to be able to set multiple sizes for a product. So I used the Django [MultiSelectField package](https://pypi.org/project/django-multiselectfield/). This allows the admin to select multiple options (set in the product model) in the form of checkboxes.

### Getting multiple sizes to work in the bag app
I was able to get a single size attribute (e.g. shoe size) to be stored in the shopping bag session and listed in the bag page. But it proved more difficult to also get the clothing sizes to be stored. At first I tried just duplicating what I had done for the shoe sizes and checking for the clothing size. I had it that the bag app was assuming that if the item's dictionary value was not an integer, then look for the value of the shoe sizes or clothing size. But I was getting a KeyError for the clothing key. Finally I realised that the program was trying to get the shoe size and clothing size for all items, which of course is not possible. I needed to check which it was.

So in the view, I had to check did shoe or clothing size exist in the POST object, check which one it was and then add (or increment) the item to the bag session. In the bag context file, I commented out the erroring code and worked out some simple if statements, so if the specific size key is in the bag item, print out what size is present and the value. I could see the dictionary that was being printed out and used [JSON Formatter](https://jsonformatter.org/) to view the structure clearer. This helped me determine how to access the correct key, value pairs. Once that was working I could place the code for adding the items to the bag within the 'if key' structure.

## Testing

### Testing Save info in webhook handler
I commented out the form.submit() action in the stripe_elements javascript file and placed an order with the save info box checked, while changing some profile information. This breaks the normal payment process (as the form is not submitted) and the fallback relies on the webhook handler to save the information. Checking the payments in Stripe dashboard shows the payment still succeeded. Then checking the orders in the site admin shows that the order was created and the profile details updated. Also, by checking the site front-end user profile, it shows that the order succeeded and the details were updated. Finally, going to the checkout page again with the same user shows their pre-filled details has been updated too.