import http.client
import urllib.parse
import json

# API Key and Host
API_KEY = "3da3461db0mshd2376caab573a7ep14e0a7jsnd5a43d1668c5"
API_HOST = "booking-com15.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def schedule_rental(pick_up_lat, pick_up_lon, drop_off_lat, drop_off_lon,
                    pick_up_date, drop_off_date, pick_up_time, drop_off_time,
                    json_filename="rental_info.json"):
    """Schedule a rental by picking the top result from the car rental search and save details to JSON."""
    params = {
        "pick_up_latitude": pick_up_lat,
        "pick_up_longitude": pick_up_lon,
        "drop_off_latitude": drop_off_lat,
        "drop_off_longitude": drop_off_lon,
        "pick_up_date": pick_up_date,
        "drop_off_date": drop_off_date,
        "pick_up_time": pick_up_time,
        "drop_off_time": drop_off_time,
        "currency_code": "EGP",
        "location": "Egypt"
    }

    query = urllib.parse.urlencode(params)

    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("GET", f"/api/v1/cars/searchCarRentals?{query}", headers=HEADERS)

    res = conn.getresponse()
    data = res.read()
    conn.close()

    parsed = json.loads(data.decode("utf-8"))
    results = parsed.get("data", {}).get("search_results", [])

    if not results:
        print("🚫 No available rentals found.")
        return None

    top_rental = results[0]

    # Extract vehicle info
    vehicle = top_rental.get("vehicle_info", {})
    car_name = vehicle.get("v_name", "N/A")
    car_category = vehicle.get("group_or_similar", "N/A")
    car_image = vehicle.get("image_url", "")

    # Extract pricing
    pricing = top_rental.get("pricing_info", {})
    price = pricing.get("price", "N/A")
    currency = pricing.get("currency", "N/A")

    # Manual conversion from INR to EGP (approximate rate)
    INR_TO_EGP = 0.42
    if currency != "EGP" and price != "N/A":
        try:
            price_egp = float(price) * INR_TO_EGP
            price_ng = price_egp / 20
            if price_ng > 500:
                price_ng = price_ng / 2
            price = f"{price_ng:.2f}"
            currency = "EGP"
        except Exception:
            pass

    # Extract supplier info
    supplier_info = top_rental.get("supplier_info", {})
    supplier = supplier_info.get("name", "Unknown")

    # Extract rating info correctly from rating_info key
    rating_info = top_rental.get("rating_info", {})
    rating_value = rating_info.get("average", "N/A")
    rating_title = rating_info.get("average_text", "N/A")
    rating_subtitle = f"{rating_info.get('no_of_ratings', 'N/A')} reviews"

    # Extract location details
    pick_info = top_rental.get("route_info", {}).get("pickup", {})
    drop_info = top_rental.get("route_info", {}).get("dropoff", {})
    pick_place = pick_info.get("name", "Unknown")
    drop_place = drop_info.get("name", "Unknown")

    # Display result
    print("✅ Rental Car Found")
    print(f"🚗 Car: {car_name} ({car_category})")
    print(f"🖼️ Image: {car_image}")
    print(f"💵 Price: {price} {currency}")
    print(f"🏢 Supplier: {supplier}")
    print(f"⭐ Rating: {rating_value} ({rating_title}) — {rating_subtitle}")
    print(f"📍 Pick-up: {pick_place} at {pick_up_date} {pick_up_time}")
    print(f"📍 Drop-off: {drop_place} at {drop_off_date} {drop_off_time}")

    # Prepare data dictionary to save
    rental_data = {
        "car": {
            "name": car_name,
            "category": car_category,
            "image": car_image
        },
        "price": {
            "amount": price,
            "currency": currency
        },
        "supplier": supplier,
        "rating": {
            "value": rating_value,
            "title": rating_title,
            "reviews": rating_subtitle
        },
        "pickup": {
            "location": pick_place,
            "date": pick_up_date,
            "time": pick_up_time
        },
        "dropoff": {
            "location": drop_place,
            "date": drop_off_date,
            "time": drop_off_time
        }
    }

    # Save to JSON file
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(rental_data, f, indent=4)

    print(f"✅ Rental info saved to {json_filename}")

    return top_rental
