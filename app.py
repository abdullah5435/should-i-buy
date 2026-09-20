from pathlib import Path
import base64
import streamlit as st
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
import pandas as pd
import plotly.express as px


from analysis import (
    get_ai_advice,
    load_data,
    overall_score,
    spec_score,
    price_score,
    create_advisor_prompt
)

st.set_page_config(
    page_title="Should I Buy?",
    page_icon="📱",
    layout="wide"
)

image_path = Path(__file__).parent / "assets" / "slate_background.png"

with open(image_path, "rb") as f:
    bg_image = base64.b64encode(f.read()).decode()

st.markdown(f"""

<style>

header[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stToolbar"] {{
    background: transparent;
}}

.stApp {{
    background-color: #111417;
    background-image:
        linear-gradient(rgba(8, 10, 12, 0.45), rgba(8, 10, 12, 0.60)),
        url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}

h1, h2, h3 {{
    color: #f5f7fa;
}}

p, label {{
    color: #c2c8ce;
}}

.hero {{
    padding: 2.5rem 0 3rem 0;
    max-width: 720px;
}}

.hero-brand {{
    color: #63a9ff;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    margin-bottom: 1rem;
}}

.hero h1 {{
    font-size: 3.4rem;
    line-height: 1.05;
    font-weight: 750;
    margin: 0;
    color: #ffffff;
}}

.hero p {{
    font-size: 1.15rem;
    color: #b8c1ca;
    margin-top: 1rem;
}}

.section-label {{
    color: #5da9ff;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    margin-bottom: 0.35rem;
}}

.section-title {{
    color: #f5f7fa;
    font-size: 2rem;
    margin: 0;
}}

.section-subtitle {{
    color: #aeb7c1;
    font-size: 1rem;
    margin-top: 0.35rem;
    margin-bottom: 1.2rem;
}}

div[data-baseweb="select"] > div {{
    background: rgba(20, 24, 29, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px;
    min-height: 52px;
}}

div[data-baseweb="select"] > div:hover {{
    border-color: rgba(93, 169, 255, 0.55);
}}

div[data-baseweb="select"] * {{
    color: #f5f7fa !important;
}}

/* Priority slider cards */

div[data-testid="stSlider"] {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 20px 10px 20px;
    margin-bottom: 14px;
}}

.stButton > button {{
    border-radius: 12px;
    font-weight: 600;
    min-height: 48px;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-brand">📱 SHOULD I BUY?</div>
    <h1>Make smarter buying decisions.</h1>
    <p>Compare. Analyze. Choose the right smartphone for you.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Product data
# -----------------------------

products = load_data()

# -----------------------------
# Page
# -----------------------------

# -----------------------------
# Product selection
# -----------------------------

st.markdown("""
<div class="section-label">PHONE SELECTOR</div>
<h2 class="section-title">Choose your phone</h2>
<p class="section-subtitle">Select a phone to see whether it's worth buying.</p>
""", unsafe_allow_html=True)

product_name = st.selectbox(
    "Phone",
    products["model"],
    help="Choose the phone you want to evaluate."
)

# -----------------------------
# Importance
# -----------------------------

st.markdown("""
<div class="priority-heading">
    <div class="section-label">YOUR PRIORITIES</div>
    <h2>What matters most to you?</h2>
    <p>Adjust the balance to personalize your recommendation.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    price_weight = st.slider(
        "💰 Price",
        0, 100, 30
    )

with col2:
    performance_weight = st.slider(
        "⚡ Specifications",
        0, 100, 30
    )

with col3:
    quality_weight = st.slider(
        "⭐ Rating",
        0, 100, 40
    )

# Calculate total
total = price_weight + performance_weight + quality_weight

if total == 0:
    st.warning("Please give at least one factor some importance.")
else:

    # Normalize weights to 100%
    price_weight = price_weight / total
    performance_weight = performance_weight / total
    quality_weight = quality_weight / total

    st.caption(
        f"Your priorities: "
        f"Price {price_weight:.0%} · "
        f"Specifications {performance_weight:.0%} · "
        f"Rating {quality_weight:.0%}"
)
    

# -----------------------------
# Analysis
# -----------------------------

st.divider()

if st.button("🔍 Analyze This Phone", type="primary", use_container_width=True):
    st.session_state.analyzed = True

if st.session_state.analyzed:

    product = products[
        products["model"] == product_name
].iloc[0]

    # Calculate overall score
    score = overall_score(
        products,
        product,
        price_weight,
        performance_weight,
        quality_weight
    )

    # -----------------------------
    # Results
    # -----------------------------

    st.markdown("## 📊 Analysis")
        
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Price Score",
        f"{price_score(products, product['price']):.1f}/100"
    )

    col2.metric(
        "⭐ Rating",
        f"{product['rating']}/100"
    )

    col3.metric(
        "⚙️ Specs Score",
        f"{spec_score(product, products):.1f}/100"
    )

    st.metric(
        "🎯 Overall Score",
        f"{score:.1f}/100"
    )
        # -----------------------------
        # Recommendation
        # -----------------------------
    if  score >= 80:
            recommendation = "🟢 Strong Buy"
    elif score >= 65:
            recommendation = "🟡 Consider Buying"
    elif score >= 50:
            recommendation = "🟠 Think Twice"
    else:
            recommendation = "🔴 Not Recommended"

    st.markdown("### 🛒 Recommendation")

    if score >= 80:
        st.success(f"### {recommendation}")
    elif score >= 65:
        st.info(f"### {recommendation}")
    elif score >= 50:
        st.warning(f"### {recommendation}")
    else:
        st.error(f"### {recommendation}")
    st.markdown("### 💡 Why this recommendation?")

    median_price = products["price"].median()
    spec = spec_score(product, products)
    rating = product["rating"]

    price_percentile = (
        products["price"] <= product["price"]
    ).mean() * 100

    reasons = []

    if spec >= 80:
        reasons.append(
        f"⚙️ This phone has strong specifications, scoring {spec:.1f}/100."
    )
    elif spec < 60:
     reasons.append(
        f"⚙️ The specifications are relatively weak, scoring {spec:.1f}/100."
    )
    if rating >= 85:
        reasons.append(
            f"⭐ Its rating of {rating}/100 is excellent."
        )
    elif rating < 70:
        reasons.append(
            f"⭐ Its rating of {rating}/100 is below the stronger phones in the dataset."
        )

    if price_percentile <= 30:
        reasons.append(
            "💰 This phone is among the more affordable options in the dataset."
        )
    elif price_percentile >= 70:
        reasons.append(
        "💰 This phone is among the more expensive options in the dataset."
    )

    if price_weight >= performance_weight and price_weight >= quality_weight:
        reasons.append(
            "💰 Price is your top priority, so the phone's higher-than-median price "
            "has a strong impact on your recommendation."
        )
    elif performance_weight >= price_weight and performance_weight >= quality_weight:
        reasons.append(
            "⚡ Performance is your top priority, so the phone's specification "
            f"score of {spec:.1f}/100 is especially important."
        )
    else:
        reasons.append(
            "⭐ Quality is your top priority, and this phone's strong "
            f"{rating:.0f}/100 rating works in its favor."
        )
    if product["price"] > median_price:
        reasons.append(
            f"💰 At ₹{product['price']:,}, this phone is more expensive "
            f"than the market median of ₹{median_price:,.0f}."
        )
    else:
        reasons.append(
            f"💰 At ₹{product['price']:,}, this phone is cheaper "
            f"than the market median of ₹{median_price:,.0f}."
        )

    if rating >= 85:
        reasons.append(
            f"⭐ Its rating of {rating:.0f}/100 is strong."
        )
    elif rating >= 75:
        reasons.append(
            f"⭐ Its rating of {rating:.0f}/100 is respectable."
        )
    else:
        reasons.append(
            f"⭐ Its rating of {rating:.0f}/100 is relatively low."
        )

    if spec >= 70:
        reasons.append(
            f"⚙️ Its specification score of {spec:.1f}/100 is strong."
        )
    elif spec >= 50:
        reasons.append(
            f"⚙️ Its specification score of {spec:.1f}/100 is moderate."
        )
    else:
        reasons.append(
            f"⚙️ Its specification score of {spec:.1f}/100 is relatively low."
        )

    for reason in reasons:
        st.markdown(f"- {reason}")
    
    st.write(
        f"💰 This phone is more expensive than "
        f"{price_percentile:.0f}% of phones in the market."
    )

    st.markdown("### 🔄 Cheaper Alternatives")
    st.caption("Lower-priced phones that score well based on your priorities.")

    alternatives = products.copy()

    alternatives["score"] = alternatives.apply(
        lambda row: overall_score(
            products,
            row,
            price_weight,
            performance_weight,
            quality_weight
        ),
        axis=1
    )

    alternatives["value_score"] = (
        alternatives["score"] / alternatives["price"]
    ) * 10000

    alternatives = alternatives[
        (alternatives["model"] != product_name)
        & (alternatives["price"] < product["price"])
    ]

    alternatives = alternatives.sort_values(
        ["score", "value_score"],
        ascending=[False, False]
    ).head(5)

    if alternatives.empty:
        st.info("No cheaper alternatives were found for this phone.")

    else:
        best_value = alternatives.loc[
            alternatives["value_score"].idxmax()
        ]

        st.success(
            f"🏆 Best Value: {best_value['model']} — "
            f"₹{best_value['price']:,} with a Value Score of "
            f"{best_value['value_score']:.1f}"
        )

        st.dataframe(
            alternatives[
                ["model", "price", "rating", "score", "value_score"]
            ].rename(
                columns={
                    "model": "Phone",
                    "price": "Price (₹)",
                    "rating": "Rating",
                    "score": "Overall Score",
                    "value_score": "Value Score"
                }
            ),
            use_container_width=True,
                hide_index=True
        )

        st.markdown("### ⚖️ Compare Phones")

        comparison_phone = st.selectbox(
            "Compare the selected phone with:",
            alternatives["model"].tolist()
        )

        compare_product = products[
            products["model"] == comparison_phone
        ].iloc[0]

        col1, col2 = st.columns(2)

        selected_score = overall_score(
            products,
            product,
            price_weight,
            performance_weight,
            quality_weight
            )
        advisor_data = {
            "phone": product["model"],
            "price": product["price"],
            "rating": product["rating"],
            "ram": product["Ram Size(GB)"],
            "storage": product["Rom Size(GB)"],
            "battery": product["Battery Capacity"],
            "display_size": product["Display Size(inches)"],
            "refresh_rate": product["Display Refresh Rate"],
            "main_camera": product["Rear Camera 1"],
            "front_camera": product["Front Camera"],
            "specs_score": spec_score(product, products),
            
            "overall_score": selected_score,
            "price_priority": price_weight,
            "specs_priority": performance_weight,
            "rating_priority": quality_weight,
            "recommendation": recommendation
        }

        with col1:
            st.markdown(f"#### 📱 {product['model']}")
            st.metric("💰 Price", f"₹{product['price']:,}")
            st.metric("⭐ Rating", f"{product['rating']}/100")
            st.metric(
                "⚙️ Specs Score",
                f"{spec_score(product, products):.1f}/100"
            )
            st.metric("🎯 Overall Score", f"{ selected_score:.1f}/100")

        with col2:
            st.markdown(f"#### 📱 {compare_product['model']}")
            st.metric("💰 Price", f"₹{compare_product['price']:,}")
            st.metric("⭐ Rating", f"{compare_product['rating']}/100")

            compare_specs = spec_score(compare_product, products)

            st.metric(
                "⚙️ Specs Score",
                f"{compare_specs:.1f}/100"
            )

            compare_score = overall_score(
                products,
                compare_product,
                price_weight,
                performance_weight,
                quality_weight
            )

            st.metric(
                "🎯 Overall Score",
                f"{compare_score:.1f}/100"
            )

        price_difference = product["price"] - compare_product["price"]

        if price_difference > 0:
            st.info(
                f"💰 {compare_product['model']} is ₹{price_difference:,} cheaper."
            )
        elif price_difference < 0:
            st.info(
                f"💰 {compare_product['model']} is ₹{abs(price_difference):,} more expensive."
            )
        else:
            st.info("💰 Both phones have the same price.")

        st.markdown("### 🤖 AI Advisor")

        try:
            ai_advice = get_ai_advice(advisor_data)

            st.write(ai_advice)

        except Exception:
         st.error(
            "The AI Advisor is temporarily unavailable. "
            "Please try again in a moment."
    )


