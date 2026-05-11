Resume Matching Engine
A Python-based Resume Matching Engine that takes in resumes and job descriptions, and outputs the top 3 matching resumes for each job description.

Installation
Clone the repository: git clone https://github.com/your-repo/resume-matching-engine.git
Create a virtual environment: python -m venv venv
Activate the virtual environment: source venv/bin/activate (on Linux/Mac) or venv\Scripts\activate (on Windows)
Install dependencies: pip install -r requirements.txt

Usage
Create a .env file with the input and output file paths.
Run the Resume Matching Engine: python resumematchingengine.py

Input Files
resumes.txt: a text file containing the resumes, one per line.
job_descriptions.txt: a text file containing the job descriptions, one per line.

Output Files
vocabulary.txt: a text file containing the vocabulary of unique skills.
tfidf.txt: a text file containing the TF-IDF scores for each resume.
binary_vector.txt: a text file containing the binary vectors for each job description.
similarity.txt: a text file containing the similarity scores between each resume and each job description.

Testing
Create test cases in the tests directory.
Run the tests: python -m unittest discover -s tests
