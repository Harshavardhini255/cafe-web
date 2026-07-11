import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from models import db, MenuItem, Order, Reservation, Review, Subscriber, ContactMessage

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

@app.route('/')
def index():
    menu_items = MenuItem.query.filter_by(available=True).all()
    reviews = Review.query.filter_by(approved=True).all()
    return render_template('index.html', menu_items=menu_items, reviews=reviews)

@app.route('/api/menu', methods=['GET'])
def get_menu():
    items = MenuItem.query.filter_by(available=True).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    if not data or not data.get('items'):
        return jsonify({'error': 'No items in order'}), 400
    order = Order(
        customer_name=data.get('name', 'Guest'),
        customer_phone=data.get('phone', ''),
        items=json.dumps(data['items']),
        total=data.get('total', 0),
        order_type=data.get('order_type', 'takeaway'),
        notes=data.get('notes', ''),
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'success': True, 'order_id': order.id, 'message': 'Order placed! We\'ll DM you shortly.'})

@app.route('/api/order/lookup', methods=['GET'])
def order_lookup():
    phone = request.args.get('phone', '').strip()
    if not phone:
        return jsonify({'error': 'Phone number required'}), 400
    orders = Order.query.filter_by(customer_phone=phone).order_by(Order.created_at.desc()).limit(5).all()
    return jsonify([o.to_dict() for o in orders])

@app.route('/api/reserve/<int:res_id>', methods=['GET'])
def get_reservation(res_id):
    res = Reservation.query.get_or_404(res_id)
    return jsonify(res.to_dict())

@app.route('/api/reserve', methods=['POST'])
def make_reservation():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    reservation = Reservation(
        customer_name=data['name'],
        customer_phone=data.get('phone', ''),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time=data.get('time', '7:00 PM'),
        guests=data.get('guests', 2),
        occasion=data.get('occasion', 'Casual Dining'),
        notes=data.get('notes', ''),
        status='pending'
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'success': True, 'reservation_id': reservation.id, 'message': 'Reservation request noted! We\'ll DM you to confirm.'})

@app.route('/api/review', methods=['POST'])
def submit_review():
    data = request.json
    if not data or not data.get('name') or not data.get('content'):
        return jsonify({'error': 'Name and review are required'}), 400
    review = Review(
        customer_name=data['name'],
        rating=data.get('rating', 5),
        content=data['content'],
        approved=False
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Review submitted! Will appear after approval.'})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data.get('email', '').strip().lower()
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({'success': True, 'message': 'Already subscribed!'})
    subscriber = Subscriber(email=email)
    db.session.add(subscriber)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Subscribed successfully!'})

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    if not data or not data.get('name') or not data.get('message'):
        return jsonify({'error': 'Name and message are required'}), 400
    msg = ContactMessage(
        name=data['name'],
        email=data.get('email', ''),
        subject=data.get('subject', ''),
        message=data['message'],
        read=False
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message sent! We\'ll get back to you soon.'})

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_do_login():
    data = request.form
    pw = data.get('password', '')
    if pw == os.environ.get('ADMIN_PASSWORD', 'wakecup123'):
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html', error='Wrong password')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    orders = Order.query.order_by(Order.created_at.desc()).all()
    reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
    menu_items = MenuItem.query.all()
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    subscribers = Subscriber.query.order_by(Subscriber.created_at.desc()).all()
    contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/dashboard.html',
        orders=orders, reservations=reservations,
        menu_items=menu_items, reviews=reviews,
        subscribers=subscribers, contacts=contacts)

@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    order = Order.query.get_or_404(order_id)
    order.status = request.json.get('status', order.status)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/reservation/<int:res_id>/status', methods=['POST'])
