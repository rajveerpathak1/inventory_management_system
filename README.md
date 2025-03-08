# Inventory Management System

##  Overview
This is a simple **Inventory Management System** built with **Flask** and **MySQL**. It allows users to:
- Add new inventory items
- View the current inventory
- Update existing items
- Delete items from the inventory

##  Project Structure
```
📂 inventory_management_system
│-- 📂 templates/      # HTML templates (index.html, etc.)
│-- 📂 static/         # CSS, JS, Images
│-- 📂 migrations/     # Database migrations (if using Flask-Migrate)
│-- 📄 app.py          # Main Flask application
│-- 📄 models.py       # Database models (SQLAlchemy)
│-- 📄 config.py       # App configurations
│-- 📄 requirements.txt # Project dependencies
│-- 📄 README.md       # Project documentation
```

##  Installation & Setup
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/inventory-management.git
cd inventory-management
```

### **2️⃣ Create and Activate a Virtual Environment**
```sh
# For Windows\python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure MySQL Database**
Update `app.py` with your MySQL credentials:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:your_password@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
```

### **5️⃣ Initialize the Database**
```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### **6️⃣ Run the Application**
```sh
flask run
```
Visit **http://127.0.0.1:5000/** in your browser.

---

##  Features
✅ Add inventory items  
✅ Update item details  
✅ Delete items  
✅ Flash messages for user feedback  
✅ Responsive UI  


##  Technologies Used
- **Flask** (Python Web Framework)
- **MySQL** (Database)
- **SQLAlchemy** (ORM for database management)
- **Jinja2** (HTML templating)
- **Bootstrap** (For styling)


##  Contributing
Feel free to submit a pull request if you’d like to contribute! 😊

