"""Seed the database with BMW 2002 model variants and sample data."""

from datetime import date
from app import db
from app.models import ModelVariant, RegistryCar, Listing, PriceRecord

VARIANTS = [
    {
        "name": "1502",
        "year_start": 1975,
        "year_end": 1977,
        "engine_cc": 1573,
        "bhp": 75,
        "description": "Budget entry-level variant with the smaller 1.6L engine. "
                       "Produced near the end of the 02 series run.",
        "estimated_uk_survivors": 15,
    },
    {
        "name": "1602",
        "year_start": 1966,
        "year_end": 1975,
        "engine_cc": 1573,
        "bhp": 85,
        "description": "The original 02 series car. 1.6-litre single-carb engine. "
                       "Predecessor to the 2002 and the car that started the sport sedan revolution.",
        "estimated_uk_survivors": 80,
    },
    {
        "name": "2002",
        "year_start": 1968,
        "year_end": 1976,
        "engine_cc": 1990,
        "bhp": 100,
        "description": "The iconic model. 2.0-litre single-carb engine producing 100 bhp. "
                       "The car that established BMW's reputation as a driver's marque.",
        "estimated_uk_survivors": 250,
    },
    {
        "name": "2002 Automatic",
        "year_start": 1969,
        "year_end": 1975,
        "engine_cc": 1990,
        "bhp": 100,
        "description": "Automatic transmission variant of the 2002. Three-speed ZF auto box. "
                       "Less sought-after but increasingly rare.",
        "estimated_uk_survivors": 30,
    },
    {
        "name": "2002 tii",
        "year_start": 1971,
        "year_end": 1975,
        "engine_cc": 1990,
        "bhp": 130,
        "description": "Kugelfischer mechanical fuel injection. 130 bhp. "
                       "The hot rod of the range — highly prized by collectors.",
        "estimated_uk_survivors": 60,
    },
    {
        "name": "2002 Turbo",
        "year_start": 1973,
        "year_end": 1975,
        "engine_cc": 1990,
        "bhp": 170,
        "description": "Europe's first turbocharged production car. KKK turbocharger, "
                       "Kugelfischer injection, 170 bhp. Only ~1,672 made. Extremely collectible.",
        "estimated_uk_survivors": 12,
    },
    {
        "name": "2002 Cabriolet (Baur)",
        "year_start": 1971,
        "year_end": 1975,
        "engine_cc": 1990,
        "bhp": 100,
        "description": "Targa-top conversion by Baur coachbuilders in Stuttgart. "
                       "Removable roof panel with fixed roll bar. Very rare.",
        "estimated_uk_survivors": 20,
    },
    {
        "name": "2002 Touring",
        "year_start": 1971,
        "year_end": 1974,
        "engine_cc": 1990,
        "bhp": 100,
        "description": "Three-door hatchback variant with clever rear tailgate design. "
                       "Never officially sold in RHD but a few were imported.",
        "estimated_uk_survivors": 8,
    },
    {
        "name": "1802",
        "year_start": 1971,
        "year_end": 1975,
        "engine_cc": 1766,
        "bhp": 90,
        "description": "Mid-range 1.8-litre variant slotting between the 1602 and 2002. "
                       "Relatively uncommon in the UK.",
        "estimated_uk_survivors": 25,
    },
]

