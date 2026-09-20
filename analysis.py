import pandas as pd
import numpy as np
import streamlit as st
from google import genai

def load_data():
    df = pd.read_csv("data/smartphones.csv")
    return df
def price_score(df, price):
    min_price = df["price"].min()
    max_price = df["price"].max()

    log_min = np.log1p(min_price)
    log_max = np.log1p(max_price)
    log_price = np.log1p(price)

    if log_max == log_min:
        return 100

    score = (1 - (log_price - log_min) / (log_max - log_min)) * 100

    return max(0, min(score, 100))
def rating_score(rating):
    return rating
def spec_score(phone, df):
    scores = []
    weights = []

        # RAM
    ram = phone["Ram Size(GB)"]

    if ram > 0:
        if ram <= 4:
            ram_score = 40
        elif ram <= 6:
            ram_score = 55
        elif ram <= 8:
            ram_score = 70
        elif ram <= 12:
            ram_score = 85
        elif ram <= 16:
            ram_score = 95
        else:
            ram_score = 100

        scores.append(ram_score)
        weights.append(2)

        # Storage
    storage = phone["Rom Size(GB)"]

    if storage > 0:
        if storage <= 64:
            storage_score = 40
        elif storage <= 128:
            storage_score = 65
        elif storage <= 256:
            storage_score = 85
        elif storage <= 512:
            storage_score = 95
        else:
            storage_score = 100

        scores.append(storage_score)
        weights.append(2)

        # Battery
    battery = phone["Battery Capacity"]

    if battery > 0:
        if battery <= 4000:
            battery_score = 55
        elif battery <= 5000:
            battery_score = 75
        elif battery <= 6000:
            battery_score = 90
        else:
            battery_score = 100

        scores.append(battery_score)
        weights.append(2)

        # Display refresh rate
    refresh_rate = phone["Display Refresh Rate"]

    if refresh_rate > 0:
        if refresh_rate <= 60:
            refresh_score = 45
        elif refresh_rate <= 90:
            refresh_score = 65
        elif refresh_rate <= 120:
            refresh_score = 85
        elif refresh_rate <= 144:
            refresh_score = 92
        elif refresh_rate <= 165:
            refresh_score = 96
        else:
            refresh_score = 100

        scores.append(refresh_score)
        weights.append(1)

        # Camera
    camera_score = 0

    main_camera = phone["Rear Camera 1"]
    secondary_camera = phone["Rear Camera 2"]
    third_camera = phone["Rear Camera 3"]

    main_score = np.interp(
        main_camera,
        [0, 12, 50, 64, 108, 200],
        [0, 60, 85, 90, 95, 100]
    )

    secondary_score = np.interp(
        secondary_camera,
        [0, 2, 8, 12, 50],
        [0, 40, 65, 75, 90]
    )

    third_score = np.interp(
        third_camera,
        [0, 2, 5, 8, 32],
        [0, 40, 50, 65, 85]
    )

    camera_score = (
        main_score * 0.60
        + secondary_score * 0.25
        + third_score * 0.15
    )

    if camera_score > 0:
        scores.append(camera_score)
        weights.append(2)

    return sum(score * weight for score, weight in zip(scores, weights)) / sum(weights)

def overall_score(df, phone, price_weight, rating_weight, spec_weight):
    price = price_score(df, phone["price"])
    rating = rating_score(phone["rating"])
    specs = spec_score(phone, df)

    total = price_weight + rating_weight + spec_weight

    if total == 0:
        return 0

    price_weight = price_weight / total
    rating_weight = rating_weight / total
    spec_weight = spec_weight / total

    score = (
        price * price_weight
        + rating * rating_weight
        + specs * spec_weight
    )

    return score

def create_advisor_prompt(advisor_data):
    return f"""
    You are a smartphone buying advisor.

    Analyze this phone based only on the provided data.

    Phone: {advisor_data["phone"]}
    Price: ₹{advisor_data["price"]}
    Rating: {advisor_data["rating"]}/100
    RAM: {advisor_data["ram"]} GB
    Storage: {advisor_data["storage"]} GB
    Battery: {advisor_data["battery"]} mAh
    Display Size: {advisor_data["display_size"]} inches
    Refresh Rate: {advisor_data["refresh_rate"]} Hz
    Main Camera: {advisor_data["main_camera"]} MP
    Front Camera: {advisor_data["front_camera"]} MP
    Specs Score: {advisor_data["specs_score"]:.1f}/100
    Overall Score: {advisor_data["overall_score"]:.1f}/100

    User priorities:
    Price: {advisor_data["price_priority"]:.0%}
    Specifications: {advisor_data["specs_priority"]:.0%}
    Rating: {advisor_data["rating_priority"]:.0%}

    Current recommendation: {advisor_data["recommendation"]}

    Explain:
    1. Why the phone received this recommendation.
    2. Its main strengths.
    3. Its main weaknesses.
    4. What type of buyer it may suit.

    Format your response exactly like this:

WHY:
Give a short explanation of the recommendation in 2-3 sentences.

STRENGTHS:
- Mention 2-4 specific strengths based on the provided specifications and scores.

WEAKNESSES:
- Mention 2-3 specific weaknesses based on the provided specifications, price, and scores.

BEST FOR:
Give one short sentence describing the type of buyer this phone may suit.

Do not repeat the full specification list.
Do not invent specifications or facts that are not provided.
Keep the response concise and useful for someone deciding whether to buy the phone.
    """
def get_ai_advice(advisor_data):
    try:
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        prompt = create_advisor_prompt(advisor_data)

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Advisor error: {type(e).__name__}"