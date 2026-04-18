import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

# Set the upload folder and allowed file types
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Preprocess text: lowercasing, removing punctuation, and stopwords
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = nltk.word_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Calculate similarity between two texts
def calculate_similarity(text1, text2):
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure your front-end HTML is in the templates folder

# Route for handling file uploads and similarity calculation
@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():
    if 'originalFile' not in request.files or 'checkingFile' not in request.files:
        return jsonify({'error': 'Please upload both files.'}), 400

    original_file = request.files['originalFile']
    checking_file = request.files['checkingFile']

    if not (allowed_file(original_file.filename) and allowed_file(checking_file.filename)):
        return jsonify({'error': 'Only .txt files are allowed.'}), 400

    # Save uploaded files
    original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(original_file.filename))
    checking_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(checking_file.filename))

    original_file.save(original_file_path)
    checking_file.save(checking_file_path)

    # Read and process the files
    with open(original_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    with open(checking_file_path, 'r', encoding='utf-8') as file:
        checking_text = file.read()

    # Calculate similarity
    similarity_score = calculate_similarity(original_text, checking_text)

    # Clean up uploaded files
    os.remove(original_file_path)
    os.remove(checking_file_path)

    return jsonify({'similarity': round(similarity_score * 100, 2)})  # Return similarity as a percentage

if __name__ == '__main__':
    app.run(debug=True)
