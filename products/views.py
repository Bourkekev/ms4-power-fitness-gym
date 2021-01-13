from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """
    * Creates the products listing page, sorting and search queries

    \n Arguments:
    1. request

    \n Returns:
    * request, 'products/products.html', context
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    best_sellers = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            # allow case insensitive sorting
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            # exclude products with no sale price
            if sortkey == 'sale_price':
                products = products.exclude(sale_price__isnull=True)

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'best_sellers' in request.GET:
            products = products.filter(is_best_seller='True')
            best_sellers = True

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You did not enter any search terms!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # create string to sort by
    requested_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'requested_categories': categories,
        'requested_sorting': requested_sorting,
        'best_sellers': best_sellers,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    * Creates a page to show individual product detail

    \n Arguments:
    1. request
    2. product_id

    \n Returns:
    * request, 'products/product_detail.html', context

    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)

    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)


@staff_member_required
def add_product(request):
    """
    * Creates an Add product page and handles \
        new product form submission.  Should require user to be staff_member.

    \n Arguments:
    1. request

    \n Returns:
    * If GET: request, template, form in context
    * If POST: product.id to product_detail view
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product successfully added')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product. \
                            Please ensure the form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@staff_member_required
def edit_product(request, product_id):
    """ edit_product:

    * Edits an existing product. Should require user to be staff_member.

    \n Args:
    1. request
    2. product_id: the ID of the product to be edited

    \n Returns:
    * If GET: request, template, context
    * If POST: product.id to product_detail view

    \n Redirects
    * User back to product page
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(
            request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Updated product successfully.')
            return redirect(reverse('product_detail',
                                    args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                Please ensure the form is valid.')

    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are now editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@staff_member_required
def delete_product(request, product_id):
    """ delete_product:

    * Deletes an existing product. Should require login.

    \n Args:
    1. request
    2. product_id: the ID of the product to be deleted

    \n Returns:
    * redirect to products view

    \n Redirects
    * User back to products page
    """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def review_product(request, product_id):
    """ review_product:

    * Reviews an existing product. Should require login.

    \n Args:
    1. request
    2. product_id: the ID of the product to be reviewed

    \n Returns:
    * If GET: request, template, context
    * If POST: product.id to product_detail view

    \n Redirects
    * User back to product page
    """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.product = product
            review.save()
            messages.success(request, 'Product review successfully submitted')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product review. \
                            Please ensure the form is valid.')
    else:
        form = ReviewForm(instance=product)
    template = 'products/add_review.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    """ edit_review:

    * Edit an existing Review. Should require login.

    \n Args:
    1. request
    2. review_id: the ID of the review to be edited

    \n Returns:
    * If GET: request, template, context
    * If POST: redirect to profile view

    \n Redirects
    * User back to profile page
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.reviewer:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product review successfully edited')
                return redirect(reverse('profile'))
            else:
                messages.error(request,
                               'Failed to edit product review. \
                                Please ensure the form is valid.')
        else:
            form = ReviewForm(instance=review)
        template = 'products/edit_review.html'
        context = {
            'form': form,
            'review': review,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'You cannot edit other people\'s reviews!')
        return redirect(reverse('profile'))


@login_required
def delete_review(request, review_id):
    """ delete_review:

    * Delete an existing Review. Should require login.

    \n Args:
    1. request
    2. review_id: the ID of the review to be deleted

    \n Returns:
    * redirect to profile view

    \n Redirects:
    * User back to profile page
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.reviewer:
        review.delete()
        messages.success(request, 'Review deleted!')
        return redirect(reverse('profile'))
    else:
        messages.error(request, 'You cannot delete other people\'s reviews!')
        return redirect(reverse('profile'))
