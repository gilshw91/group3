from flask import Flask, session, redirect, url_for, render_template
from utilities.db.db_manager import dbManager


###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
## Homepage
#TODO: we need to change homepage to homepage page
from pages.homepage.homepage import homepage
app.register_blueprint(homepage)

## About
from pages.about.about import about
app.register_blueprint(about)

## Catalog
from pages.catalog.catalog import catalog
app.register_blueprint(catalog)

## Page error handlers
from pages.page_error_handlers.page_error_handlers import page_error_handlers
app.register_blueprint(page_error_handlers)

## Categories
from pages.categories.categories import categories
app.register_blueprint(categories)

## sign_in_registration
from pages.sign_in_registration.sign_in_registration import sign_in_registration
app.register_blueprint(sign_in_registration)

## sign_up
from pages.sign_up.sign_up import sign_up
app.register_blueprint(sign_up)

## sign_out
from pages.sign_out.sign_out import sign_out
app.register_blueprint(sign_out)

# Product check
from pages.product.product import product
app.register_blueprint(product)

## catalog
from pages.catalog.catalog import catalog
app.register_blueprint(catalog)

## customer_feedback
from pages.customer_feedback.customer_feedback import customer_feedback
app.register_blueprint(customer_feedback)

##customer_page
from pages.customer_page.customer_page import customer_page
app.register_blueprint(customer_page)
###### Components
## Main menu
from components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)


@app.route("/cart")
def cart():
    if not session.get('email'):
        return redirect(url_for('sign_in_registration.index'))
    user_mail = session['email']
    user_items = dbManager.fetch('''
        SELECT product.id, product.name, product.price, product.img 
        FROM product 
        JOIN kart
        WHERE product.id = kart.product_id 
        AND kart.email_address = user_mail
        ''')
    number_of_items = dbManager.fetch("SELECT count(product_id) FROM kart WHERE email_address = %s", (user_mail,))
    total_price = 0
    for row in user_items:
        total_price += row[2]
    return render_template("cart.html", products=user_items, totalPrice=total_price, loggedIn=session['logged-in'],
                           firstName=session['name'], noOfItems=number_of_items)