st.divider()

st.markdown("### 📊 Explore the Smartphone Market")
st.caption("Explore patterns and trends across the phones in the dataset.")

st.write("")

analysis_choice = st.selectbox(
    "What would you like to explore?",
    [
        "Price vs Rating",
        "What Makes a Phone Expensive?",
        "Best Value Phones",
        "Brand Analysis",
        "5G Price Premium",
        "Camera Capability",
        "Battery Analysis",
        "Storage Analysis"
    ]
)

# -----------------------------
# Price vs Rating
# -----------------------------

if analysis_choice == "Price vs Rating":

    st.markdown("### 📊 Price vs Rating")

    fig = px.scatter(
        products,
        x="price",
        y="rating",
        hover_name="model",
        trendline="ols",
        title="Do More Expensive Phones Get Better Ratings?"
    )

    fig.update_xaxes(type="log")

    st.plotly_chart(fig, use_container_width=True)

    correlation = products["price"].corr(products["rating"])

    st.metric(
        "📈 Price–Rating Correlation",
        f"{correlation:.2f}"
    )

    if correlation >= 0.7:
        st.write(
            "Strong positive relationship: higher-priced phones tend to have higher ratings."
        )
    elif correlation >= 0.4:
        st.write(
            "Moderate positive relationship: price and rating tend to increase together."
        )
    elif correlation >= 0.2:
        st.write(
            "Weak positive relationship: price has some relationship with rating."
        )
    elif correlation <= -0.2:
        st.write(
            "Negative relationship: higher-priced phones tend to have lower ratings."
        )
    else:
        st.write(
            "Little relationship: price does not strongly predict rating."
        )


