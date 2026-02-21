from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func
from app import db
from app.models import ModelVariant, RegistryCar, Listing, PriceRecord
from app.forms import RegistryCarForm, ListingForm, PriceRecordForm

main = Blueprint("main", __name__)


def _variant_choices():
    """Return list of (id, name) tuples for select fields."""
    return [(v.id, v.name) for v in ModelVariant.query.order_by(ModelVariant.name).all()]


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@main.route("/")
def index():
    total_registry = RegistryCar.query.count()
    total_listings = Listing.query.filter_by(is_sold=False).count()
    total_sold = PriceRecord.query.count()
    variants = ModelVariant.query.order_by(ModelVariant.name).all()

    # Aggregate stats per variant
    variant_stats = []
    for v in variants:
        avg_price = (
            db.session.query(func.avg(PriceRecord.price_gbp))
            .filter(PriceRecord.variant_id == v.id)
            .scalar()
        )
        listing_count = Listing.query.filter_by(variant_id=v.id, is_sold=False).count()
        registry_count = RegistryCar.query.filter_by(variant_id=v.id).count()
        variant_stats.append({
            "variant": v,
            "avg_price": int(avg_price) if avg_price else None,
            "listing_count": listing_count,
            "registry_count": registry_count,
        })

    return render_template(
        "index.html",
        total_registry=total_registry,
        total_listings=total_listings,
        total_sold=total_sold,
        variant_stats=variant_stats,
    )


# ---------------------------------------------------------------------------
# Registry — known surviving BMW 02s in the UK
# ---------------------------------------------------------------------------
@main.route("/registry")
def registry():
    variant_filter = request.args.get("variant", type=int)
    condition_filter = request.args.get("condition")

    query = RegistryCar.query.join(ModelVariant)
    if variant_filter:
        query = query.filter(RegistryCar.variant_id == variant_filter)
    if condition_filter:
        query = query.filter(RegistryCar.condition == condition_filter)

    cars = query.order_by(ModelVariant.name, RegistryCar.year).all()
    variants = ModelVariant.query.order_by(ModelVariant.name).all()
    return render_template("registry.html", cars=cars, variants=variants,
                           variant_filter=variant_filter, condition_filter=condition_filter)


@main.route("/registry/add", methods=["GET", "POST"])
def registry_add():
    form = RegistryCarForm()
    form.variant_id.choices = _variant_choices()
    if form.validate_on_submit():
        car = RegistryCar()
        form.populate_obj(car)
        db.session.add(car)
        db.session.commit()
        flash("Car added to registry.", "success")
        return redirect(url_for("main.registry"))
    return render_template("registry_form.html", form=form, title="Add Car to Registry")


@main.route("/registry/<int:car_id>/edit", methods=["GET", "POST"])
def registry_edit(car_id):
    car = RegistryCar.query.get_or_404(car_id)
    form = RegistryCarForm(obj=car)
    form.variant_id.choices = _variant_choices()
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        flash("Registry entry updated.", "success")
        return redirect(url_for("main.registry"))
    return render_template("registry_form.html", form=form, title="Edit Registry Entry")


@main.route("/registry/<int:car_id>/delete", methods=["POST"])
def registry_delete(car_id):
    car = RegistryCar.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash("Registry entry deleted.", "info")
    return redirect(url_for("main.registry"))


# ---------------------------------------------------------------------------
# Listings — for-sale tracker
# ---------------------------------------------------------------------------
@main.route("/listings")
def listings():
    show_sold = request.args.get("sold", "0") == "1"
    variant_filter = request.args.get("variant", type=int)

    query = Listing.query.join(ModelVariant)
    if not show_sold:
        query = query.filter(Listing.is_sold == False)  # noqa: E712
    if variant_filter:
        query = query.filter(Listing.variant_id == variant_filter)

    all_listings = query.order_by(Listing.listed_at.desc()).all()
    variants = ModelVariant.query.order_by(ModelVariant.name).all()

    # Compute deal ratings for active listings
    deal_ratings = {}
    for listing in all_listings:
        if not listing.is_sold:
            deal_ratings[listing.id] = _compute_deal_rating(listing)

    return render_template("listings.html", listings=all_listings, variants=variants,
                           variant_filter=variant_filter, show_sold=show_sold,
                           deal_ratings=deal_ratings)


@main.route("/listings/add", methods=["GET", "POST"])
def listing_add():
    form = ListingForm()
    form.variant_id.choices = _variant_choices()
    if form.validate_on_submit():
        listing = Listing()
        form.populate_obj(listing)
        db.session.add(listing)
        db.session.commit()
        flash("Listing added.", "success")
        return redirect(url_for("main.listings"))
    return render_template("listing_form.html", form=form, title="Add Listing")


