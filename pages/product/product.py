from flask import Blueprint, render_template, request, session, url_for, redirect, flash
from entities import Product, Review, Order
from datetime import datetime

product = Blueprint('product', __name__, static_folder='static', static_url_path='/product', template_folder='templates')

# Routes
@product.route('/product', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':  # Regular version
        product_data = Product().get_product(request.args['id'])
        review_data = Review().get_review(request.args['id'])
        session['pid'] = request.args['id']
        if len(review_data):
            return render_template('product.html', product=product_data[0], review=review_data[0])
        else:
            return render_template('product.html', product=product_data[0])
    else:  # After review was given
        if not session.get('logged-in'):
            flash("Please sign-in to post a review")
            return redirect(url_for('sign_in_registration.index'))
        else:
            email = session['email']
            pid = session['pid']
            has_bought = Order().get_product_order(email, pid)
            if len(has_bought) == 0:
                flash("Only customers who bought this item may review it")
                return redirect(url_for('homepage.index'))
            else:
                review = request.form.get('review')
                rank = request.form.get('star')
                dt_string = datetime.now()  # dd-mm-YY H:M:S
                new_review = Review()
                new_review.date = dt_string
                new_review.rank = rank
                new_review.content = review
                new_review.email_address = email
                new_review.id = pid
                new_review.add_review()
                flash("Thank you for your review")
                return redirect(url_for('homepage.index'))


@product.route('/content_manager')
def content_manager():
    return render_template('content_manager.html')
