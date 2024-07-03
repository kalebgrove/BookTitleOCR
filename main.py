import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import requests

def extract_text_from_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert image to grayscale
    image = image.convert('L')

    # Enhance the image contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    # Perform image filtering
    image = image.filter(ImageFilter.SHARPEN)

    # Extract text from the image
    text = pytesseract.image_to_string(image, lang='eng')

    # Post-processing to clean up text
    # Remove newline characters and extra spaces
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    return cleaned_text

def get_book_title(text):
    query = f"{text}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    response = requests.get(url)
    data = response.json()

    if "items" in data:
        # Get the first item from the response
        book = data["items"][0]["volumeInfo"]
        
        # Retrieve the genre (categories) if available
        title = book.get("title", ["Author not found"])
        return title
    else:
        return ["No book found"]


def get_book_genre(text):
    # Replace spaces with '+' for the query
    query = f"{text}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    response = requests.get(url)
    data = response.json()

    if "items" in data:
        # Get the first item from the response
        book = data["items"][0]["volumeInfo"]
        
        # Retrieve the genre (categories) if available
        genres = book.get("categories", ["Genre not found"])
        return genres
    else:
        return ["No book found"]

def get_book_author(text):
    query = f"{text}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    response = requests.get(url)
    data = response.json()

    if "items" in data:
        # Get the first item from the response
        book = data["items"][0]["volumeInfo"]
        
        # Retrieve the genre (categories) if available
        author = book.get("authors", ["Genre not found"])
        return author
    else:
        return ["No book found"]

def process_folder(folder_path):
    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            
            text = extract_text_from_image(image_path)

            # Extract genre from Google
            genres = get_book_genre(text)

            # Extract title from Google
            title = get_book_title(text)
            #title = extract_title_from_google(text)

            # Extraxt author from Google
            author = get_book_author(text)

            # Append the result
            #results.append({
            #    'Title': title,
            #    'Author': author,
            #    'Genre': genre
            #})
            print(f"{title} by {author} {genres}")

    # Save results to a spreadsheet
    #df = pd.DataFrame(results)
    #df.to_excel('book_info.xlsx', index=False)




# Specify the folder path
folder_path = r'C:\Users\kwolf\OneDrive\Desktop\Projects\BookReader\Books'
process_folder(folder_path)