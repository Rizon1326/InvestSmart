from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class MarketDataScraper:
    def __init__(self):
        self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver with Chrome options"""
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    def scrape_foodpanda(self, location, business_interest):
        """Scrape Foodpanda data for restaurant/food business analysis"""
        try:
            # Example URL structure for Foodpanda Bangladesh
            base_url = "https://www.foodpanda.com.bd"
            search_url = f"{base_url}/restaurants/new?latitude=23.8103&longitude=90.4125"  # Dhaka coordinates
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Extract restaurant data (mock implementation - actual selectors may vary)
            restaurants = soup.find_all('div', class_='vendor-item')[:5]  # Get top 5
            
            for i, restaurant in enumerate(restaurants):
                try:
                    name = restaurant.find('h3', class_='name')
                    name = name.text.strip() if name else f"Restaurant {i+1}"
                    
                    # Mock price extraction (actual implementation would vary)
                    price = 200 + (i * 50)  # Mock pricing
                    
                    products.append({
                        "name": name,
                        "price": price,
                        "demand_score": 8.5 - (i * 0.3),
                        "competition_level": "medium" if i < 3 else "high",
                        "seasonal_trend": "stable",
                        "category": "food"
                    })
                except Exception as e:
                    logging.warning(f"Error parsing restaurant {i}: {e}")
                    continue
            
            return {
                "source": "foodpanda",
                "location": location,
                "business_type": business_interest,
                "products": products,
                "market_size": "large",
                "avg_price_range": [150.0, 400.0],
                "competition_density": "high",
                "market_growth": "stable"
            }
            
        except Exception as e:
            logging.error(f"Foodpanda scraping error: {e}")
            return self.get_mock_food_data(location, business_interest)
    
    def scrape_daraz(self, location, business_interest):
        """Scrape Daraz data for e-commerce/retail business analysis"""
        try:
            base_url = "https://www.daraz.com.bd"
            
            # Map business interest to Daraz categories
            category_mapping = {
                "retail": "fashion",
                "electronics": "electronics",
                "food": "groceries",
                "beauty": "health-beauty"
            }
            
            category = category_mapping.get(business_interest.lower(), "fashion")
            search_url = f"{base_url}/catalog/?q={category}&_keyori=ss&from=input&spm=a2a0e.tm80335161.search.go.735e7c00Q8dJsD"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Extract product data (mock implementation)
            product_items = soup.find_all('div', class_='gridItem--Yd0sa')[:5]
            
            for i, item in enumerate(product_items):
                try:
                    name_elem = item.find('div', class_='title--wFj93')
                    name = name_elem.text.strip() if name_elem else f"Product {i+1}"
                    
                    price_elem = item.find('span', class_='currency--GVKjl')
                    price = 500 + (i * 100)  # Mock pricing
                    
                    products.append({
                        "name": name,
                        "price": price,
                        "demand_score": 7.8 - (i * 0.2),
                        "competition_level": "high" if i < 2 else "medium",
                        "seasonal_trend": "growing",
                        "category": category
                    })
                except Exception as e:
                    logging.warning(f"Error parsing product {i}: {e}")
                    continue
            
            return {
                "source": "daraz",
                "location": location,
                "business_type": business_interest,
                "products": products,
                "market_size": "large",
                "avg_price_range": [300.0, 1000.0],
                "competition_density": "very_high",
                "market_growth": "growing"
            }
            
        except Exception as e:
            logging.error(f"Daraz scraping error: {e}")
            return self.get_mock_retail_data(location, business_interest)
    
    def get_mock_food_data(self, location, business_interest):
        """Return mock food/restaurant data"""
        return {
            "source": "mock_foodpanda",
            "location": location,
            "business_type": business_interest,
            "products": [
                {"name": "Biriyani", "price": 250, "demand_score": 9.2, "competition_level": "high", "seasonal_trend": "stable"},
                {"name": "Burger", "price": 180, "demand_score": 8.1, "competition_level": "medium", "seasonal_trend": "growing"},
                {"name": "Pizza", "price": 350, "demand_score": 7.8, "competition_level": "high", "seasonal_trend": "stable"},
                {"name": "Chinese Food", "price": 220, "demand_score": 7.5, "competition_level": "medium", "seasonal_trend": "stable"},
                {"name": "Local Snacks", "price": 120, "demand_score": 8.5, "competition_level": "low", "seasonal_trend": "seasonal"}
            ],
            "market_size": "large",
            "avg_price_range": [120.0, 350.0],
            "competition_density": "high",
            "market_growth": "stable"
        }
    
    def get_mock_retail_data(self, location, business_interest):
        """Return mock retail/e-commerce data"""
        return {
            "source": "mock_daraz",
            "location": location,
            "business_type": business_interest,
            "products": [
                {"name": "Fashion Items", "price": 800, "demand_score": 8.5, "competition_level": "very_high", "seasonal_trend": "seasonal"},
                {"name": "Electronics", "price": 1200, "demand_score": 7.9, "competition_level": "high", "seasonal_trend": "stable"},
                {"name": "Home & Living", "price": 600, "demand_score": 7.2, "competition_level": "medium", "seasonal_trend": "growing"},
                {"name": "Beauty Products", "price": 400, "demand_score": 8.1, "competition_level": "high", "seasonal_trend": "growing"},
                {"name": "Sports & Outdoor", "price": 900, "demand_score": 6.8, "competition_level": "medium", "seasonal_trend": "seasonal"}
            ],
            "market_size": "very_large",
            "avg_price_range": [400.0, 1200.0],
            "competition_density": "very_high",
            "market_growth": "growing"
        }

scraper = MarketDataScraper()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "market-data-scraper"})

@app.route('/scrape', methods=['POST'])
def scrape_market_data():
    try:
        data = request.json
        location = data.get('location', 'Dhaka')
        business_interest = data.get('businessInterest', 'food')
        selling_channel = data.get('sellingChannel', 'online')
        
        logging.info(f"Scraping request: {location}, {business_interest}, {selling_channel}")
        
        # Determine which platform to scrape based on business interest
        if business_interest.lower() in ['food', 'restaurant']:
            result = scraper.scrape_foodpanda(location, business_interest)
        else:
            result = scraper.scrape_daraz(location, business_interest)
        
        # Add channel-specific data
        result['selling_channel'] = selling_channel
        result['scraped_at'] = time.time()
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Scraping service error: {e}")
        return jsonify({
            "error": "Scraping failed",
            "message": str(e),
            "mock_data": scraper.get_mock_food_data("Dhaka", "food")
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)