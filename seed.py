from app import create_app, db
from app.models import Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        print("Seeding products...")
        products = [
            Product(name='Laptop Dell XPS 15'),
            Product(name='Wireless Mouse Logitech'),
            Product(name='USB-C Cable'),
            Product(name='Monitor Samsung 27"')
        ]
        db.session.add_all(products)
        db.session.commit()
        
        print("Seeding locations...")
        locations = [
            Location(name='Warehouse A'),
            Location(name='Warehouse B'),
            Location(name='Retail Store'),
            Location(name='Distribution Center')
        ]
        db.session.add_all(locations)
        db.session.commit()
        
        print("Seeding product movements...")
        movements = []
        
        base_time = datetime.utcnow() - timedelta(days=30)
        
        for i in range(20):
            movement_type = random.choice(['in', 'out', 'transfer'])
            product = random.choice(products)
            qty = random.randint(5, 50)
            timestamp = base_time + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            
            if movement_type == 'in':
                movement = ProductMovement(
                    product_id=product.product_id,
                    from_location=None,
                    to_location=random.choice(locations).location_id,
                    qty=qty,
                    timestamp=timestamp
                )
            elif movement_type == 'out':
                movement = ProductMovement(
                    product_id=product.product_id,
                    from_location=random.choice(locations).location_id,
                    to_location=None,
                    qty=qty,
                    timestamp=timestamp
                )
            else:
                from_loc = random.choice(locations)
                to_loc = random.choice([l for l in locations if l != from_loc])
                movement = ProductMovement(
                    product_id=product.product_id,
                    from_location=from_loc.location_id,
                    to_location=to_loc.location_id,
                    qty=qty,
                    timestamp=timestamp
                )
            
            movements.append(movement)
        
        db.session.add_all(movements)
        db.session.commit()
        
        print(f"Database seeded successfully!")
        print(f"- {len(products)} products")
        print(f"- {len(locations)} locations")
        print(f"- {len(movements)} movements")

if __name__ == '__main__':
    seed_database()
