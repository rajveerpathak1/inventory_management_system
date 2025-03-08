from flask import request, redirect, url_for, flash, render_template
from models.inventory import db, Inventory

def add_item():
    name = request.form['name']
    quantity = float(request.form['quantity'])
    price = float(request.form['price'])

    existing_item = Inventory.query.filter_by(name=name).first()
    if existing_item:
        flash("Item already exists!", "error")
        return redirect(url_for('index'))

    new_item = Inventory(name=name, quantity=quantity, price=price)
    db.session.add(new_item)
    db.session.commit()
    flash("Item added successfully!", "success")
    return redirect(url_for('index'))

def delete_item(item_id):
    item = Inventory.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted!", "success")
    return redirect(url_for('index'))

def update_item(item_id):
    item = Inventory.query.get(item_id)
    if item:
        item.name = request.form['name']
        item.quantity = float(request.form['quantity'])
        item.price = float(request.form['price'])
        db.session.commit()
        flash("Item updated successfully!", "success")
    return redirect(url_for('index'))

def search_items():
    query = request.args.get('query')
    results = Inventory.query.filter(Inventory.name.ilike(f"%{query}%")).all()
    return render_template('index.html', inventory=results)
