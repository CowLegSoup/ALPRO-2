import random
import time
from datetime import datetime, timedelta

begin = time.time()

class VacationPlanner:
    def __init__(self, budget=10000000, start_date=None):
        self.total_budget = budget
        self.remaining_budget = budget
        self.start_date = start_date if start_date else datetime.now()
        
        # Define destinations with detailed information
        self.destinations = {
            "Makassar": {
                "hotel_cost": 350000,  # per night
                "food_cost": {"breakfast": 25000, "lunch": 40000, "dinner": 60000},
                "snack_cost": 20000,  # per day
                "souvenirs": {"Miniatur Toraja": 50000, "Sarung Sutra": 150000, "Markisa": 45000},
                "local_transport": 100000,  # per day
                # New weather information by month (1=January, etc)
                "weather": {
                    1: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-30°C"},
                    2: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-30°C"},
                    3: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-31°C"},
                    4: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-32°C"},
                    5: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-33°C"},
                    6: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-33°C"},
                    7: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-32°C"},
                    8: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-32°C"},
                    9: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-33°C"},
                    10: {"condition": "Dry", "risk_level": "Medium", "temp_range": "24-33°C"},
                    11: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-32°C"},
                    12: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-31°C"}
                },
                # Major festivals and events
                "events": {
                    1: ["Tahun Baru"],
                    3: ["Festival Pagelaran Budaya"],
                    6: ["Festival Pesona Losari"],
                    8: ["Kemerdekaan RI"],
                    12: ["Festival Kuliner Makassar"]
                },
                # Risk factors specific to this destination
                "risks": ["Traffic congestion", "Street flooding during rainy season"]
            },
            "Manado": {
                "hotel_cost": 400000,  # per night
                "food_cost": {"breakfast": 30000, "lunch": 45000, "dinner": 70000},
                "snack_cost": 25000,  # per day
                "souvenirs": {"Kain Bentenan": 120000, "Gorengan Pisang": 35000, "Kacang Goyang": 40000},
                "local_transport": 120000,  # per day
                "weather": {
                    1: {"condition": "Rainy", "risk_level": "High", "temp_range": "23-30°C"},
                    2: {"condition": "Rainy", "risk_level": "High", "temp_range": "23-30°C"},
                    3: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-30°C"},
                    4: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "23-31°C"},
                    5: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-31°C"},
                    6: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-31°C"},
                    7: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-31°C"},
                    8: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-31°C"},
                    9: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "23-31°C"},
                    10: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-31°C"},
                    11: {"condition": "Rainy", "risk_level": "High", "temp_range": "23-30°C"},
                    12: {"condition": "Rainy", "risk_level": "High", "temp_range": "23-30°C"}
                },
                "events": {
                    4: ["Festival Bunga Kota Tomohon"],
                    7: ["Festival Bunaken"],
                    9: ["Cap Go Meh"],
                    12: ["Christmas Festival"]
                },
                "risks": ["Volcanic activity from Mount Lokon", "Marine conditions affecting boat tours"]
            },
            "Palu": {
                "hotel_cost": 300000,  # per night
                "food_cost": {"breakfast": 20000, "lunch": 35000, "dinner": 50000},
                "snack_cost": 15000,  # per day
                "souvenirs": {"Sarung Bomba": 100000, "Kerajinan Kayu": 85000, "Kacang Mete": 50000},
                "local_transport": 80000,  # per day
                "weather": {
                    1: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-33°C"},
                    2: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-33°C"},
                    3: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "23-33°C"},
                    4: {"condition": "Mixed", "risk_level": "Low", "temp_range": "24-34°C"},
                    5: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-34°C"},
                    6: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-34°C"},
                    7: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-34°C"},
                    8: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-34°C"},
                    9: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-34°C"},
                    10: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-34°C"},
                    11: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-33°C"},
                    12: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "23-33°C"}
                },
                "events": {
                    5: ["Festival Teluk Palu"],
                    8: ["Festival Budaya Kaili"],
                    10: ["Palu Nomoni"]
                },
                "risks": ["Earthquake risk", "Road conditions in remote areas", "Reconstruction activities"]
            },
            "Kendari": {
                "hotel_cost": 280000,  # per night
                "food_cost": {"breakfast": 20000, "lunch": 35000, "dinner": 45000},
                "snack_cost": 18000,  # per day
                "souvenirs": {"Olahan Jambu Mete": 60000, "Kalosara": 120000, "Kain Tenun": 85000},
                "local_transport": 90000,  # per day
                "weather": {
                    1: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-31°C"},
                    2: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-31°C"},
                    3: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-32°C"},
                    4: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-32°C"},
                    5: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-32°C"},
                    6: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-32°C"},
                    7: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-32°C"},
                    8: {"condition": "Dry", "risk_level": "Low", "temp_range": "23-32°C"},
                    9: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-32°C"},
                    10: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-32°C"},
                    11: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-31°C"},
                    12: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-31°C"}
                },
                "events": {
                    4: ["Festival Teluk Kendari"],
                    7: ["Festival Seni Budaya Tolaki"],
                    11: ["Festival Walima"]
                },
                "risks": ["Limited transportation options", "Hospital availability in remote areas"]
            },
            "Gorontalo": {
                "hotel_cost": 250000,  # per night
                "food_cost": {"breakfast": 25000, "lunch": 40000, "dinner": 55000},
                "snack_cost": 20000,  # per day
                "souvenirs": {"Karawo": 90000, "Kukis Pia": 40000, "Gula Aren": 35000},
                "local_transport": 85000,  # per day
                "weather": {
                    1: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-30°C"},
                    2: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-30°C"},
                    3: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-31°C"},
                    4: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-31°C"},
                    5: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-32°C"},
                    6: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-32°C"},
                    7: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-32°C"},
                    8: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-32°C"},
                    9: {"condition": "Dry", "risk_level": "Low", "temp_range": "24-32°C"},
                    10: {"condition": "Mixed", "risk_level": "Medium", "temp_range": "24-31°C"},
                    11: {"condition": "Rainy", "risk_level": "Medium", "temp_range": "24-31°C"},
                    12: {"condition": "Rainy", "risk_level": "High", "temp_range": "24-30°C"}
                },
                "events": {
                    5: ["Festival Karawo"],
                    8: ["Festival Danau Limboto"],
                    12: ["Festival Polopalo"]
                },
                "risks": ["Flooding during rainy season", "Limited tourist infrastructure"]
            }
        }
        
        # Flight information including potential delays by season
        self.flights = {
            "Surabaya-Makassar": {"cost": 800000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Surabaya-Manado": {"cost": 1200000, "rainy_delay_risk": 0.35, "dry_delay_risk": 0.15},
            "Surabaya-Palu": {"cost": 1000000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Surabaya-Kendari": {"cost": 1100000, "rainy_delay_risk": 0.25, "dry_delay_risk": 0.1},
            "Surabaya-Gorontalo": {"cost": 1300000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Makassar-Manado": {"cost": 600000, "rainy_delay_risk": 0.35, "dry_delay_risk": 0.15},
            "Makassar-Palu": {"cost": 500000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Makassar-Kendari": {"cost": 550000, "rainy_delay_risk": 0.25, "dry_delay_risk": 0.1},
            "Makassar-Gorontalo": {"cost": 700000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Manado-Palu": {"cost": 400000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Manado-Kendari": {"cost": 650000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Manado-Gorontalo": {"cost": 300000, "rainy_delay_risk": 0.25, "dry_delay_risk": 0.1},
            "Palu-Kendari": {"cost": 450000, "rainy_delay_risk": 0.3, "dry_delay_risk": 0.1},
            "Palu-Gorontalo": {"cost": 400000, "rainy_delay_risk": 0.25, "dry_delay_risk": 0.1},
            "Kendari-Gorontalo": {"cost": 500000, "rainy_delay_risk": 0.25, "dry_delay_risk": 0.1}
        }
        
        # Cost from home to airport
        self.home_to_airport = 100000
        
        # Contingency fund recommendation percentage
        self.contingency_percentage = 0.15
        
        # Potential unexpected events and their costs
        self.unexpected_events = {
            "flight_delay": {
                "description": "Penerbangan tertunda beberapa jam",
                "cost_range": (100000, 300000),  # Extra food, accommodation sometimes
                "probability": 0.2  # Base probability, modified by weather
            },
            "flight_cancellation": {
                "description": "Penerbangan dibatalkan, perlu menginap tambahan",
                "cost_range": (500000, 1000000),  # Hotel + meals + new ticket difference
                "probability": 0.05  # Base probability, modified by weather
            },
            "lost_baggage": {
                "description": "Bagasi hilang atau tertunda",
                "cost_range": (200000, 500000),  # Replacement necessities
                "probability": 0.03
            },
            "food_poisoning": {
                "description": "Keracunan makanan, memerlukan obat dan istirahat",
                "cost_range": (100000, 300000),  # Medicine, doctor visit
                "probability": 0.05
            },
            "transportation_strike": {
                "description": "Mogok transportasi lokal",
                "cost_range": (150000, 400000),  # Alternative transportation
                "probability": 0.02
            },
            "local_festival_price_surge": {
                "description": "Kenaikan harga karena festival lokal",
                "cost_range": (100000, 300000),  # Higher prices for everything
                "probability": 0.1
            },
            "sudden_illness": {
                "description": "Sakit mendadak selama perjalanan",
                "cost_range": (200000, 800000),  # Medical treatment
                "probability": 0.04
            },
            "natural_event": {
                "description": "Cuaca ekstrem atau peristiwa alam kecil",
                "cost_range": (300000, 1000000),  # Hotel extension, rebooking fees
                "probability": 0.02  # Base probability, modified by season and location
            }
        }
        
        # Final vacation plan
        self.best_plan = None
        self.best_remaining = float('inf')  # The smaller the remaining budget (but not negative) the better
        self.recommended_items = {
            "Rainy": ["Payung", "Jas hujan", "Sepatu tahan air", "Plastik kedap air untuk dokumen"],
            "Dry": ["Topi", "Sunscreen", "Kacamata hitam", "Baju ringan"],
            "Any": ["Obat pribadi", "P3K kecil", "Powerbank", "Dokumen perjalanan"]
        }
    
    def get_weather_risk_factor(self, city, travel_date):
        """Calculate risk factor based on weather for specified city and date."""
        month = travel_date.month
        weather_info = self.destinations[city]["weather"][month]
        
        risk_factor = 1.0  # Default no modification
        if weather_info["risk_level"] == "High":
            risk_factor = 1.5
        elif weather_info["risk_level"] == "Medium":
            risk_factor = 1.2
        
        return risk_factor, weather_info
    
    def calculate_flight_cost(self, origin, destination, travel_date):
        """Calculate flight cost including potential delays due to weather conditions."""
        if origin == destination:
            return 0, 0  # No flight needed, no delay risk
            
        key = f"{origin}-{destination}"
        reverse_key = f"{destination}-{origin}"
        
        if key in self.flights:
            flight_info = self.flights[key]
        elif reverse_key in self.flights:
            flight_info = self.flights[reverse_key]
        else:
            return 0, 0  # No direct flight
        
        # Get month-based weather conditions for destination
        month = travel_date.month
        if destination in self.destinations:
            weather_condition = self.destinations[destination]["weather"][month]["condition"]
            
            # Determine delay risk based on weather
            if weather_condition == "Rainy":
                delay_risk = flight_info["rainy_delay_risk"]
            else:  # Dry or Mixed
                delay_risk = flight_info["dry_delay_risk"]
        else:
            delay_risk = 0.1  # Default if destination not specified
        
        return flight_info["cost"], delay_risk
    
    def get_event_at_date(self, city, travel_date):
        """Check if there are any events at the destination on the given date."""
        month = travel_date.month
        return self.destinations[city]["events"].get(month, [])
    
    def generate_potential_issues(self, city, days, travel_date, delay_risk):
        """Generate potential unexpected events based on location, duration, and season."""
        issues = []
        month = travel_date.month
        weather_info = self.destinations[city]["weather"][month]
        
        # Check for city-specific risks
        city_risks = self.destinations[city].get("risks", [])
        
        # Consider weather-related risks
        weather_risk_factor = 1.0
        if weather_info["condition"] == "Rainy":
            weather_risk_factor = 1.5
        
        # Each day of stay increases chance of encountering an issue
        for day in range(days):
            current_date = travel_date + timedelta(days=day)
            
            # Check flight delay risk (applies to arrival day)
            if day == 0 and random.random() < delay_risk:
                cost = random.randint(*self.unexpected_events["flight_delay"]["cost_range"])
                issues.append({
                    "day": current_date.strftime("%d %b %Y"),
                    "event": self.unexpected_events["flight_delay"]["description"],
                    "cost": cost
                })
            
            # Check for food poisoning
            if random.random() < self.unexpected_events["food_poisoning"]["probability"] * days / 10:
                cost = random.randint(*self.unexpected_events["food_poisoning"]["cost_range"])
                issues.append({
                    "day": current_date.strftime("%d %b %Y"),
                    "event": self.unexpected_events["food_poisoning"]["description"],
                    "cost": cost
                })
            
            # Check for special events that might cause price surges
            events = self.get_event_at_date(city, current_date)
            if events and random.random() < self.unexpected_events["local_festival_price_surge"]["probability"] * 2:
                cost = random.randint(*self.unexpected_events["local_festival_price_surge"]["cost_range"])
                issues.append({
                    "day": current_date.strftime("%d %b %Y"),
                    "event": f"{self.unexpected_events['local_festival_price_surge']['description']} ({', '.join(events)})",
                    "cost": cost
                })
            
            # Weather-related issues
            if weather_info["condition"] == "Rainy" and random.random() < 0.1 * weather_risk_factor:
                if any("flood" in risk.lower() for risk in city_risks):
                    cost = random.randint(100000, 300000)
                    issues.append({
                        "day": current_date.strftime("%d %b %Y"),
                        "event": "Banjir lokal mempengaruhi transportasi",
                        "cost": cost
                    })
            
            # Natural events based on location-specific risks
            if any("volcano" in risk.lower() for risk in city_risks) and random.random() < 0.01:
                cost = random.randint(*self.unexpected_events["natural_event"]["cost_range"])
                issues.append({
                    "day": current_date.strftime("%d %b %Y"),
                    "event": "Peningkatan aktivitas gunung berapi menyebabkan pembatalan tur",
                    "cost": cost
                })
                
            if any("earthquake" in risk.lower() for risk in city_risks) and random.random() < 0.005:
                cost = random.randint(*self.unexpected_events["natural_event"]["cost_range"])
                issues.append({
                    "day": current_date.strftime("%d %b %Y"),
                    "event": "Gempa kecil menyebabkan perubahan rencana",
                    "cost": cost
                })
        
        return issues
    def generate_vacation_plan(self):
        """Menggunakan backtracking untuk menghasilkan rencana liburan optimal dengan mempertimbangkan berbagai risiko."""
        # Mulai dengan semua kota
        cities = list(self.destinations.keys())
        
        # Urutkan kota berdasarkan biaya hotel dari rendah ke tinggi
        cities.sort(key=lambda city: self.destinations[city]["hotel_cost"])
        
        # Backtracking untuk mencari rencana liburan optimal
        def backtrack(current_plan, remaining_budget, current_city="Surabaya", visited_cities=None, current_date=None):
            if visited_cities is None:
                visited_cities = set()
            if current_date is None:
                current_date = self.start_date
            
            # Jika sudah mengunjungi semua kota atau anggaran habis
            if len(visited_cities) == len(cities) or remaining_budget <= 0:
                # Hitung biaya pulang ke Surabaya
                return_cost, return_delay_risk = self.calculate_flight_cost(current_city, "Surabaya", current_date)
                
                # Jika masih ada anggaran untuk pulang ke Surabaya
                if remaining_budget >= return_cost:
                    # Pastikan kita mengunjungi minimal 2 kota
                    if len(visited_cities) >= 2:
                        # Tambahkan biaya pulang ke Surabaya
                        final_plan = current_plan.copy()
                        if current_city != "Surabaya":
                            # Generate potential issues for return flight
                            return_issues = []
                            if random.random() < return_delay_risk:
                                delay_cost = random.randint(*self.unexpected_events["flight_delay"]["cost_range"])
                                return_issues.append({
                                    "day": current_date.strftime("%d %b %Y"),
                                    "event": self.unexpected_events["flight_delay"]["description"],
                                    "cost": delay_cost
                                })
                                
                            final_plan.append({
                                "activity": "flight",
                                "from": current_city,
                                "to": "Surabaya",
                                "date": current_date.strftime("%d %b %Y"),
                                "cost": return_cost,
                                "delay_risk": return_delay_risk,
                                "potential_issues": return_issues
                            })
                        
                        final_remaining = remaining_budget - return_cost
                        
                        # Kurangi biaya potensial masalah di penerbangan pulang
                        for issue in return_issues if 'return_issues' in locals() else []:
                            final_remaining -= issue["cost"]
                        
                        # Update rencana terbaik jika ini menggunakan anggaran lebih optimal
                        if 0 <= final_remaining < self.best_remaining:
                            self.best_plan = final_plan
                            self.best_remaining = final_remaining
                
                return
            
            # Coba kunjungi kota-kota yang belum dikunjungi
            for city in cities:
                if city not in visited_cities:
                    # Hitung biaya penerbangan ke kota ini
                    flight_cost, delay_risk = self.calculate_flight_cost(current_city, city, current_date)
                    
                    # Jika biaya penerbangan lebih dari sisa anggaran, skip
                    if flight_cost > remaining_budget:
                        continue
                    
                    # Generate potential issues for this flight
                    flight_issues = []
                    if random.random() < delay_risk:
                        delay_cost = random.randint(*self.unexpected_events["flight_delay"]["cost_range"])
                        flight_issues.append({
                            "day": current_date.strftime("%d %b %Y"),
                            "event": self.unexpected_events["flight_delay"]["description"],
                            "cost": delay_cost
                        })
                    
                    # Tambahkan aktivitas penerbangan
                    current_plan.append({
                        "activity": "flight",
                        "from": current_city,
                        "to": city,
                        "date": current_date.strftime("%d %b %Y"),
                        "cost": flight_cost,
                        "delay_risk": delay_risk,
                        "potential_issues": flight_issues
                    })
                    
                    # Kurangi anggaran
                    current_remaining = remaining_budget - flight_cost
                    
                    # Kurangi biaya dari potensi masalah penerbangan
                    for issue in flight_issues:
                        current_remaining -= issue["cost"]
                    
                    # Jika anggaran menjadi negatif karena masalah, backtrack
                    if current_remaining < 0:
                        current_plan.pop()
                        continue
                    
                    # Tanggal setelah terbang (anggap penerbangan memakan waktu 1 hari)
                    next_date = current_date + timedelta(days=1)
                    
                    # Coba berbagai durasi menginap
                    for days in range(1, 5):  # Coba 1-4 hari
                        # Hitung risiko berdasarkan cuaca di kota dan tanggal tersebut
                        risk_factor, weather_info = self.get_weather_risk_factor(city, next_date)
                        
                        # Hitung semua biaya untuk durasi ini
                        hotel_cost = self.destinations[city]["hotel_cost"] * days
                        food_cost = sum(self.destinations[city]["food_cost"].values()) * days
                        snack_cost = self.destinations[city]["snack_cost"] * days
                        transport_cost = self.destinations[city]["local_transport"] * days
                        
                        # Pilih souvenir acak
                        souvenir_items = random.sample(list(self.destinations[city]["souvenirs"].items()), 
                                                      min(days, len(self.destinations[city]["souvenirs"])))
                        souvenir_cost = sum(price for _, price in souvenir_items)
                        
                        # Total biaya untuk kunjungan ini
                        total_cost = hotel_cost + food_cost + snack_cost + transport_cost + souvenir_cost
                        
                        # Jika biaya total lebih dari sisa anggaran, coba durasi lain
                        if total_cost > current_remaining:
                            continue
                        
                        # Generate potential issues for this stay
                        stay_issues = self.generate_potential_issues(city, days, next_date, delay_risk)
                        
                        # Hitung total biaya masalah
                        issues_cost = sum(issue["cost"] for issue in stay_issues)
                        
                        # Jika total biaya termasuk masalah melebihi anggaran, coba durasi lain
                        if total_cost + issues_cost > current_remaining:
                            continue
                        
                        # Cek event/festival selama periode ini
                        events = []
                        for d in range(days):
                            event_date = next_date + timedelta(days=d)
                            day_events = self.get_event_at_date(city, event_date)
                            if day_events:
                                events.extend([f"{event} ({event_date.strftime('%d %b')})" for event in day_events])
                        
                        # Tambahkan aktivitas penginapan
                        current_plan.append({
                            "activity": "stay",
                            "city": city,
                            "days": days,
                            "start_date": next_date.strftime("%d %b %Y"),
                            "end_date": (next_date + timedelta(days=days-1)).strftime("%d %b %Y"),
                            "hotel_cost": hotel_cost,
                            "food_cost": food_cost,
                            "snack_cost": snack_cost,
                            "local_transport": transport_cost,
                            "souvenirs": dict(souvenir_items),
                            "total_cost": total_cost,
                            "weather": weather_info,
                            "events": events,
                            "potential_issues": stay_issues
                        })
                        
                        # Update visited cities
                        visited_cities.add(city)
                        
                        # Lanjutkan backtracking
                        next_city_date = next_date + timedelta(days=days)
                        backtrack(current_plan, current_remaining - total_cost - issues_cost, 
                                 city, visited_cities, next_city_date)
                        
                        # Backtrack: hapus aktivitas penginapan
                        current_plan.pop()
                        visited_cities.remove(city)
                    
                    # Backtrack: hapus aktivitas penerbangan
                    current_plan.pop()
        
        # Mulai backtracking
        initial_plan = [{
            "activity": "home_to_airport",
            "date": self.start_date.strftime("%d %b %Y"),
            "cost": self.home_to_airport
        }]
        backtrack(initial_plan, self.total_budget - self.home_to_airport, 
                 "Surabaya", set(), self.start_date)
        
        return self.best_plan, self.total_budget - self.best_remaining

    def recommend_items(self, plan):
        """Merekomendasikan barang yang perlu dibawa berdasarkan rencana perjalanan."""
        if not plan:
            return []
        
        items = set(self.recommended_items["Any"])
        has_rainy = False
        has_dry = False
        
        for activity in plan:
            if activity["activity"] == "stay":
                weather = activity.get("weather", {}).get("condition", "")
                if weather == "Rainy":
                    has_rainy = True
                elif weather == "Dry":
                    has_dry = True
        
        if has_rainy:
            items.update(self.recommended_items["Rainy"])
        if has_dry:
            items.update(self.recommended_items["Dry"])
        
        return sorted(items)
    
    def calculate_contingency_fund(self, plan):
        """Menghitung dana darurat yang direkomendasikan berdasarkan rencana perjalanan."""
        if not plan:
            return 0
        
        total_issues_cost = 0
        highest_risk_issue = 0
        
        # Hitung total biaya potensial dari masalah dan identifikasi masalah termahal
        for activity in plan:
            issues = activity.get("potential_issues", [])
            for issue in issues:
                issue_cost = issue.get("cost", 0)
                total_issues_cost += issue_cost
                highest_risk_issue = max(highest_risk_issue, issue_cost)
        
        # Dana darurat adalah persentase dari total biaya + biaya masalah termahal
        base_cost = sum(activity["cost"] if "cost" in activity else 
                         activity.get("total_cost", 0) for activity in plan)
        
        contingency = base_cost * self.contingency_percentage + highest_risk_issue
        
        return int(contingency)
        
    def print_vacation_plan(self):
        """Mencetak rencana liburan dalam format yang mudah dibaca dengan informasi risiko."""
        plan, total_cost = self.generate_vacation_plan()
        
        if not plan:
            print("Tidak dapat menemukan rencana liburan yang sesuai dengan anggaran.")
            return
        
        print("=" * 80)
        print("RENCANA LIBURAN SURABAYA KE SULAWESI".center(80))
        print("=" * 80)
        print(f"Anggaran Total: Rp {self.total_budget:,}")
        print(f"Biaya Total: Rp {total_cost:,}")
        print(f"Sisa Anggaran: Rp {self.best_remaining:,}")
        print(f"Tanggal Mulai: {self.start_date.strftime('%d %B %Y')}")
        print("=" * 80)
        
        day_count = 1
        for activity in plan:
            if activity["activity"] == "home_to_airport":
                print(f"Hari {day_count} ({activity['date']}):")
                print(f"- Perjalanan dari rumah ke Bandara Juanda (Surabaya)")
                print(f"  Biaya: Rp {activity['cost']:,}")
                print()
            
            elif activity["activity"] == "flight":
                print(f"Hari {day_count} ({activity['date']}):")
                print(f"- Penerbangan dari {activity['from']} ke {activity['to']}")
                print(f"  Biaya: Rp {activity['cost']:,}")
                print(f"  Risiko Keterlambatan: {activity['delay_risk']*100:.1f}%")
                
                if activity["potential_issues"]:
                    print("  Potensi Masalah:")
                    for issue in activity["potential_issues"]:
                        print(f"    - {issue['event']} (Biaya: Rp {issue['cost']:,})")
                print()
                day_count += 1
            
            elif activity["activity"] == "stay":
                print(f"Hari {day_count} - {day_count + activity['days'] - 1} ({activity['start_date']} - {activity['end_date']}): {activity['city']}")
                print(f"- Menginap selama {activity['days']} hari")
                print(f"  Hotel: Rp {activity['hotel_cost']:,}")
                print(f"  Makan: Rp {activity['food_cost']:,}")
                print(f"  Snack: Rp {activity['snack_cost']:,}")
                print(f"  Transportasi Lokal: Rp {activity['local_transport']:,}")
                print("  Souvenirs:")
                for item, price in activity['souvenirs'].items():
                    print(f"    - {item}: Rp {price:,}")
                print(f"  Total biaya di {activity['city']}: Rp {activity['total_cost']:,}")
                print(f"  Cuaca: {activity['weather']['condition']} ({activity['weather']['temp_range']})")
                
                if activity["events"]:
                    print("  Event/Festival:")
                    for event in activity["events"]:
                        print(f"    - {event}")
                
                if activity["potential_issues"]:
                    print("  Potensi Masalah:")
                    for issue in activity["potential_issues"]:
                        print(f"    - {issue['day']}: {issue['event']} (Biaya: Rp {issue['cost']:,})")
                print()
                day_count += activity['days']
        
        # Calculate and display contingency fund
        contingency_fund = self.calculate_contingency_fund(plan)
        
        print("=" * 80)
        print("REKOMENDASI BARANG:".center(80))
        recommended_items = self.recommend_items(plan)
        for item in recommended_items:
            print(f"- {item}")
        print()
        
        print("=" * 80)
        print("RINGKASAN BIAYA DAN RISIKO:".center(80))
        print(f"Anggaran Awal: Rp {self.total_budget:,}")
        print(f"Total Biaya: Rp {total_cost:,}")
        print(f"Sisa Anggaran: Rp {self.best_remaining:,}")
        print(f"Dana Darurat yang Direkomendasikan: Rp {contingency_fund:,}")
        print(f"Persentase Anggaran Terpakai: {(total_cost / self.total_budget) * 100:.2f}%")
        
        # Calculate total potential risk costs
        total_risk_cost = 0
        for activity in plan:
            for issue in activity.get("potential_issues", []):
                total_risk_cost += issue["cost"]
        
        if total_risk_cost > 0:
            print(f"Potensi Biaya Risiko: Rp {total_risk_cost:,}")
            print(f"Rencana perjalanan memiliki faktor risiko {(total_risk_cost / total_cost) * 100:.2f}%")
        print("=" * 80)

# Jalankan program
if __name__ == "__main__":
    # Tentukan tanggal mulai (misal 1 Juli 2023)
    start_date = datetime(2023, 7, 1)
    planner = VacationPlanner(budget=10000000, start_date=start_date)
    planner.print_vacation_plan()

 
time.sleep(1) 
# store end time 
end = time.time() 
 
# total time taken 
print(f"Total runtime of the program is {end - begin} seconds.") 

'''
Implementasi Backtracking dalam Program
Fungsi backtrack pada program ini adalah jantung dari algoritma backtracking yang digunakan. Mari saya jelaskan cara kerjanya:
- Kondisi Batas: Algoritma berhenti ketika semua kota telah dikunjungi atau anggaran habis. Ini adalah kondisi batas yang menentukan
kapan pencarian berhenti. Pencarian Sistematis: Program mencoba mengunjungi setiap kota yang belum dikunjungi dengan berbagai 
kemungkinan durasi menginap (1-4 hari). Setiap kombinasi mewakili satu cabang pada pohon pencarian.
- Proses Mundur (Backtrack): Ketika suatu jalur eksplorasi tidak memungkinkan (misalnya, anggaran tidak cukup), program akan mundur
ke jalur sebelumnya dan mencoba alternatif lain. Ini diimplementasikan dengan menghapus aktivitas terakhir dari rencana saat ini dan
memulihkan status sebelumnya. 
- Optimasi: Program mempertahankan solusi terbaik yang ditemukan sejauh ini (self.best_plan) dan sisa
anggaran terkecil yang tidak negatif (self.best_remaining). Kriteria optimasinya adalah meminimalkan sisa anggaran (mengoptimalkan
penggunaan anggaran).


Kelebihan Pendekatan Backtracking
- Jaminan Solusi Optimal: Backtracking secara sistematis menjelajahi semua kemungkinan solusi, sehingga menjamin menemukan solusi
  optimal jika ada. Dalam konteks ini, program akan menemukan rencana perjalanan yang menggunakan anggaran secara maksimal tanpa melebihi batas.
- Fleksibilitas: Pendekatan ini sangat fleksibel dan dapat menangani berbagai batasan dan kriteria optimasi. Program dapat dengan 
  mudah dimodifikasi untuk mengoptimalkan kriteria lain seperti durasi perjalanan, jumlah kota yang dikunjungi, atau preferensi destinasi.
- Penyesuaian Dinamis: Program dapat menyesuaikan durasi kunjungan ke setiap kota (1-4 hari) berdasarkan anggaran yang tersisa, 
  menciptakan rencana perjalanan yang disesuaikan dengan kebutuhan.

Kekurangan Pendekatan Backtracking
- Kompleksitas Waktu Eksponensial Algoritma backtracking memiliki waktu eksekusi yang bisa sangat lambat untuk dataset besar. Dalam 
  kasus ini, dengan 5 kota dan 4 kemungkinan durasi, kompleksitasnya sekitar O(5! × 4^5), yang bisa menjadi masalah jika jumlah kota 
  atau opsi durasi bertambah.
- Konsumsi Memori: Algoritma rekursif membutuhkan ruang memori untuk stack rekursif, yang bisa menjadi masalah untuk dataset besar 
  atau komputer dengan memori terbatas.
'''