# -----------------------------
# Best Value Phones
# -----------------------------

if analysis_choice == "Best Value Phones":

    st.markdown("#### 💰 Best Value Phones")

    value_data = products.copy()

    value_data["Value Score"] = (
        value_data["rating"] / value_data["price"]
    ) * 100000

    top_value = (
        value_data
        .sort_values("Value Score", ascending=False)
        .head(10)
    )

    fig_value = px.bar(
        top_value.sort_values("Value Score"),
        x="Value Score",
        y="model",
        orientation="h",
        title="Top 10 Phones by Rating per ₹100,000"
    )

    st.plotly_chart(
        fig_value,
        use_container_width=True
    )


# -----------------------------
# Brand Analysis
# -----------------------------

if analysis_choice == "Brand Analysis":

    st.markdown("#### 🏷️ Brand Analysis")

    products["brand"] = (
        products["model"]
        .str.split()
        .str[0]
        .str.strip()
    )

    brand_map = {
        "POCO": "Poco",
        "OPPO": "Oppo",
        "IPhone": "Apple",
        "iPhone": "Apple"
    }

    products["brand"] = products["brand"].replace(brand_map)

    brand_data = (
        products
        .groupby("brand")
        .agg(
            Average_Price=("price", "mean"),
            Average_Rating=("rating", "mean"),
            Phone_Count=("model", "count")
        )
        .sort_values("Average_Rating", ascending=False)
        .reset_index()
    )

    brand_data = brand_data[
        brand_data["Phone_Count"] >= 10
    ]

    fig_brand = px.bar(
        brand_data,
        x="brand",
        y="Average_Rating",
        hover_data=["Average_Price", "Phone_Count"],
        title="Average Rating by Brand"
    )

    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )

    st.markdown("#### 💰 Average Price by Brand")

    fig_brand_price = px.bar(
        brand_data,
        x="brand",
        y="Average_Price",
        hover_data=["Average_Rating", "Phone_Count"],
        title="Average Price by Brand"
    )

    st.plotly_chart(
        fig_brand_price,
        use_container_width=True
    )

    st.markdown("#### 🏆 Best Value Brands")

    brand_value = brand_data.copy()

    brand_value["Value_Score"] = (
        brand_value["Average_Rating"]
        / brand_value["Average_Price"]
    ) * 100000

    brand_value = (
        brand_value
        .sort_values("Value_Score", ascending=False)
        .head(10)
    )

    fig_brand_value = px.bar(
        brand_value,
        x="brand",
        y="Value_Score",
        hover_data=[
            "Average_Price",
            "Average_Rating",
            "Phone_Count"
        ],
        title="Best Value Brands"
    )

    st.plotly_chart(
        fig_brand_value,
        use_container_width=True
    )