SAMPLE_REGISTRY = [
    {"variant_name": "2002", "year": 1974, "colour": "Inka Orange", "location_region": "Surrey",
     "condition": "excellent", "mot_status": "valid", "source": "BMW 2002 FAQ Forum", "notes": "Round taillight model, believed original engine"},
    {"variant_name": "2002", "year": 1972, "colour": "Fjord Blue", "location_region": "Yorkshire",
     "condition": "good", "mot_status": "valid", "source": "Car & Classic sighting", "notes": "Square taillight, older restoration"},
    {"variant_name": "2002 tii", "year": 1973, "colour": "Chamonix White", "location_region": "Kent",
     "condition": "concours", "mot_status": "exempt", "source": "Goodwood Revival 2025", "notes": "Kugelfischer injection fully rebuilt, concours winner"},
    {"variant_name": "2002 Turbo", "year": 1974, "colour": "Polaris Silver", "location_region": "London",
     "condition": "excellent", "mot_status": "exempt", "source": "Bonhams auction records", "notes": "One of ~12 known UK survivors, matching numbers"},
    {"variant_name": "1602", "year": 1971, "colour": "Colorado Orange", "location_region": "Norfolk",
     "condition": "fair", "mot_status": "sorn", "source": "eBay listing history", "notes": "Running but needs bodywork, stored in barn"},
    {"variant_name": "2002 Cabriolet (Baur)", "year": 1973, "colour": "Golf Yellow", "location_region": "Oxfordshire",
     "condition": "good", "mot_status": "valid", "source": "BMW Car Club GB register", "notes": "Baur targa, repainted but mechanically sound"},
    {"variant_name": "2002", "year": 1975, "colour": "Malaga Red", "location_region": "Scotland",
     "condition": "project", "mot_status": "sorn", "source": "Facebook group", "notes": "Non-running project, complete car, some rust"},
    {"variant_name": "2002 tii", "year": 1972, "colour": "Sahara Beige", "location_region": "Hampshire",
     "condition": "good", "mot_status": "valid", "source": "PistonHeads classified", "notes": "Imported from Germany in 2018, converted to RHD"},
    {"variant_name": "1802", "year": 1974, "colour": "Riviera Blue", "location_region": "Dorset",
     "condition": "fair", "mot_status": "sorn", "source": "DVLA records check", "notes": "Rare 1802 variant, needs recommissioning"},
    {"variant_name": "2002 Touring", "year": 1972, "colour": "Taiga Green", "location_region": "Cambridgeshire",
     "condition": "excellent", "mot_status": "exempt", "source": "BMW 2002 Touring register", "notes": "One of very few Tourings in the UK, LHD import"},
]

SAMPLE_LISTINGS = [
    {"variant_name": "2002", "title": "1974 BMW 2002 Round Tail - Inka Orange", "year": 1974,
     "price_gbp": 24950, "mileage": 87000, "condition": "good", "colour": "Inka Orange",
     "location": "Brighton, East Sussex", "source_site": "carandclassic",
     "description": "Well-maintained round taillight 2002. Solid floors, recent respray in original Inka. Runs well.",
     "listed_at": date(2026, 2, 10)},
    {"variant_name": "2002 tii", "title": "BMW 2002 tii 1973 - Fully Restored", "year": 1973,
     "price_gbp": 58000, "mileage": 42000, "condition": "concours", "colour": "Chamonix White",
     "location": "Sevenoaks, Kent", "source_site": "pistonheads",
     "description": "Nut-and-bolt restoration completed 2024. Kugelfischer injection rebuilt by specialist. Concours standard.",
     "listed_at": date(2026, 1, 28)},
    {"variant_name": "2002", "title": "BMW 2002 Project Car 1971", "year": 1971,
     "price_gbp": 8500, "mileage": None, "condition": "project", "colour": "White (faded)",
     "location": "Manchester", "source_site": "ebay",
     "description": "Barn find, not running. Needs full restoration. Chassis appears solid under surface rust.",
     "listed_at": date(2026, 2, 15)},
    {"variant_name": "2002 Turbo", "title": "1974 BMW 2002 Turbo - Investment Grade", "year": 1974,
     "price_gbp": 145000, "mileage": 61000, "condition": "excellent", "colour": "Polaris Silver",
     "location": "Chelsea, London", "source_site": "other",
     "description": "Matching numbers Turbo. Full history file. One of the best in the UK.",
     "listed_at": date(2026, 2, 1)},
    {"variant_name": "1602", "title": "1970 BMW 1602 - Honest Driver", "year": 1970,
     "price_gbp": 14500, "mileage": 95000, "condition": "fair", "colour": "Nevada Beige",
     "location": "Bristol", "source_site": "carandclassic",
     "description": "Solid daily-driveable 1602. Some patina, mechanically sorted. MOT until Oct 2026.",
     "listed_at": date(2026, 2, 5)},
    {"variant_name": "2002", "title": "BMW 2002 1976 - Last of the Line", "year": 1976,
     "price_gbp": 19750, "mileage": 104000, "condition": "good", "colour": "Fjord Blue",
     "location": "Edinburgh", "source_site": "facebook",
     "description": "Late model 2002. Some rust in usual places but drives beautifully. Matching numbers.",
     "listed_at": date(2026, 1, 20)},
]

