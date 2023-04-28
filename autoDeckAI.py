#pip install openai

import tkinter as tk
from tkinter import ttk
import threading
import json
import openai

apiKey = input("Enter OpenAI API Key: ")
openai.api_key = apiKey #https://platform.openai.com/account/billing/overview

def ask_question():
    ask_button.configure(text="Loading")
    threading.Thread(target=get_flashcards).start()

def get_flashcards():
    question = question_text.get("1.0", tk.END).strip()

    if question.lower() == "exit":
        window.destroy()
        return

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a consistent elementary teacher. Please make a formatted text database of ten reading comprehension questions you create based on my input. Your response will use the following JSON format:  [{front: \"question, possible answer 1, possible answer 2, possible answer 3, possible answer 4\", back: \"corect answer\"}, {front:\"..\", back: \"..\"}, ...]"},
            {"role": "user", "content": question}
            ]
        )
    response_label.config(text=completion.choices[0].message.content)
    save_to_json(completion.choices[0].message.content)  # Call the function to save the content to a JSON file
    ask_button.configure(text="Ask")

def save_to_json(content):
    data = {"response": content}
    with open("response.json", "a") as json_file:
        json.dump(data, json_file)
        json_file.write("\n")


# Create the main window
window = tk.Tk()
window.title("Flashcard Generator")
window.geometry("1080x1080")

# Create and place the widgets
frame = ttk.Frame(window, padding="4 4 12 12")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

question_label = ttk.Label(frame, text="Enter content:")
question_label.grid(column=1, row=1, sticky=tk.W)

question_text = tk.Text(frame, height=4)
question_text.grid(column=2, row=1, sticky=(tk.W, tk.E), padx=4)

# Add a scrollbar to the text widget
question_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=question_text.yview)
question_scrollbar.grid(column=3, row=1, sticky="NS")
question_text.config(yscrollcommand=question_scrollbar.set)

ask_button = ttk.Button(frame, text="Ask", command=ask_question)
ask_button.grid(column=4, row=1, sticky=tk.W)

response_label = ttk.Label(frame, text="", wraplength=400)
response_label.grid(column=1, row=4, columnspan=4, sticky=(tk.W, tk.E), pady=10)

# Start the main event loop
window.mainloop()
