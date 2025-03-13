# Interactive Film Recommendation System with CSV Integration
# This program implements a film recommendation system using A* algorithm with CSV database

import heapq
import csv
import os
from collections import defaultdict

# Define a Film class to store movie information
class Film:
    def __init__(self, id, title, genres=None, actors=None, director=None, year=None, rating=None):
        self.id = id
        self.title = title
        self.genres = genres or []
        self.actors = actors or []
        self.director = director
        self.year = year
        self.rating = rating
        
    def __str__(self):
        return f"{self.title} ({self.year}) - Rating: {self.rating}"
    
    def __repr__(self):
        return self.__str__()
        
    def to_csv_row(self):
        """Convert film object to CSV row format"""
        return [
            self.id,
            self.title,
            "|".join(self.genres),
            "|".join(self.actors),
            self.director if self.director else "",
            self.year if self.year else "",
            self.rating if self.rating else ""
        ]
    
    @classmethod
    def from_csv_row(cls, row):
        """Create a Film object from a CSV row"""
        try:
            film_id = int(row[0])
            title = row[1]
            genres = row[2].split("|") if row[2] else []
            actors = row[3].split("|") if row[3] else []
            director = row[4] if row[4] else None
            year = int(row[5]) if row[5] and row[5].isdigit() else None
            rating = float(row[6]) if row[6] else None
            
            return cls(film_id, title, genres, actors, director, year, rating)
        except (IndexError, ValueError) as e:
            print(f"Error parsing row: {row}. Error: {e}")
            return None

# Define a Graph class to represent the film similarity network
class FilmGraph:
    def __init__(self):
        self.nodes = {}  # Maps film_id to Film object
        self.edges = defaultdict(list)  # Maps film_id to list of (neighbor_id, weight) tuples
        
    def add_film(self, film):
        """Add a film node to the graph"""
        self.nodes[film.id] = film
        
    def add_edge(self, film1_id, film2_id, weight):
        """Add an edge between two films with a similarity weight"""
        # Lower weight means higher similarity
        self.edges[film1_id].append((film2_id, weight))
        self.edges[film2_id].append((film1_id, weight))  # Undirected graph
        
    def calculate_similarity(self, film1, film2):
        """Calculate similarity between two films based on attributes"""
        similarity = 0
        
        # Genre similarity (0-5 points)
        genre_match = len(set(film1.genres) & set(film2.genres))
        similarity += min(5, genre_match * 2)
        
        # Actor similarity (0-3 points)
        actor_match = len(set(film1.actors) & set(film2.actors))
        similarity += min(3, actor_match)
        
        # Director similarity (0-2 points)
        if film1.director == film2.director and film1.director is not None:
            similarity += 2
            
        # Year similarity (0-1 point)
        if film1.year and film2.year:
            year_diff = abs(film1.year - film2.year)
            if year_diff <= 5:
                similarity += 1
        
        # Convert similarity score to distance (lower is better in A*)
        # We use a 10-point scale and invert it, so 0 means identical films, 10 means completely different
        distance = 10 - similarity
        return max(0.1, distance)  # Ensure distance is never zero to avoid issues
    
    def build_similarity_edges(self, threshold=6.0):
        """Build edges between all films with similarity above threshold"""
        film_ids = list(self.nodes.keys())
        
        # For each film, compare with all other films
        for i, film1_id in enumerate(film_ids):
            film1 = self.nodes[film1_id]
            
            for film2_id in film_ids[i+1:]:  # Avoid duplicate comparisons
                film2 = self.nodes[film2_id]
                
                # Calculate similarity and convert to distance
                distance = self.calculate_similarity(film1, film2)
                
                # Only add edge if films are similar enough (distance is low enough)
                if distance <= threshold:
                    self.add_edge(film1_id, film2_id, distance)
        
        # Ensure all films have at least some connections by adding more if needed
        for film_id in self.nodes:
            if len(self.edges[film_id]) == 0:
                # Find 3 most similar films
                similarities = []
                for other_id in self.nodes:
                    if other_id != film_id:
                        distance = self.calculate_similarity(self.nodes[film_id], self.nodes[other_id])
                        similarities.append((other_id, distance))
                
                # Add edges to the 3 most similar films
                for other_id, distance in sorted(similarities, key=lambda x: x[1])[:3]:
                    self.add_edge(film_id, other_id, distance)