SAMPLE_PRICE_RECORDS = [
    # 2002 standard
    {"variant_name": "2002", "price_gbp": 18000, "year_of_car": 1973, "condition": "good", "source": "Car & Classic", "sold_date": date(2024, 3, 15)},
    {"variant_name": "2002", "price_gbp": 21500, "year_of_car": 1974, "condition": "good", "source": "eBay", "sold_date": date(2024, 6, 22)},
    {"variant_name": "2002", "price_gbp": 23000, "year_of_car": 1972, "condition": "excellent", "source": "PistonHeads", "sold_date": date(2024, 9, 10)},
    {"variant_name": "2002", "price_gbp": 25500, "year_of_car": 1974, "condition": "excellent", "source": "Car & Classic", "sold_date": date(2025, 1, 8)},
    {"variant_name": "2002", "price_gbp": 27000, "year_of_car": 1973, "condition": "excellent", "source": "Bonhams", "sold_date": date(2025, 5, 20)},
    {"variant_name": "2002", "price_gbp": 7500, "year_of_car": 1971, "condition": "project", "source": "eBay", "sold_date": date(2024, 11, 5)},
    {"variant_name": "2002", "price_gbp": 9200, "year_of_car": 1975, "condition": "project", "source": "Facebook", "sold_date": date(2025, 4, 12)},
    {"variant_name": "2002", "price_gbp": 29000, "year_of_car": 1974, "condition": "excellent", "source": "Silverstone Auctions", "sold_date": date(2025, 9, 18)},
    {"variant_name": "2002", "price_gbp": 15500, "year_of_car": 1976, "condition": "fair", "source": "Car & Classic", "sold_date": date(2025, 12, 1)},
    # 2002 tii
    {"variant_name": "2002 tii", "price_gbp": 42000, "year_of_car": 1972, "condition": "good", "source": "Bonhams", "sold_date": date(2024, 4, 18)},
    {"variant_name": "2002 tii", "price_gbp": 48500, "year_of_car": 1973, "condition": "excellent", "source": "Silverstone Auctions", "sold_date": date(2024, 8, 25)},
    {"variant_name": "2002 tii", "price_gbp": 55000, "year_of_car": 1973, "condition": "concours", "source": "Bonhams", "sold_date": date(2025, 3, 14)},
    {"variant_name": "2002 tii", "price_gbp": 52000, "year_of_car": 1971, "condition": "excellent", "source": "PistonHeads", "sold_date": date(2025, 7, 9)},
    # Turbo
    {"variant_name": "2002 Turbo", "price_gbp": 120000, "year_of_car": 1974, "condition": "excellent", "source": "Bonhams", "sold_date": date(2024, 5, 12)},
    {"variant_name": "2002 Turbo", "price_gbp": 135000, "year_of_car": 1974, "condition": "concours", "source": "RM Sotheby's", "sold_date": date(2025, 2, 20)},
    {"variant_name": "2002 Turbo", "price_gbp": 142000, "year_of_car": 1973, "condition": "excellent", "source": "Silverstone Auctions", "sold_date": date(2025, 11, 8)},
    # 1602
    {"variant_name": "1602", "price_gbp": 11000, "year_of_car": 1971, "condition": "good", "source": "eBay", "sold_date": date(2024, 7, 3)},
    {"variant_name": "1602", "price_gbp": 13500, "year_of_car": 1970, "condition": "good", "source": "Car & Classic", "sold_date": date(2025, 1, 22)},
    # Cabriolet
    {"variant_name": "2002 Cabriolet (Baur)", "price_gbp": 35000, "year_of_car": 1973, "condition": "good", "source": "Bonhams", "sold_date": date(2025, 6, 15)},
]


def seed_database():
    """Populate the database with reference data and samples."""
    if ModelVariant.query.first():
        return  # already seeded

    # Insert model variants
    variant_map = {}
    for v in VARIANTS:
        variant = ModelVariant(**v)
        db.session.add(variant)
        db.session.flush()
        variant_map[variant.name] = variant.id

    # Insert registry cars
    for car_data in SAMPLE_REGISTRY:
        name = car_data.pop("variant_name")
        car_data["variant_id"] = variant_map[name]
        db.session.add(RegistryCar(**car_data))

    # Insert listings
    for listing_data in SAMPLE_LISTINGS:
        name = listing_data.pop("variant_name")
        listing_data["variant_id"] = variant_map[name]
        db.session.add(Listing(**listing_data))

    # Insert price records
    for price_data in SAMPLE_PRICE_RECORDS:
        name = price_data.pop("variant_name")
        price_data["variant_id"] = variant_map[name]
        db.session.add(PriceRecord(**price_data))

    db.session.commit()