def update_reservation_status(res_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    res = Reservation.query.get_or_404(res_id)
    res.status = request.json.get('status', res.status)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/review/<int:review_id>/approve', methods=['POST'])
def approve_review(review_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    review = Review.query.get_or_404(review_id)
    review.approved = not review.approved
    db.session.commit()
    return jsonify({'success': True, 'approved': review.approved})

@app.route('/admin/menu/add', methods=['POST'])
def add_menu_item():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    price = data.get('price', 0)
    if price is None or (isinstance(price, float) and price != price):
        price = 0
    item = MenuItem(
        name=data['name'],
        category=data.get('category', 'Main'),
        description=data.get('description', ''),
        price=price,
        image=data.get('image', 'product-1.png'),
        available=True
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True, 'item': item.to_dict()})

@app.route('/admin/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/menu/<int:item_id>/edit', methods=['POST'])
def edit_menu_item(item_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    item = MenuItem.query.get_or_404(item_id)
    data = request.json
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.category = data.get('category', item.category)
    item.image = data.get('image', item.image)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'success': True, 'item': item.to_dict()})

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','webp','mp4'}
def allowed_file(name):
    return '.' in name and name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/images', methods=['GET'])
def list_images():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    static_dir = os.path.join(app.root_path, 'static')
    files = []
    for f in os.listdir(static_dir):
        if allowed_file(f):
            files.append(f)
    return jsonify(sorted(files))

@app.route('/admin/upload', methods=['POST'])
def upload_image():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Allowed: png, jpg, jpeg, gif, webp, mp4'}), 400
    filename = secure_filename(file.filename)
    static_dir = os.path.join(app.root_path, 'static')
    file.save(os.path.join(static_dir, filename))
    return jsonify({'success': True, 'filename': filename})

_init_done = False

@app.before_request
def init_db():
    global _init_done
    if _init_done:
        return
    db.create_all()
    existing_names = {item.name for item in MenuItem.query.with_entities(MenuItem.name).all()}
    seeds = [
        MenuItem(name='Chicken Marinara Sandwich', category='Sandwich', description='Slow-simmered in our in-house marinara, juicy chicken & melted cheese — just how it should be.', price=200, image='chicken-marinara.jpg'),
        MenuItem(name='Golden Crunch Chicken Burger', category='Burger', description='Crispy golden chicken burger with premium toppings.', price=220, image='golden-crunch-burger.jpg'),
        MenuItem(name='Butterfly Chicken Bites', category='Snack', description='Crispy butterfly-cut chicken bites — golden, crunchy & perfect for sharing!', price=180, image='potato-chicken-skewers.jpg'),
        MenuItem(name='Bread Pudding', category='Dessert', description='Warm, soft bread pudding baked to perfection — comfort in every bite.', price=0, image='bread-pudding.jpg'),
        MenuItem(name='Buttery Herbed Rice with Spicy Honey Glazed Chicken', category='Main', description='Hot, buttery herbed rice served with juicy, flavourful spicy honey glazed chicken — so comforting yet filling.', price=250, image='herbed-rice-chicken.jpg'),
        MenuItem(name='Classic Tiramisu', category='Dessert', description='Coffee, cream, cocoa — layers of perfection.', price=250, image='classic-tiramisu.jpg'),
        MenuItem(name='Pistachio Tiramisu', category='Dessert', description='Layers of love & pistachio — a nutty twist on the classic.', price=280, image='pistachio-tiramisu.jpg'),
        MenuItem(name='Choco Hazelnut Tiramisu', category='Dessert', description='Rich chocolate & hazelnut layered tiramisu.', price=280, image='choco-hazelnut-tiramisu.jpg'),
        MenuItem(name='Mini Blueberry Bliss', category='Dessert', description='Delightful mini blueberry dessert — sweet & tangy.', price=200, image='mini-blueberry-bliss.jpg'),
        MenuItem(name='Caramel Crunch', category='Dessert', description='Irresistible caramel crunch dessert.', price=220, image='caramel-crunch.jpg'),
        MenuItem(name='Classic Affogato', category='Beverage', description='Espresso poured over vanilla ice cream — a classic Italian finish.', price=180, image='classic-affogato.jpg'),
        MenuItem(name='Cold Kaapi Scoop', category='Beverage', description='Refreshing cold coffee scoop — perfect pick-me-up.', price=160, image='cold-kaapi-scoop.jpg'),
    ]
    new_items = [s for s in seeds if s.name not in existing_names]
    if new_items:
        db.session.add_all(new_items)
        db.session.commit()
    _init_done = True

if __name__ == '__main__':
    app.run(debug=True)
