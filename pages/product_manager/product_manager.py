from flask import Blueprint, render_template, redirect, url_for, request, flash
from entities import Product

# Products Blueprint Definition
product_manager = Blueprint('product_manager', __name__, static_folder='static', static_url_path='/product_manager',
                     template_folder='templates')


#  Routes
@product_manager.route('/product_manager')
def index():
    products_data = Product().get_all()  # The products that will appear in the carousel
    return render_template('product_manager.html', products=products_data)


@product_manager.route('/add_product', methods=["POST"])
def add_product():
    product = Product()
    product.id = request.form['id']
    product.name = request.form['name']
    product.price = request.form['price']
    product.description = request.form['description']
    product.img = request.form['img']
    product.category_code = request.form['category-code']
    product.add_product()
    flash('Added Successfully!')
    return redirect(url_for('product_manager.index'))


@product_manager.route('/update', methods=["POST"])
def update():
    print(request.form['given-id'])
    print(request.form['id'])
    Product().update_product(request.form['id'], request.form['name'], request.form['price'],
                             request.form['prev-price'], request.form['description'], request.form['img'],
                             request.form['category-code'], request.form['given-id'])
    flash('Updated Successfully!')
    return redirect(url_for('product_manager.index'))


@product_manager.route('/delete/<string:id>', methods=["GET"])
def delete(id):
    Product().delete_product(id)
    flash('Deleted Successfully!')
    return redirect(url_for('product_manager.index'))

