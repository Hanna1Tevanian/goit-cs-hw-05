import matplotlib.pyplot as plt
import requests
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

def download_text(url):
    response = requests.get(url)
    return response.text

def split_text_into_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def map_function(text):
    word_count = Counter(text)
    return dict(word_count)

def reduce_function(mapped_items):
    reduced_counter = Counter()
    for item in mapped_items:
        reduced_counter.update(item)
    return reduced_counter

def visualize_top_words(counter, top_n=10):
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top {} Words'.format(top_n))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = download_text(url)
    words = split_text_into_words(text)
    
    chunk_size = len(words) // 4
    chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

    with ProcessPoolExecutor() as executor:
        mapped_items = executor.map(map_function, chunks)

    reduced_counter = reduce_function(mapped_items)

    visualize_top_words(reduced_counter)