@main.route("/listings/<int:listing_id>/edit", methods=["GET", "POST"])
def listing_edit(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    form = ListingForm(obj=listing)
    form.variant_id.choices = _variant_choices()
    if form.validate_on_submit():
        form.populate_obj(listing)
        db.session.commit()
        flash("Listing updated.", "success")
        return redirect(url_for("main.listings"))
    return render_template("listing_form.html", form=form, title="Edit Listing")


@main.route("/listings/<int:listing_id>/delete", methods=["POST"])
def listing_delete(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted.", "info")
    return redirect(url_for("main.listings"))


# ---------------------------------------------------------------------------
# Market Analysis
# ---------------------------------------------------------------------------
@main.route("/market")
def market():
    variants = ModelVariant.query.order_by(ModelVariant.name).all()
    variant_filter = request.args.get("variant", type=int)

    # Build price history data for chart
    price_query = PriceRecord.query.join(ModelVariant).order_by(PriceRecord.sold_date)
    if variant_filter:
        price_query = price_query.filter(PriceRecord.variant_id == variant_filter)

    price_records = price_query.all()

    # Per-variant summary stats
    analysis = []
    target_variants = [ModelVariant.query.get(variant_filter)] if variant_filter else variants
    for v in target_variants:
        records = [r for r in price_records if r.variant_id == v.id]
        if not records:
            continue
        prices = [r.price_gbp for r in records]
        recent = [r for r in records if r.sold_date >= date(2025, 1, 1)]
        recent_prices = [r.price_gbp for r in recent] if recent else prices

        analysis.append({
            "variant": v,
            "count": len(records),
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": int(sum(prices) / len(prices)),
            "recent_avg": int(sum(recent_prices) / len(recent_prices)),
            "trend": _price_trend(records),
        })

    # Chart data: group by variant name → list of {date, price}
    chart_data = {}
    for r in price_records:
        vname = r.variant.name
        if vname not in chart_data:
            chart_data[vname] = []
        chart_data[vname].append({
            "date": r.sold_date.isoformat(),
            "price": r.price_gbp,
            "condition": r.condition or "unknown",
        })

    return render_template("market.html", variants=variants, analysis=analysis,
                           chart_data=chart_data, variant_filter=variant_filter)


@main.route("/market/add", methods=["GET", "POST"])
def price_record_add():
    form = PriceRecordForm()
    form.variant_id.choices = _variant_choices()
    if form.validate_on_submit():
        record = PriceRecord()
        form.populate_obj(record)
        db.session.add(record)
        db.session.commit()
        flash("Price record added.", "success")
        return redirect(url_for("main.market"))
    return render_template("price_form.html", form=form, title="Add Price Record")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _price_trend(records):
    """Return 'rising', 'stable', or 'falling' based on simple comparison."""
    if len(records) < 2:
        return "stable"
    sorted_recs = sorted(records, key=lambda r: r.sold_date)
    mid = len(sorted_recs) // 2
    early_avg = sum(r.price_gbp for r in sorted_recs[:mid]) / mid
    late_avg = sum(r.price_gbp for r in sorted_recs[mid:]) / (len(sorted_recs) - mid)
    pct_change = (late_avg - early_avg) / early_avg * 100
    if pct_change > 5:
        return "rising"
    elif pct_change < -5:
        return "falling"
    return "stable"


def _compute_deal_rating(listing):
    """Rate a listing against recent market data. Returns dict with rating info."""
    avg_price = (
        db.session.query(func.avg(PriceRecord.price_gbp))
        .filter(
            PriceRecord.variant_id == listing.variant_id,
            PriceRecord.condition == listing.condition,
        )
        .scalar()
    )
    if not avg_price:
        # Fall back to variant average regardless of condition
        avg_price = (
            db.session.query(func.avg(PriceRecord.price_gbp))
            .filter(PriceRecord.variant_id == listing.variant_id)
            .scalar()
        )
    if not avg_price:
        return {"rating": "unknown", "label": "No data", "css": "secondary",
                "detail": "Not enough price history to assess"}

    avg_price = int(avg_price)
    diff_pct = (listing.price_gbp - avg_price) / avg_price * 100

    if diff_pct < -15:
        return {"rating": "great", "label": "Great deal", "css": "success",
                "detail": f"£{listing.price_gbp:,} is {abs(diff_pct):.0f}% below avg £{avg_price:,}"}
    elif diff_pct < -5:
        return {"rating": "good", "label": "Good price", "css": "info",
                "detail": f"£{listing.price_gbp:,} is {abs(diff_pct):.0f}% below avg £{avg_price:,}"}
    elif diff_pct <= 10:
        return {"rating": "fair", "label": "Fair price", "css": "warning",
                "detail": f"£{listing.price_gbp:,} is close to avg £{avg_price:,}"}
    else:
        return {"rating": "high", "label": "Above market", "css": "danger",
                "detail": f"£{listing.price_gbp:,} is {diff_pct:.0f}% above avg £{avg_price:,}"}