# -----------------------------
# 5G Price Premium
# -----------------------------

if analysis_choice == "5G Price Premium":

    st.markdown("### 📊 5G Price Premium")

    if "5G" in products.columns:

        network_data = (
            products
            .groupby("5G")["price"]
            .mean()
            .reset_index()
        )

        network_data["5G"] = network_data["5G"].map({
            0: "Non-5G",
            1: "5G"
        })

        fig_5g = px.bar(
            network_data,
            x="5G",
            y="price",
            title="Average Price: 5G vs Non-5G Phones",
            labels={
                "5G": "5G Support",
                "price": "Average Price (₹)"
            }
        )

        st.plotly_chart(
            fig_5g,
            use_container_width=True
        )

        non_5g_price = network_data.loc[
            network_data["5G"] == "Non-5G", "price"
        ].iloc[0]

        five_g_price = network_data.loc[
            network_data["5G"] == "5G", "price"
        ].iloc[0]

        premium = (
            (five_g_price - non_5g_price)
            / non_5g_price
        ) * 100

        st.write(
            f"💡 On average, 5G phones cost "
            f"{premium:.1f}% more than non-5G phones in this dataset."
        )

        # -----------------------------
# What Makes a Phone Expensive?
# -----------------------------

if analysis_choice == "What Makes a Phone Expensive?":

    st.markdown("### 💰 What Makes a Phone Expensive?")

    numeric_columns = products.select_dtypes(
        include="number"
    ).columns

    correlations = (
        products[numeric_columns]
        .corr()["price"]
        .drop("price")
        .sort_values(ascending=False)
    )

    correlation_data = (
        correlations
        .head(10)
        .reset_index()
    )

    correlation_data.columns = [
        "Feature",
        "Correlation"
    ]

    fig_expensive = px.bar(
        correlation_data,
        x="Correlation",
        y="Feature",
        orientation="h",
        title="Features Most Closely Related to Phone Price"
    )

    st.plotly_chart(
        fig_expensive,
        use_container_width=True
    )

    st.write(
        "💡 A higher correlation means that the feature tends "
        "to increase as phone price increases. Correlation does "
        "not necessarily mean the feature causes the higher price."
    )

    # -----------------------------
