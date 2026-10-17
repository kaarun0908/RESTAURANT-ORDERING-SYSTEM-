from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "foodies-v1-change-this-key"
DB_PATH = Path(__file__).with_name("foodies.db")

MENU = [
    {"id": 1, "name": "Chicken Biryani", "category": "Biryani", "price": 180, "rating": 4.6, "image": "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=900&q=80", "veg": False},
    {"id": 2, "name": "Margherita Pizza", "category": "Pizza", "price": 220, "rating": 4.4, "image": "https://images.unsplash.com/photo-157 pizza?auto=format&fit=crop&w=900&q=80".replace(" ", ""), "veg": True},
    {"id": 3, "name": "Masala Dosa", "category": "South Indian", "price": 90, "rating": 4.5, "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=900&q=80", "veg": True},
    {"id": 4, "name": "Classic Burger", "category": "Burgers", "price": 150, "rating": 4.3, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80", "veg": False},
    {"id": 5, "name": "Paneer Wrap", "category": "Wraps", "price": 130, "rating": 4.2, "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=900&q=80", "veg": True},
    {"id": 6, "name": "Idli & Sambar", "category": "South Indian", "price": 70, "rating": 4.1, "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=900&q=80", "veg": True},
    {"id": 7, "name": "Hakka Noodles", "category": "Chinese", "price": 160, "rating": 4.3, "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=900&q=80", "veg": False},
    {"id": 8, "name": "Chocolate Brownie", "category": "Desserts", "price": 100, "rating": 4.7, "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80", "veg": True},
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")

@app.context_processor
def common_template_values():
    return {"cart_count": sum(session.get("cart", {}).values())}

@app.route("/")
def home():
    return render_template("index.html", menu=MENU, user=session.get("user"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Enter all details. Password must contain at least 6 characters.", "error")
            return redirect(url_for("register"))
        try:
            with get_db() as db:
                db.execute("INSERT INTO users(name, email, password_hash) VALUES (?, ?, ?)",
                           (name, email, generate_password_hash(password)))
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "error")
    return render_template("auth.html", mode="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"]}
            flash("Welcome back, " + user["name"] + "!", "success")
            return redirect(url_for("home"))
        flash("Invalid email or password.", "error")
    return render_template("auth.html", mode="login")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    items = []
    total = 0
    for food in MENU:
        quantity = cart_data.get(str(food["id"]), 0)
        if quantity:
            row = dict(food)
            row["quantity"] = quantity
            row["subtotal"] = quantity * food["price"]
            total += row["subtotal"]
            items.append(row)
    return render_template("cart.html", items=items, total=total)

@app.route("/cart/add/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    if not any(food["id"] == item_id for food in MENU):
        flash("Menu item not found.", "error")
        return redirect(url_for("home"))
    cart_data = session.get("cart", {})
    key = str(item_id)
    cart_data[key] = cart_data.get(key, 0) + 1
    session["cart"] = cart_data
    flash("Item added to your cart.", "success")
    return redirect(request.referrer or url_for("home"))

@app.route("/cart/update/<int:item_id>", methods=["POST"])
def update_cart(item_id):
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 1
    cart_data = session.get("cart", {})
    if quantity <= 0:
        cart_data.pop(str(item_id), None)
    else:
        cart_data[str(item_id)] = min(quantity, 99)
    session["cart"] = cart_data
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["POST"])
def checkout():
    if not session.get("user"):
        flash("Please log in before placing an order.", "error")
        return redirect(url_for("login"))
    cart_data = session.get("cart", {})
    chosen = []
    total = 0
    for food in MENU:
        quantity = cart_data.get(str(food["id"]), 0)
        if quantity:
            chosen.append(f'{food["name"]} x {quantity}')
            total += food["price"] * quantity
    if not chosen:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart"))
    with get_db() as db:
        db.execute("INSERT INTO orders(user_id, items, total) VALUES (?, ?, ?)",
                   (session["user"]["id"], ", ".join(chosen), total))
    session["cart"] = {}
    flash("Order placed successfully! Total: ₹" + str(total), "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
