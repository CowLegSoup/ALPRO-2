import csv
import os
import random
from collections import defaultdict

# Simple Film class to store basic movie information
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

# Poorly designed database with no indexing and inefficient operations
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
            [10, "Interstellar", "Adventure|Drama|Sci-Fi", "Matthew McConaughey|Anne Hathaway", "Christopher Nolan", 2014, 8.6]
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
        """Search for films in the database by title (inefficient implementation)"""
        # Inefficiently reloads all films for each search
        all_films = self.load_all_films()
        matching_films = []
        
        # Linear search instead of using indexing
        for film in all_films:
            if title.lower() in film.title.lower():
                matching_films.append(film)
        
        return matching_films
    
    def add_to_watched(self, film):
        """Add a film to the watched films list"""
        # Inefficiently checks if film is already in watched list
        watched_films = self.load_watched_films()
        
        # Linear search through all watched films
        for existing in watched_films:
            if existing.id == film.id:
                print(f"Film '{film.title}' is already in your watched list.")
                return False
        
        # Append to CSV (inefficient for large files)
        with open(self.watched_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(film.to_csv_row())
            
        print(f"Added '{film.title}' to your watched films.")
        return True

# Ford-Fulkerson implementation for film recommendation (completely inappropriate)
class BadRecommendationSystem:
    def __init__(self):
        self.db = FilmDatabase()
        self.all_films = self.db.load_all_films()
        self.film_id_map = {film.id: i for i, film in enumerate(self.all_films)}
        self.film_graph = self._build_flow_network()
        
    def _build_flow_network(self):
        # Get all films
        n = len(self.all_films)
        
        # Create a flow network as a 2D array (adjacency matrix)
        # This is very inefficient for sparse data
        graph = [[0 for _ in range(n + 2)] for _ in range(n + 2)]  # +2 for source and sink
        
        # Source is at index n, sink is at index n+1
        source = n
        sink = n + 1
        
        # Connect source to all films (inappropriate modeling)
        for i in range(n):
            # Film rating influences "flow capacity" (makes no sense for recommendations)
            rating = self.all_films[i].rating or 5.0
            graph[source][i] = int(rating * 10)  # Convert rating to integer capacity
        
        # Connect films to each other based on genres (poor design)
        for i in range(n):
            film1 = self.all_films[i]
            for j in range(n):
                if i == j:
                    continue
                    
                film2 = self.all_films[j]
                
                # Calculate some arbitrary similarity 
                similarity = 0
                for genre in film1.genres:
                    if genre in film2.genres:
                        similarity += 10
                
                # Set some small capacity for all films of the same genre
                # This completely ignores most similarity factors and creates many useless edges
                if similarity > 0:
                    graph[i][j] = similarity
        
        # Connect all films to sink with arbitrary capacities
        for i in range(n):
            # More arbitrary capacity assignment
            graph[i][sink] = 100
            
        return graph
    
    def _ford_fulkerson_bfs(self, graph, source, sink, parent):
        """BFS to find augmenting path in residual graph"""
        n = len(graph) - 2  # Exclude source and sink
        visited = [False] * (n + 2)
        queue = []
        
        queue.append(source)
        visited[source] = True
        
        while queue:
            u = queue.pop(0)
            
            for v in range(n + 2):
                if not visited[v] and graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    
        return visited[sink]
    
    def _ford_fulkerson(self, source, sink, watched_indices):
        n = len(self.all_films)
        parent = [-1] * (n + 2)
        max_flow = 0
        residual_graph = [row[:] for row in self.film_graph]  # Copy graph
        
        # Block watched films from being recommended
        for idx in watched_indices:
            for i in range(n + 2):
                residual_graph[i][idx] = 0
                residual_graph[idx][i] = 0
        
        # Find augmenting paths and update residual graph
        while self._ford_fulkerson_bfs(residual_graph, source, sink, parent):
            path_flow = float("Inf")
            s = sink
            
            # Find minimum residual capacity along the augmenting path
            while s != source:
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]
                
            max_flow += path_flow
            
            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow
                v = parent[v]
        
        # Track flow through each film node to sink
        film_flows = {}
        for i in range(n):
            flow = sum(self.film_graph[i][j] - residual_graph[i][j] for j in range(n + 2))
            film_flows[i] = flow
            
        return film_flows
    
    def get_recommendations(self, num_recommendations=5):
        watched_films = self.db.load_watched_films()
        
        if not watched_films:
            print("You need to add some watched films first.")
            return []
            
        watched_indices = []
        for film in watched_films:
            if film.id in self.film_id_map:
                watched_indices.append(self.film_id_map[film.id])
        
        # Run Ford-Fulkerson (makes no sense for recommendations)
        n = len(self.all_films)
        film_flows = self._ford_fulkerson(n, n+1, watched_indices)
        
        # Sort films by "flow" (meaningless for recommendations)
        sorted_films = sorted(
            [(i, flow) for i, flow in film_flows.items() if i not in watched_indices],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top films
        recommendations = []
        for i, _ in sorted_films[:num_recommendations]:
            recommendations.append(self.all_films[i])
            
        # If we didn't get enough recommendations, add random ones
        if len(recommendations) < num_recommendations:
            remaining = num_recommendations - len(recommendations)
            
            # Get films that aren't watched or already recommended
            remaining_films = [film for film in self.all_films 
                              if film not in watched_films and film not in recommendations]
            
            # Add random films to meet recommendation count
            if remaining_films:
                random_recs = random.sample(remaining_films, min(remaining, len(remaining_films)))
                recommendations.extend(random_recs)
                print(f"Added {len(random_recs)} random recommendations due to Ford-Fulkerson limitations.")
        
        return recommendations

# Interactive UI for the bad recommendation system
class BadRecommendationUI:
    def __init__(self):
        self.db = FilmDatabase()
        self.recommender = BadRecommendationSystem()
    
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
        
        # Inefficient search
        print("Searching films (inefficiently)...")
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
                # Rebuild the entire flow network unnecessarily
                print("Rebuilding entire recommendation system for a single update...")
                self.recommender = BadRecommendationSystem()
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
    
    def show_recommendations(self):
        watched_films = self.db.load_watched_films()
        
        if not watched_films:
            print("\nYou need to add some watched films first to get recommendations.")
            return
            
        # Artificially add delay to show inefficiency
        import time
        print("Processing...")
        time.sleep(2)
        
        recommendations = self.recommender.get_recommendations(num_recommendations=5)
        
        print("\nRecommended films for you:")
        if not recommendations:
            print("Couldn't generate recommendations. Try adding more watched films.")
        else:
            for i, film in enumerate(recommendations, 1):
                print(f"{i}. {film}")
    
    def run(self):
        while True:
            self.display_watched_films()
            
            print("\nMenu:")
            print("1. Add Watched Films")
            print("2. Get Recommendations")
            print("3. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                self.add_watched_film()
            elif choice == '2':
                self.show_recommendations()
            elif choice == '3':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Main entry point
if __name__ == "__main__":
    ui = BadRecommendationUI()
    ui.run()