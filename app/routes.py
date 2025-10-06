from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Product, Location, ProductMovement
from app.forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import text

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@bp.route('/products/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', form=form, title='New Product')

@bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', form=form, title='Edit Product')

@bp.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'warning')
    return redirect(url_for('main.products'))

@bp.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@bp.route('/locations/new', methods=['GET', 'POST'])
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data)
        db.session.add(location)
        db.session.commit()
        flash('Location created successfully!', 'success')
        return redirect(url_for('main.locations'))
    return render_template('location_form.html', form=form, title='New Location')

@bp.route('/locations/<int:location_id>/edit', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.name = form.name.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('main.locations'))
    return render_template('location_form.html', form=form, title='Edit Location')

@bp.route('/locations/<int:location_id>/delete', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'warning')
    return redirect(url_for('main.locations'))

@bp.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@bp.route('/movements/new', methods=['GET', 'POST'])
def new_movement():
    form = ProductMovementForm()
    form.product_id.choices = [(0, '-- Select Product --')] + [(p.product_id, p.name) for p in Product.query.all()]
    form.from_location.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    form.to_location.choices = [(0, '-- None --')] + [(l.location_id, l.name) for l in Location.query.all()]
    
    if form.validate_on_submit():
        from_loc = form.from_location.data if form.from_location.data != 0 else None
        to_loc = form.to_location.data if form.to_location.data != 0 else None
        
        if from_loc is None and to_loc is None:
            flash('At least one of From Location or To Location must be selected!', 'danger')
            return render_template('movement_form.html', form=form, title='New Movement')
        
        movement = ProductMovement(
            product_id=form.product_id.data,
            from_location=from_loc,
            to_location=to_loc,
            qty=form.qty.data
        )
        db.session.add(movement)
        db.session.commit()
        flash('Movement recorded successfully!', 'success')
        return redirect(url_for('main.movements'))
    
    return render_template('movement_form.html', form=form, title='New Movement')

@bp.route('/report')
def report():
    query = text("""
        SELECT p.product_id, p.name AS product_name, l.location_id, l.name AS location_name, SUM(qty_signed) AS balance
        FROM (
          SELECT product_id, to_location AS location_id, qty AS qty_signed FROM product_movement WHERE to_location IS NOT NULL
          UNION ALL
          SELECT product_id, from_location AS location_id, -qty AS qty_signed FROM product_movement WHERE from_location IS NOT NULL
        ) t
        JOIN product p ON p.product_id=t.product_id
        JOIN location l ON l.location_id=t.location_id
        GROUP BY p.product_id, p.name, l.location_id, l.name
        ORDER BY p.product_id, l.location_id
    """)
    
    result = db.session.execute(query)
    balances = result.fetchall()
    
    return render_template('report.html', balances=balances)
