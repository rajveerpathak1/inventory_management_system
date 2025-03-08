from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models.inventory import db, Inventory

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

@app.route('/')
def index():
    inventory = Inventory.query.all()
    return render_template('index.html', inventory=inventory)


@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    if not name or not quantity or not price:
        flash("All fields are required!", "danger")
        return redirect(url_for('index'))

    new_item = Inventory(name=name, quantity=float(quantity), price=float(price))
    db.session.add(new_item)
    db.session.commit()
    flash("Item added successfully!", "success")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
