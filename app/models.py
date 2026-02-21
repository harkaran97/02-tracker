from datetime import datetime, timezone
from app import db


class ModelVariant(db.Model):
    """Reference table for BMW 2002 model variants."""
    __tablename__ = "model_variants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    year_start = db.Column(db.Integer, nullable=False)
    year_end = db.Column(db.Integer, nullable=False)
    engine_cc = db.Column(db.Integer, nullable=False)
    bhp = db.Column(db.Integer)
    description = db.Column(db.Text)
    estimated_uk_survivors = db.Column(db.Integer)

    registry_cars = db.relationship("RegistryCar", backref="variant", lazy=True)
    listings = db.relationship("Listing", backref="variant", lazy=True)

    def __repr__(self):
        return f"<ModelVariant {self.name}>"


class RegistryCar(db.Model):
    """Known surviving BMW 2002s in the UK."""
    __tablename__ = "registry_cars"

    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("model_variants.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(40))
    chassis_prefix = db.Column(db.String(20))
    location_region = db.Column(db.String(60))
    condition = db.Column(db.String(20))  # concours, excellent, good, fair, project
    mot_status = db.Column(db.String(20))  # valid, sorn, exempt
    mot_expiry = db.Column(db.Date)
    notes = db.Column(db.Text)
    source = db.Column(db.String(120))  # where we learned about this car
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<RegistryCar {self.year} {self.variant.name if self.variant else '?'}>"


class Listing(db.Model):
    """For-sale listings tracked from UK marketplaces."""
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("model_variants.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    price_gbp = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer)
    condition = db.Column(db.String(20))
    colour = db.Column(db.String(40))
    location = db.Column(db.String(80))
    source_site = db.Column(db.String(60))  # ebay, autotrader, carandclassic, etc.
    source_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    is_sold = db.Column(db.Boolean, default=False)
    listed_at = db.Column(db.Date)
    sold_at = db.Column(db.Date)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Listing {self.title} £{self.price_gbp}>"


class PriceRecord(db.Model):
    """Historical price data points for market analysis."""
    __tablename__ = "price_records"

    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("model_variants.id"), nullable=False)
    price_gbp = db.Column(db.Integer, nullable=False)
    year_of_car = db.Column(db.Integer)
    condition = db.Column(db.String(20))
    source = db.Column(db.String(60))
    sold_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    variant = db.relationship("ModelVariant", backref="price_records")

    def __repr__(self):
        return f"<PriceRecord £{self.price_gbp} on {self.sold_date}>"
