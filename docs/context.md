Here’s your full project context formatted as a **Markdown file**:

````markdown
# 📊 Business Analysis Platform – Project Context

## 🏗 Tech Stack
- **Backend:** Java + Spring Boot  
- **Frontend:** React (TypeScript)  
- **Database:** PostgreSQL (or MongoDB if flexible schema required)  
- **Scraping & ML Layer:** Python microservice  
  - Libraries: `Requests`, `BeautifulSoup`, `Selenium`, `Prophet`, `SARIMAX`, `XGBoost`, `LightGBM`  
- **AI Layer:** Groq API (`llama-3.1-8b-instant`)  

---

## 🔹 Step 1 – User Input (Backend Form Handling)
Collected via **React form → Spring Boot API → stored in DB**.  

**Inputs:**
- Location (district, BD – 64 districts)  
- Business interest (food, retail, agri, e-commerce, services)  
- Capital range (min–max)  
- Risk profile (conservative / balanced / aggressive)  
- Target income (monthly / yearly)  
- Work type (full-time / part-time)  
- Selling channel (online / offline)  
- Seasonal preference (e.g., Ramadan, Eid, winter)  
- Delivery capability (own / third-party)  

---

## 🔹 Step 2 – Scraping (Backend → Python Service)
Backend triggers a **Python scraping service** (Foodpanda, Daraz, etc.).

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.foodpanda.com.bd/restaurant/ivil/magix-bear"
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

items = soup.find_all("div", class_="menu-item")
for item in items:
    name = item.find("h3").text.strip()
    price = item.find("span", class_="price").text.strip()
    print(name, price)
````

---

## 🔹 Step 3 – AI/ML Analysis (Backend → Groq API + Models)

### 🔗 Groq API (Llama-3.1-8b-instant)

The scraped dataset is sent to **Groq API** for textual + formula-based analysis.

```python
import requests

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": "Bearer <YOUR_API_KEY>"}

payload = {
  "model": "llama-3.1-8b-instant",
  "messages": [
    {"role": "system", "content": "You are a business analyst."},
    {"role": "user", "content": "Analyze product demand, pricing margin, and feasibility from this dataset ..."}
  ]
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

---

### 📈 Forecasting

* **Prophet / SARIMAX** → seasonality forecast
* **XGBoost / LightGBM** → demand & price prediction

---

### 📊 Product Fit Scoring

```python
fit_score = demand_score * margin_score * feasibility_score
```

---

### 💰 Pricing Formula

```python
suggested_price = procurement_cost + margin - competition_adjustment
```

---

### 📦 Supply Chain & Cost Estimation

* Logistics cost
* Inventory holding cost
* Supplier availability index

---

### 💵 Finance & Simulation

```python
Revenue = Price × Quantity
Net Profit = Revenue – (Fixed + Variable + Logistics + Marketing)
```

**Scenarios:**

* **Deterministic:** best / expected / worst
* **Monte Carlo (1k runs):** ROI probability distribution

---

## 🔹 Step 4 – Frontend (Visualization & Presentation)

Frontend (**React + TypeScript**) consumes backend API results and displays insights.

**UI Elements:**

* **Charts:** ROI curve, sales forecast, break-even chart
* **KPI Cards:** Net profit, gross margin, ROI, payback period
* **Recommendation Cards:** 3–5 best product/business ideas

---

## 📌 End-to-End Workflow

1. User fills onboarding form (criteria inputs)
2. Backend saves inputs → triggers scraping
3. Scraped data → passed to Groq API (`llama-3.1-8b-instant`) + ML models
4. Analysis runs (forecasting, fit scoring, simulation)
5. Backend generates recommendations + financial metrics
6. Frontend visualizes results (charts, KPIs, recommendations)

---

✅ Now your context is **linear** (backend → analysis → frontend), includes **Groq API at the right step**, and keeps all **formulas + modules intact**.

```


```
