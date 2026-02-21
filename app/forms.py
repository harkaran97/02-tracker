from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, TextAreaField,
    DateField, BooleanField, SubmitField,
)
from wtforms.validators import DataRequired, Optional, NumberRange, URL

CONDITION_CHOICES = [
    ("", "-- Select --"),
    ("concours", "Concours"),
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("fair", "Fair"),
    ("project", "Project"),
]

MOT_CHOICES = [
    ("", "-- Select --"),
    ("valid", "Valid MOT"),
    ("sorn", "SORN"),
    ("exempt", "Historic/Exempt"),
]

SOURCE_SITE_CHOICES = [
    ("", "-- Select --"),
    ("ebay", "eBay"),
    ("autotrader", "AutoTrader"),
    ("carandclassic", "Car & Classic"),
    ("pistonheads", "PistonHeads"),
    ("facebook", "Facebook Marketplace"),
    ("club", "BMW 2002 Club"),
    ("other", "Other"),
]


class RegistryCarForm(FlaskForm):
    variant_id = SelectField("Model Variant", coerce=int, validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired(), NumberRange(min=1966, max=1977)])
    colour = StringField("Colour", validators=[Optional()])
    chassis_prefix = StringField("Chassis Prefix", validators=[Optional()])
    location_region = StringField("Region / County", validators=[Optional()])
    condition = SelectField("Condition", choices=CONDITION_CHOICES, validators=[Optional()])
    mot_status = SelectField("MOT Status", choices=MOT_CHOICES, validators=[Optional()])
    mot_expiry = DateField("MOT Expiry", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    source = StringField("Source", validators=[Optional()])
    submit = SubmitField("Save")


class ListingForm(FlaskForm):
    variant_id = SelectField("Model Variant", coerce=int, validators=[DataRequired()])
    title = StringField("Listing Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional(), NumberRange(min=1966, max=1977)])
    price_gbp = IntegerField("Price (£)", validators=[DataRequired(), NumberRange(min=0)])
    mileage = IntegerField("Mileage", validators=[Optional()])
    condition = SelectField("Condition", choices=CONDITION_CHOICES, validators=[Optional()])
    colour = StringField("Colour", validators=[Optional()])
    location = StringField("Location", validators=[Optional()])
    source_site = SelectField("Source Site", choices=SOURCE_SITE_CHOICES, validators=[Optional()])
    source_url = StringField("Listing URL", validators=[Optional(), URL()])
    description = TextAreaField("Description", validators=[Optional()])
    is_sold = BooleanField("Sold?")
    listed_at = DateField("Date Listed", validators=[Optional()])
    sold_at = DateField("Date Sold", validators=[Optional()])
    submit = SubmitField("Save")


class PriceRecordForm(FlaskForm):
    variant_id = SelectField("Model Variant", coerce=int, validators=[DataRequired()])
    price_gbp = IntegerField("Sale Price (£)", validators=[DataRequired(), NumberRange(min=0)])
    year_of_car = IntegerField("Year of Car", validators=[Optional(), NumberRange(min=1966, max=1977)])
    condition = SelectField("Condition", choices=CONDITION_CHOICES, validators=[Optional()])
    source = StringField("Source", validators=[Optional()])
    sold_date = DateField("Date Sold", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save")
