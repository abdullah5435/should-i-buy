# 📱 Should I Buy?

**Should I Buy?** is a data-driven smartphone buying advisor that helps users evaluate phones based on price, specifications, quality, and personal priorities.

Instead of simply listing phone specifications, the app analyzes the data and turns it into a practical buying recommendation.

## 🚀 Features

- 📊 **Data-driven phone scoring**
  - Evaluates price, specifications, and quality
  - Personalizes the score using user priorities

- 🎯 **Personalized recommendations**
  - Strong Buy
  - Consider Buying
  - Think Twice
  - Not Recommended

- 💰 **Price & value analysis**
  - Understand how phone prices relate to specifications
  - Find cheaper alternatives with similar or better scores

- 📈 **Market analysis**
  - Price vs. rating
  - What makes a phone expensive?
  - Brand analysis
  - 5G price premium
  - Camera capability
  - Battery analysis
  - Storage analysis
  - Best-value phones

- ⚖️ **Phone comparison**
  - Compare smartphones using the same scoring framework

- 🤖 **AI Advisor**
  - Explains why a phone received its score
  - Highlights strengths and weaknesses
  - Describes who the phone may be suitable for

- 📱 **Real smartphone data**
  - Includes phones from major brands
  - Dataset is continuously updated as new models are added

## 🧠 How It Works

The app combines smartphone specifications with a weighted scoring system.

Users can adjust how much they care about:

- 💰 Price
- ⚡ Performance
- ⭐ Quality

The application then calculates an overall score based on the selected phone's data.

The scoring system also considers factors such as:

- RAM
- Storage
- Battery capacity
- Display refresh rate
- Camera hardware
- Phone rating
- Price

The goal is not simply to find the phone with the highest specifications. It is to help users understand whether a phone makes sense **for their priorities and budget**.

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly**
- **Statsmodels**
- **Google Gemini API**
- **OpenPyXL**

## 📂 Project Structure

```text
should-i-buy/
│
├── app.py                 # Streamlit application
├── analysis.py            # Scoring, analysis, and AI advisor logic
├── requirements.txt       # Python dependencies
├── data/
│   └── smartphones.csv    # Smartphone dataset
├── assets/
│   └── ...                # UI assets
└── README.md
```

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/abdullah5435/should-i-buy.git
cd should-i-buy
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```
### 5. Start the app

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 📊 Dataset

The application uses a structured smartphone dataset containing specifications such as:

- Brand and model
- Operating system
- Processor
- RAM
- Storage
- Battery
- Display
- Refresh rate
- Camera specifications
- Connectivity
- Price
- Rating

The dataset is maintained in:

```text
data/smartphones.csv
```

New smartphone models can be added while maintaining the existing column structure.

## 🌐 Deployment

The application is designed for deployment using **Streamlit Community Cloud**.

The GitHub repository is:

**https://github.com/abdullah5435/should-i-buy**

## 🗺️ Future Improvements

Planned improvements include:

- 🔎 Faster phone search and filtering
- 📱 Larger and more frequently updated smartphone database
- ⚖️ More advanced phone comparison
- 🤖 More conversational AI recommendations
- 💸 Better value-for-money analysis
- 📊 Additional market insights
- 📱 Improved mobile experience
- ✨ Final UI and branding polish

## 🎯 Project Goal

The long-term goal of **Should I Buy?** is to make smartphone buying decisions easier by combining:

**Real data + personalized priorities + transparent analysis + AI explanations**

rather than relying only on generic reviews or specification lists.

---

### Built with Python, Streamlit, data analysis, and Gemini AI.