# Camera Capability
# -----------------------------

if analysis_choice == "Camera Capability":

    st.markdown("### 📸 Camera Capability")

    camera_columns = [
        "Rear Camera 1",
        "Rear Camera 2",
        "Rear Camera 3",
        "Front Camera"
    ]

    camera_data = products.copy()

    camera_data["Camera Score"] = (
    camera_data["Rear Camera 1"].fillna(0) * 1.0
    + camera_data["Rear Camera 2"].fillna(0) * 0.5
    + camera_data["Rear Camera 3"].fillna(0) * 0.5
    + camera_data["Front Camera"].fillna(0) * 0.5
    )

    top_camera = (
        camera_data
        .sort_values("Camera Score", ascending=False)
        .head(10)
    )

    fig_camera = px.bar(
        top_camera.sort_values("Camera Score"),
        x="Camera Score",
        y="model",
        orientation="h",
        title="Top Phones by Camera Hardware"
    )

    st.plotly_chart(
        fig_camera,
        use_container_width=True
    )

    st.write(
        "💡 Camera Score is based on the combined camera "
        "specifications available in the dataset."
    )

if analysis_choice == "Storage Analysis":
    st.markdown("### 💾 Storage Analysis")

    storage_data = products.copy()

    storage_data["Storage Tier"] = pd.cut(
        storage_data["Rom Size(GB)"],
        bins=[0, 64, 128, 256, 512, float("inf")],
        labels=["≤64 GB", "128 GB", "256 GB", "512 GB", "1 TB+"]
    )

    storage_summary = (
        storage_data.groupby("Storage Tier", observed=False)
        .agg(
            Average_Rating=("rating", "mean"),
            Phone_Count=("model", "count")
        )
        .reset_index()
    )

    fig_storage = px.bar(
        storage_summary,
        x="Storage Tier",
        y="Average_Rating",
        text="Average_Rating",
        hover_data=["Phone_Count"],
        title="Average Rating by Storage Tier",
        labels={
            "Storage Tier": "Storage",
            "Average_Rating": "Average Rating"
        }
    )

    fig_storage.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    st.plotly_chart(fig_storage, use_container_width=True)

    st.write(
        "💡 This shows how phone ratings vary across different storage capacities."
    )

if analysis_choice == "Battery Analysis":
    st.markdown("### 🔋 Battery Analysis")

    battery_data = products.copy()

    battery_data["Battery Tier"] = pd.cut(
            battery_data["Battery Capacity"],
            bins=[0, 4000, 5000, 6000, float("inf")],
            labels=["≤4000 mAh", "4001–5000 mAh", "5001–6000 mAh", "6000+ mAh"]
        )

    battery_summary = (
            battery_data.groupby("Battery Tier", observed=False)
            .agg(
                Average_Rating=("rating", "mean"),
                Phone_Count=("model", "count")
            )
            .reset_index()
        )

    fig_battery = px.bar(
            battery_summary,
            x="Battery Tier",
            y="Average_Rating",
            text="Average_Rating",
            hover_data=["Phone_Count"],
            title="Average Rating by Battery Capacity",
            labels={
                "Battery Tier": "Battery Capacity",
                "Average_Rating": "Average Rating"
            }
        )

    fig_battery.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

    st.plotly_chart(fig_battery, use_container_width=True)

    st.write(
            "💡 This shows how phone ratings vary across different battery capacities."
        )