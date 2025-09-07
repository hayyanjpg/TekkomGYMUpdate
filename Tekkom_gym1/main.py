from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from functools import wraps
import re

app = Flask(__name__)

# Konfigurasi Aplikasi dan Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TekkomGym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)

# Model Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    images = db.Column(db.String(500), nullable=True)

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)

# Middleware untuk Autentikasi Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Silakan login sebagai admin untuk mengakses halaman ini.", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# Inisialisasi database
with app.app_context():
    db.create_all()

# Halaman Home
@app.route("/")
def home():
    return render_template("index.html")

# Halaman Login Pengguna
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("Username tidak terdaftar.", "danger")
            return render_template("login.html")

        if not check_password_hash(user.password, password):
            flash("Password salah.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        flash("Login berhasil. Selamat datang, {}!".format(user.username), "success")
        return redirect(url_for("market"))

    return render_template("login.html")

# Halaman Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "success")
    return redirect(url_for("home"))

# Halaman Registrasi Pengguna
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validasi Username
        if len(username) < 12:
            flash("Username harus minimal 12 karakter.", "danger")
            return render_template("register.html")

        # Validasi Password
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            flash("Password harus minimal 8 karakter, mengandung huruf besar, huruf kecil, angka, dan karakter unik.", "danger")
            return render_template("register.html")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username atau email sudah terdaftar", "danger")
            return render_template("register.html")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registrasi berhasil! Silakan login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Helper Function: Tambahkan pengguna default
def initialize_default_user():
    default_user = User.query.filter_by(username="aan").first()
    if not default_user:
        hashed_password = generate_password_hash("1", method="pbkdf2:sha256")
        new_user = User(username="aan", email="a@gmail.com", password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("Pengguna default berhasil dibuat!")

def initialize_default_admin():
    default_admin = Admin.query.filter_by(username="admin").first()
    if not default_admin:
        hashed_password = generate_password_hash("1", method="pbkdf2:sha256")
        new_admin = Admin(username="admin", email="admin@example.com", phone="123456789", password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

# Inisialisasi Database
with app.app_context():
    db.create_all()
    initialize_default_admin()

# Routes
@app.route("/market")
def market():
    products = Product.query.all()
    return render_template("market.html", products=products)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin_id"] = admin.id
            flash("Login berhasil!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Username atau password salah!", "danger")
    return render_template("admin_login.html")

@app.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    flash("Anda telah logout dari admin.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    products = Product.query.all()
    memberships = Membership.query.all()
    admins = Admin.query.all()
    return render_template("admin_dashboard.html", products=products, memberships=memberships, admins=admins)

@app.route("/admin/add_product", methods=["POST"])
@admin_required
def add_product():
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    stock = request.form.get("stock")
    images = request.form.get("images")

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        flash("Harga harus berupa angka dan stok harus berupa bilangan bulat.", "danger")
        return redirect(url_for("admin_dashboard"))

    new_product = Product(name=name, description=description, price=price, stock=stock, images=images)
    db.session.add(new_product)
    db.session.commit()

    flash("Produk berhasil ditambahkan!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/update_product/<int:product_id>", methods=["POST"])
@admin_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.name = request.form.get("name")
    product.description = request.form.get("description")
    product.price = request.form.get("price")
    product.stock = request.form.get("stock")
    product.images = request.form.get("images")

    try:
        product.price = float(product.price)
        product.stock = int(product.stock)
    except ValueError:
        flash("Harga atau stok tidak valid!", "danger")
        return redirect(url_for("admin_dashboard"))

    db.session.commit()
    flash("Produk berhasil diperbarui!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_product", methods=["POST"])
@admin_required
def delete_product():
    product_id = request.form.get("product_id")  # Ambil dari form
    if not product_id:
        flash("ID produk tidak valid.", "danger")
        return redirect(url_for("admin_dashboard"))

    product = Product.query.get(product_id)
    if not product:
        flash("Produk tidak ditemukan.", "danger")
        return redirect(url_for("admin_dashboard"))

    db.session.delete(product)
    db.session.commit()
    flash("Produk berhasil dihapus!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/add_membership/product_id", methods=["POST"])
@admin_required
def add_membership():
    if request.method == "POST":
        membership_type = request.form.get("type")
        duration = request.form.get("duration")
        price = request.form.get("price")
        status = request.form.get("status")

        status = True if status == 'true' else False

        try:
            price = float(price)
        except ValueError:
            flash("Harga membership harus berupa angka!", "danger")
            return redirect(url_for("admin_dashboard"))

        new_membership = Membership(type=membership_type, duration=duration, price=price, status=status)
        db.session.add(new_membership)
        db.session.commit()
        flash("Membership berhasil ditambahkan!", "success")

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_membership/<int:membership_id>", methods=["POST"])
@admin_required
def delete_membership(membership_id):
    membership = Membership.query.get_or_404(membership_id)
    db.session.delete(membership)
    db.session.commit()
    flash("Membership berhasil dihapus!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/api/memberships", methods=["GET"])
def get_memberships():
    memberships = Membership.query.all()
    memberships_list = [
        {
            "id": membership.id,
            "type": membership.type,
            "duration": membership.duration,
            "price": membership.price,
            "status": "Aktif" if membership.status else "Tidak Aktif"
        }
        for membership in memberships
    ]
    return {"memberships": memberships_list}

@app.route("/admin/add_admin", methods=["POST"])
@admin_required
def add_admin():
    username = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    if Admin.query.filter((Admin.username == username) | (Admin.email == email)).first():
        flash("Username atau email sudah terdaftar!", "danger")
        return redirect(url_for("admin_dashboard"))

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_admin = Admin(username=username, email=email, phone=phone, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    flash("Admin berhasil ditambahkan!", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
