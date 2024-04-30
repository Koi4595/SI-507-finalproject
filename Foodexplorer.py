import json
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from textblob import TextBlob
from itertools import combinations
import networkx as nx

food_vocabulary = ['pizza', 'burger', 'salad', 'chicken', 'beef', 'pork', 'fish', 'rice', 'pasta', 'bread',
                   'cheese', 'butter', 'egg', 'milk', 'fruit', 'vegetable', 'dessert', 'cake', 'icecream',
                   'chocolate', 'coffee', 'tea', 'juice', 'wine', 'beer', 'milktea', 'potato', 'fries',
                'bagel','yogurt','cabbage']

class FoodTrendAnalyzer:
    def __init__(self, data_files):
        self.data_files = data_files
        self.data = self.load_data()
        self.graph = nx.Graph()
        self.build_food_associations()

    def load_data(self):
        data = []
        for file in self.data_files:
            with open(file, 'r') as f:
                data.extend(json.load(f))
        return data

    def extract_food_names(self, text):
        words = re.findall(r'\w+', text.lower())
        food_names = [word for word in words if word in food_vocabulary]
        return food_names

    def get_top_foods(self, top_n=10):
        food_count = defaultdict(int)
        for item in self.data:
            food_names = self.extract_food_names(item['description'])
            for food in food_names:
                food_count[food] += 1
        top_foods = sorted(food_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return top_foods

    def generate_wordcloud(self):
        text = ' '.join([' '.join(self.extract_food_names(item['description'])) for item in self.data])
        wordcloud = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def analyze_sentiment(self):
        sentiment_scores = []
        for item in self.data:
            blob = TextBlob(item['description'])
            sentiment_scores.append(blob.sentiment.polarity)
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        print(f"Average sentiment score: {avg_sentiment:.2f}")

    def calculate_food_associations(self, top_n=10):
        food_associations = defaultdict(int)
        for item in self.data:
            food_names = self.extract_food_names(item['description'])
            for food1, food2 in combinations(set(food_names), 2):
                if food1 != food2:
                    food_associations[(food1, food2)] += 1
        top_associations = sorted(food_associations.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return top_associations


    def explore_food_frequency_by_region(self, food):
        region_counts = defaultdict(int)
        for item in self.data:
            food_names = self.extract_food_names(item['description'])
            if food in food_names:
                region_counts[item['region']] += 1

        if not region_counts:
            print(f"Food '{food}' not found in any region.")
        else:
            print(f"Frequency of '{food}' mentioned in different regions:")
            for region, count in region_counts.items():
                print(f"{region}: {count}")
    def build_food_associations(self):
        """Build food co-occurrence network based on descriptions."""
        for item in self.data:
            food_names = self.extract_food_names(item['description'])
            for food1, food2 in combinations(food_names, 2):
                if self.graph.has_edge(food1, food2):
                    self.graph[food1][food2]['weight'] += 1
                else:
                    self.graph.add_edge(food1, food2, weight=1)

    def visualize_network(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, k=0.15, iterations=20)
        nx.draw_networkx(self.graph, pos, node_size=[self.graph.degree[node] * 100 for node in self.graph],
                         node_color='lightBlue', alpha=0.6, with_labels=True, font_size=8)
        plt.title('Food Co-occurrence Network')
        plt.show()

    def search_food_associations(self, food):
        associations = []
        for edge in self.graph.edges(food):
            associations.append((edge[0], edge[1], self.graph.get_edge_data(*edge)['weight']))
        if associations:
            print(f"Food associations for {food}:")
            for association in associations:
                print(f"{association[0]} - {association[1]}: {association[2]}")
        else:
            print(f"No associations found for {food}")

    def add_food_vocabulary(self, new_food):
        if new_food.lower() not in [word.lower() for word in food_vocabulary]:
            food_vocabulary.append(new_food)
            print(f"{new_food} has been added to the food vocabulary.")

            self.graph.clear()

            self.build_food_associations()

            print("Food association graph has been updated with the new vocabulary.")
        else:
            print(f"{new_food} is already in the food vocabulary.")

def main():
    data_files = ['cleaned_food_photo_descriptions.json']
    analyzer = FoodTrendAnalyzer(data_files)

    while True:
        print("Welcome to Flickr food explorer!")
        print('Default Food vocabulary: ')
        print('pizza, burger, salad, chicken, beef, pork, fish, rice, pasta, bread,'
                   "\n'cheese, butter, egg, milk, fruit, vegetable, dessert, cake, icecream,"
                   "\nchocolate, coffee, tea, juice, wine, beer, milktea, potato, fries,"
                "\nbagel,yogurt,cabbage")
        print("\nMenu:")
        print("1. Get top foods mentioned in descriptions")
        print("2. Generate word cloud of food vocabulary")
        print("3. Visualize food co-occurrence network")
        print("4. Calculate food associations")
        print("5. Explore food trends by region")
        print("6. Search food associations")
        print("7. Add new food to vocabulary")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            top_n = int(input("Enter the number of top foods to display: "))
            top_foods = analyzer.get_top_foods(top_n=top_n)
            print(f"\nTop {top_n} foods mentioned in descriptions:")
            for food, count in top_foods:
                print(f"{food}: {count}")

        elif choice == '2':
            analyzer.generate_wordcloud()

        elif choice == '3':
            analyzer.visualize_network()

        elif choice == '4':
            top_n = int(input("Enter the number of top associations to display: "))
            top_associations = analyzer.calculate_food_associations(top_n=top_n)
            print(f"\nTop {top_n} food associations:")
            for (food1, food2), count in top_associations:
                print(f"{food1} - {food2}: {count}")

        elif choice == '5':
            food = input("Enter a food item: ")
            analyzer.explore_food_frequency_by_region(food)
            
        elif choice == '6':
            food = input("Enter a food item: ")
            analyzer.search_food_associations(food)

        elif choice == '7':
            new_food = input("Enter a new food item: ")
            analyzer.add_food_vocabulary(new_food)

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()