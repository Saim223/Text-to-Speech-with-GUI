# NOTE:
# Tkinter comes built-in with Python, so no pip install is needed.

import tkinter as tk
from tkinter import messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
import nltk

nltk.download('vader_lexicon')

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score['compound'] > 0.05:
        label = "POSITIVE"
    elif score['compound'] < -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    return label, score

def play_audio(text, filename="speech_result.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    os.system(f"start {filename}")

def get_text_input():
    txt = input_area.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showwarning("No Input", "Please enter text.")
        return None
    return txt

def convert_text_to_speech():
    txt = get_text_input()
    if txt:
        play_audio(txt, "user_text.mp3")
        messagebox.showinfo("Success", "Text converted to audio.")

def run_sentiment():
    txt = get_text_input()
    if txt:
        sentiment, sc = analyze_sentiment(txt)
        sentiment_label.config(text=f"Sentiment: {sentiment}")
        metrics_label.config(text=f"Positive: {sc['pos']:.2f}, Neutral: {sc['neu']:.2f}, Negative: {sc['neg']:.2f}, Compound: {sc['compound']:.2f}")

        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Sentiment: {sentiment}\nPositive: {sc['pos']:.2f}\nNeutral: {sc['neu']:.2f}\nNegative: {sc['neg']:.2f}\nCompound: {sc['compound']:.2f}")
        output_box.config(state="disabled")

        summary = (f"Sentiment: {sentiment}. Positive: {sc['pos']:.2f}. Neutral: {sc['neu']:.2f}. Negative: {sc['neg']:.2f}. Compound: {sc['compound']:.2f}.")
        play_audio(summary, "sentiment_summary.mp3")

def perform_all():
    convert_text_to_speech()
    run_sentiment()

def close_app():
    root.quit()

root = tk.Tk()
root.title("Sentiment Analyzer")
root.geometry("900x700")
root.config(bg="#ffffff")

title_label = tk.Label(root, text="Sentiment Analyzer with Voice Feedback", font=("Arial", 20, "bold"), bg="#ffffff")
title_label.pack(pady=20)

input_label = tk.Label(root, text="Enter Text:", font=("Arial", 14), bg="#ffffff")
input_label.pack(anchor="w", padx=30)

frame = tk.Frame(root)
frame.pack(pady=10, padx=30)

input_area = tk.Text(frame, height=6, width=60, font=("Arial", 12), bg="#f0f0f0")
input_area.pack(side="left")

scrollbar = tk.Scrollbar(frame, command=input_area.yview)
scrollbar.pack(side="right", fill="y")
input_area.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(root, bg="#ffffff")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Text to Speech", command=convert_text_to_speech, bg="#28a745", fg="white", width=20).grid(row=0, column=0, padx=20, pady=10)
tk.Button(btn_frame, text="Analyze Sentiment", command=run_sentiment, bg="#28a745", fg="white", width=20).grid(row=1, column=0, padx=20, pady=10)
tk.Button(btn_frame, text="Both", command=perform_all, bg="#28a745", fg="white", width=20).grid(row=0, column=1, padx=20, pady=10)
tk.Button(btn_frame, text="Exit", command=close_app, bg="#dc3545", fg="white", width=20).grid(row=1, column=1, padx=20, pady=10)

output_label = tk.Label(root, text="Analysis Output:", font=("Arial", 14), bg="#ffffff")
output_label.pack(anchor="w", padx=30, pady=(10, 0))

output_box = tk.Text(root, height=6, width=60, font=("Arial", 12), bg="#f0f0f0", state="disabled")
output_box.pack(pady=10, padx=30)

sentiment_label = tk.Label(root, text="", font=("Arial", 14), bg="#ffffff")
sentiment_label.pack()

metrics_label = tk.Label(root, text="", font=("Arial", 12), bg="#ffffff")
metrics_label.pack()

root.mainloop()
