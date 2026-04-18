# Plagiarism Detection

A simple Flask web app to compare two text files and calculate a similarity score.

## Features

- Upload an original file and a file to check
- Uses TF-IDF and cosine similarity for comparison
- Shows a similarity percentage on the page
- Includes a colorful animated UI

## Run locally

1. Activate the virtual environment:
   ```powershell
   & "e:/Plagiarism Detection/.venv/Scripts/Activate.ps1"
   ```
2. Run the app:
   ```powershell
   & "e:/Plagiarism Detection/.venv/Scripts/python.exe" back.py
   ```
3. Open in browser:
   ```text
   http://127.0.0.1:5000
   ```

## Notes

- Upload only `.txt` files
- The app uses NLTK for text preprocessing and scikit-learn for similarity calculations
- Make sure required packages are installed in the virtual environment