# A* Algorithm implementation for film recommendations
class FilmRecommender:
    def __init__(self, film_graph):
        self.graph = film_graph
        
    def heuristic(self, film_id, user_preferences):
        """Calculate heuristic for A* algorithm based on user preferences"""
        film = self.graph.nodes[film_id]
        score = 0
        
        # Factor in genre preferences
        for genre in film.genres:
            score -= user_preferences.get('genres', {}).get(genre, 0)
            
        # Factor in actor preferences
        for actor in film.actors:
            score -= user_preferences.get('actors', {}).get(actor, 0)
            
        # Factor in director preferences
        if film.director:
            score -= user_preferences.get('directors', {}).get(film.director, 0)
            
        # Factor in year preferences (closer to preferred years gets better score)
        if film.year and 'preferred_years' in user_preferences:
            min_diff = min(abs(film.year - year) for year in user_preferences['preferred_years'])
            score += min_diff * 0.1  # Small penalty for year difference
            
        # Rating bonus (higher rated films get lower scores, which is better for A*)
        if film.rating:
            score -= film.rating / 2
            
        return max(0, score)  # Ensure heuristic is non-negative
    
    def recommend_films(self, liked_film_ids, user_preferences, num_recommendations=5):
        """Use A* to find film recommendations based on liked films and preferences"""
        if not liked_film_ids:
            return []
        
        # We'll track visited films to avoid duplicates
        visited = set(liked_film_ids)
        
        # Our list of recommendations
        recommendations = []
        
        # Priority queue for A* search
        open_set = []
        
        # Initialize with liked films
        for film_id in liked_film_ids:
            # For each starting film, add its neighbors to open set
            for neighbor_id, weight in self.graph.edges[film_id]:
                if neighbor_id not in visited:
                    # Calculate priority score (lower is better)
                    h_score = self.heuristic(neighbor_id, user_preferences)
                    f_score = weight + h_score
                    heapq.heappush(open_set, (f_score, neighbor_id))
        
        # Main A* loop - simplified for recommendation purpose
        while open_set and len(recommendations) < num_recommendations:
            # Get film with best score
            f_score, current_film_id = heapq.heappop(open_set)
            
            # Skip if already visited
            if current_film_id in visited:
                continue
                
            # Mark as visited
            visited.add(current_film_id)
            
            # Add to recommendations
            recommendations.append(self.graph.nodes[current_film_id])
            
            # Add neighbors to open set
            for neighbor_id, weight in self.graph.edges[current_film_id]:
                if neighbor_id not in visited:
                    # Calculate priority score
                    h_score = self.heuristic(neighbor_id, user_preferences)
                    f_score = weight + h_score
                    heapq.heappush(open_set, (f_score, neighbor_id))
        
        return recommendations

