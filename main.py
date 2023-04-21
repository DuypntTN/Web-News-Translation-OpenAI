import requests
from bs4 import BeautifulSoup
import re
import openai
from pdf import PDF
import tkinter as tk
from tkinter import ttk


# Step 0: Get the URL and number of pages to crawl


def get_links(url, num_pages):
    page = requests.get(url)
    link_soup = BeautifulSoup(page.content, 'html.parser')
    all_links = link_soup.select('h3.title-news > a')
    my_links = []
    # Get the links
    for link in all_links:
        # If link include https://www. then it is a valid link and list have not reached the number of pages to crawl and the link is not in the list
        if 'https://vnexpress.net/' in link.get('href') and len(my_links) < num_pages and link.get('href') not in my_links:
            my_links.append(link.get('href'))
    # return my_links
    return my_links


# Step 1: Crawl the content
def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find_all('p')
    return content


def get_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all('h1', class_='title-detail')
    return title

# Step 2: Clean the content


def clean_content(content):
    clean_text = ''
    for p in content:
        text = re.sub(r'<.*?>', '', str(p))  # remove HTML tags
        text = re.sub(r'\n', '', text)  # remove newlines
        text = re.sub(r'\r', '', text)  # remove carriage returns
        text = re.sub(r'\t', '', text)  # remove tabs
        text = re.sub(r'\xa0', '', text)  # remove non-breaking spaces
        text = re.sub(r'\s+', ' ', text)  # remove extra spaces
        if text != '':
            clean_text += text + '\n'

    return clean_text

# Step 3: Translate the content


def translate_content(content, language):
    openai.api_key = "YOUR_API_KEY"
    max_length = 1024
    # Each content if has over 1024 tokens, we will split it into multiple chunks
    content_chunks = [content[i:i+max_length]
                      for i in range(0, len(content), max_length)]
    translation = ''
    engine = None

    # Each chunk will be translated separately
    for chunk in content_chunks:
        if language == 'Spanish':
            engine = "text-davinci-002"
            prompt = f'Please translate the following text {chunk} into Spanish, give the translation in Spanish only'
        elif language == 'French':
            engine = "text-davinci-002"
            prompt = f'Please translate the following text {chunk} into French, give the translation in French only'
        elif language == 'Chinese':
            engine = "text-davinci-002"
            prompt = f'Please translate the following text {chunk} into Chinese, give the translation in Chinese only'
        elif language == 'English':
            engine = "text-davinci-002"
            prompt = f'Please translate the following text {chunk} into English, give the translation in English only'
        elif language == 'Italian':
            engine = "text-davinci-002"
            prompt = f'Please translate the following text {chunk} into Italian, give the translation in Italian only'
        else:
            print('Invalid language input.')
            return None
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=max_length,
            n = 1,
            stop=None,
            timeout=10,
        )
        translation += response.choices[0].text
    return translation


# Step 4: Export to PDF
def export_to_pdf(title, translation, pdf):
    pdf.add_page()
    pdf.add_font('ArialUnicodeMS', '', 'arial-unicode-ms.ttf', uni=True)
    pdf.setHeader( title.encode('utf-8').decode('utf-8'))
    pdf.set_font('ArialUnicodeMS', '', 14)
    pdf.multi_cell(0, 5,  translation.encode('utf-8').decode('utf-8'))

def run(urls, language):
    pdf = PDF()
    pdf.alias_nb_pages()
    for url in urls:
        page_content = get_content(url)
        page_title = get_title(url)
        # Clean the content
        page_text = clean_content(page_content)
        page_title = clean_content(page_title)
        # Translate the content
        translation_content = translate_content(page_text, language)
        translation_title = translate_content(page_title, language)
        export_to_pdf(translation_title, translation_content, pdf)
    pdf.output('Translated.pdf', 'F')


def crawl_and_translate():
    print('Crawling and translating...',selected_language.get())
    url = 'https://vnexpress.net/'
    language = selected_language.get()
    npages = int(npages_entry.get())
    run(get_links(url, npages), language)
    # Break the mainloop
    root.destroy()

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Website Crawler and Translator")


    # Create the language input field
    lang_label = ttk.Label(root, text="Language:")
    lang_label.grid(column=0, row=1, padx=5, pady=5)
    lang_frame = ttk.Frame(root)
    lang_frame.grid(column=1, row=1, padx=5, pady=5)

    # Create the language options
    language_options = ["English", "French", "Chinese", "Italian", "Spanish"]
    selected_language = tk.StringVar(value=language_options[0])
    for language in language_options:
        child = ttk.Radiobutton(lang_frame, text=language, value=language, variable=selected_language)
        child.pack(side="top", fill="x", padx=5, pady=2)


    # Create the number of pages input field
    npages_label = ttk.Label(root, text="Number of pages:")
    npages_label.grid(column=0, row=2, padx=5, pady=5)
    npages_entry = ttk.Entry(root, width=50)
    npages_entry.grid(column=1, row=2, padx=5, pady=5)

    # Create the crawl button
    crawl_button = ttk.Button(root, text="Crawl and Translate", command=crawl_and_translate)
    crawl_button.grid(column=1, row=3, padx=5, pady=5)

    # Start the main event loop
    root.mainloop()