# Database and file handling functionality
class FilmDatabase:
    def __init__(self, movies_file="movies_database.csv", watched_file="watched_films.csv"):
        self.movies_file = movies_file
        self.watched_file = watched_file
        self.next_id = 1
        
        # Create files if they don't exist
        self._ensure_files_exist()
        
    def _ensure_files_exist(self):
        """Make sure the CSV files exist with proper headers"""
        # Movies database file
        if not os.path.exists(self.movies_file):
            with open(self.movies_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'genres', 'actors', 'director', 'year', 'rating'])
                # Add some sample data
                self._add_sample_data(writer)
        
        # Watched films file
        if not os.path.exists(self.watched_file):
            with open(self.watched_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'genres', 'actors', 'director', 'year', 'rating'])
    
    def _add_sample_data(self, writer):
        """Add sample film data to a new database"""
        sample_films = [
            [1, "The Shawshank Redemption", "Drama", "Tim Robbins|Morgan Freeman", "Frank Darabont", 1994, 9.3],
            [2, "The Godfather", "Crime|Drama", "Marlon Brando|Al Pacino", "Francis Ford Coppola", 1972, 9.2],
            [3, "The Dark Knight", "Action|Crime|Drama", "Christian Bale|Heath Ledger", "Christopher Nolan", 2008, 9.0],
            [4, "The Godfather: Part II", "Crime|Drama", "Al Pacino|Robert De Niro", "Francis Ford Coppola", 1974, 9.0],
            [5, "12 Angry Men", "Crime|Drama", "Henry Fonda|Lee J. Cobb", "Sidney Lumet", 1957, 9.0],
            [6, "Pulp Fiction", "Crime|Drama", "John Travolta|Uma Thurman|Samuel L. Jackson", "Quentin Tarantino", 1994, 8.9],
            [7, "Inception", "Action|Adventure|Sci-Fi", "Leonardo DiCaprio|Joseph Gordon-Levitt", "Christopher Nolan", 2010, 8.8],
            [8, "Fight Club", "Drama", "Brad Pitt|Edward Norton", "David Fincher", 1999, 8.8],
            [9, "The Matrix", "Action|Sci-Fi", "Keanu Reeves|Laurence Fishburne", "Lana Wachowski", 1999, 8.7],
            [10, "Interstellar", "Adventure|Drama|Sci-Fi", "Matthew McConaughey|Anne Hathaway", "Christopher Nolan", 2014, 8.6],
            [11, "Goodfellas", "Biography|Crime|Drama", "Robert De Niro|Ray Liotta|Joe Pesci", "Martin Scorsese", 1990, 8.7],
            [12, "The Silence of the Lambs", "Crime|Drama|Thriller", "Jodie Foster|Anthony Hopkins", "Jonathan Demme", 1991, 8.6],
            [13, "Django Unchained", "Drama|Western", "Jamie Foxx|Christoph Waltz|Leonardo DiCaprio|Samuel L. Jackson", "Quentin Tarantino", 2012, 8.4],
            [14, "Toy Story", "Animation|Adventure|Comedy", "Tom Hanks|Tim Allen", "John Lasseter", 1995, 8.3],
            [15, "The Departed", "Crime|Drama|Thriller", "Leonardo DiCaprio|Matt Damon|Jack Nicholson", "Martin Scorsese", 2006, 8.5]
        ]
        for film in sample_films:
            writer.writerow(film)
        self.next_id = len(sample_films) + 1
        
    def load_all_films(self):
        """Load all films from the movies database"""
        films = []
        with open(self.movies_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                film = Film.from_csv_row(row)
                if film:
                    films.append(film)
                    # Keep track of the highest ID for new additions
                    self.next_id = max(self.next_id, film.id + 1)
        return films
    
    def load_watched_films(self):
        """Load all watched films"""
        watched_films = []
        with open(self.watched_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                film = Film.from_csv_row(row)
                if film:
                    watched_films.append(film)
        return watched_films
    
    def search_film_by_title(self, title):
        """Search for films in the database by title"""
        matching_films = []
        with open(self.movies_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2 and title.lower() in row[1].lower():
                    film = Film.from_csv_row(row)
                    if film:
                        matching_films.append(film)
        return matching_films
    
    def add_to_watched(self, film):
        """Add a film to the watched films list"""
        # Check if film is already in watched list
        watched_films = self.load_watched_films()
        for existing in watched_films:
            if existing.id == film.id:
                print(f"Film '{film.title}' is already in your watched list.")
                return False
        
        # Add to watched films
        with open(self.watched_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(film.to_csv_row())
        print(f"Added '{film.title}' to your watched films.")
        return True
    
    def get_watched_ids(self):
        """Get the IDs of all watched films"""
        watched_films = self.load_watched_films()
        return [film.id for film in watched_films]

# Interactive menu for the recommendation system
class RecommendationSystem:
    def __init__(self):
        self.db = FilmDatabase()
        
        # Load films and build graph
        all_films = self.db.load_all_films()
        self.graph = FilmGraph()
        for film in all_films:
            self.graph.add_film(film)
        
        # Build similarity edges
        print("Building film similarity network...")
        self.graph.build_similarity_edges()
        
        # Create recommender
        self.recommender = FilmRecommender(self.graph)
        
        # Default user preferences - will be updated based on watched films
        self.user_preferences = {
            'genres': {},
            'actors': {},
            'directors': {},
            'preferred_years': []
        }
        
    def update_preferences(self):
        """Update user preferences based on watched films"""
        watched_films = self.db.load_watched_films()
        
        # Reset preferences
        self.user_preferences = {
            'genres': {},
            'actors': {},
            'directors': {},
            'preferred_years': []
        }
        
        # No watched films, use default preferences
        if not watched_films:
            return
        
        # Count occurrences to find preferences
        genre_count = defaultdict(int)
        actor_count = defaultdict(int)
        director_count = defaultdict(int)
        years = []
        
        for film in watched_films:
            # Count genres
            for genre in film.genres:
                genre_count[genre] += 1
            
            # Count actors
            for actor in film.actors:
                actor_count[actor] += 1
            
            # Count directors
            if film.director:
                director_count[film.director] += 1
            
            # Collect years
            if film.year:
                years.append(film.year)
        
        # Normalize counts to preferences (0-1 scale)
        if genre_count:
            max_genre = max(genre_count.values())
            for genre, count in genre_count.items():
                self.user_preferences['genres'][genre] = count / max_genre
        
        if actor_count:
            max_actor = max(actor_count.values())
            for actor, count in actor_count.items():
                self.user_preferences['actors'][actor] = count / max_actor
        
        if director_count:
            max_director = max(director_count.values())
            for director, count in director_count.items():
                self.user_preferences['directors'][director] = count / max_director
        
        # Use median year and recent years as preferences
        if years:
            median_year = sorted(years)[len(years) // 2]
            self.user_preferences['preferred_years'] = [median_year, max(years)]
    
    def display_watched_films(self):
        """Display all watched films"""
        watched_films = self.db.load_watched_films()
        
        print("\nWatched Films:")
        if not watched_films:
            print("No films watched yet.")
        else:
            for i, film in enumerate(watched_films, 1):
                print(f"{i}. {film}")
    
    def add_watched_film(self):
        """Add a film to the watched list"""
        title = input("\nEnter film title to search: ")
        matching_films = self.db.search_film_by_title(title)
        
        if not matching_films:
            print("No matching films found.")
            return
        
        print("\nMatching films:")
        for i, film in enumerate(matching_films, 1):
            print(f"{i}. {film}")
        
        choice = input("\nSelect a film number to add to watched list (or 0 to cancel): ")
        try:
            choice = int(choice)
            if choice == 0:
                return
            if 1 <= choice <= len(matching_films):
                selected_film = matching_films[choice - 1]
                self.db.add_to_watched(selected_film)
                # Update preferences when a new film is added
                self.update_preferences()
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
    
    def show_recommendations(self):
        """Show film recommendations based on watched films"""
        # Update preferences first
        self.update_preferences()
        
        # Get watched film IDs
        watched_ids = self.db.get_watched_ids()
        
        if not watched_ids:
            print("\nYou need to add some watched films first to get recommendations.")
            return
        
        # Generate recommendations
        print("\nGenerating recommendations based on your watched films...")
        recommendations = self.recommender.recommend_films(
            watched_ids, 
            self.user_preferences, 
            num_recommendations=5
        )
        
        print("\nRecommended films for you:")
        if not recommendations:
            print("Couldn't generate recommendations. Try adding more watched films.")
        else:
            for i, film in enumerate(recommendations, 1):
                print(f"{i}. {film}")
    
    def run(self):
        """Run the interactive recommendation system"""
        print("Welcome to the Film Recommendation System!")
        
        while True:
            self.display_watched_films()
            
            print("\nMenu:")
            print("1. Add Watched Films")
            print("2. Recommendation")
            print("3. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                self.add_watched_film()
            elif choice == '2':
                self.show_recommendations()
            elif choice == '3':
                print("Thank you for using the Film Recommendation System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Main entry point
if __name__ == "__main__":
    system = RecommendationSystem()
    system.run()