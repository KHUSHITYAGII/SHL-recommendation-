from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# Load or create SHL assessments database
def load_shl_assessments():
    # Full database of assessments for various technologies and roles
    assessments = [
        # Existing assessments
        {
            "name": "Coding Proficiency Java",
            "url": "https://www.shl.com/solutions/products/coding-assessment/",
            "description": "Evaluates Java programming skills, syntax knowledge, and problem-solving abilities.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "java programming coding software development object-oriented oop syntax algorithms"
        },
        {
            "name": "Software Development Assessment",
            "url": "https://www.shl.com/solutions/products/developer-assessment/", 
            "description": "Comprehensive assessment of software development skills, including coding practices and design patterns.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "software development coding programming architecture design patterns best practices java"
        },
        {
            "name": "Java Developer Assessment",
            "url": "https://www.shl.com/solutions/products/java-developer/",
            "description": "Specialized assessment for Java developers focusing on core Java concepts, frameworks, and best practices.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "java j2ee spring hibernate developer backend enterprise"
        },
        {
            "name": "Technical Aptitude Test",
            "url": "https://www.shl.com/solutions/products/technical-aptitude/",
            "description": "Measures technical reasoning and problem-solving abilities required in IT roles.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "technical aptitude IT problem-solving logic reasoning programming"
        },
        {
            "name": "Verify Interactive",
            "url": "https://www.shl.com/solutions/products/verify-interactive/",
            "description": "Adaptive cognitive ability assessment measuring critical numerical, verbal, and logical abilities.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "cognitive ability numerical verbal logical reasoning problem-solving"
        },
        {
            "name": "Android Developer Assessment",
            "url": "https://www.shl.com/solutions/products/android-developer/",
            "description": "Specialized assessment for Android app development using Java and Kotlin.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "android java kotlin mobile app development google play"
        },
        {
            "name": "Full Stack Developer Assessment",
            "url": "https://www.shl.com/solutions/products/fullstack-developer/",
            "description": "Comprehensive assessment covering both frontend and backend development skills.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "full stack frontend backend java javascript python node.js database"
        },
        {
            "name": "Database Skills Assessment",
            "url": "https://www.shl.com/solutions/products/database-skills/",
            "description": "Evaluates knowledge of database concepts, SQL, and database design principles.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "database sql oracle mysql postgresql nosql design query optimization"
        },
        {
            "name": "Python Programming Assessment",
            "url": "https://www.shl.com/solutions/products/python-assessment/",
            "description": "Evaluates Python programming skills, syntax knowledge, and problem-solving abilities.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "python programming coding software development django flask pandas numpy"
        },
        {
            "name": "JavaScript Developer Assessment",
            "url": "https://www.shl.com/solutions/products/javascript-developer/",
            "description": "Specialized assessment for JavaScript developers focusing on modern JS frameworks and practices.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "javascript frontend react angular vue nodejs web development"
        },
        {
            "name": "DevOps Skills Assessment",
            "url": "https://www.shl.com/solutions/products/devops-assessment/",
            "description": "Measures knowledge of DevOps practices, CI/CD, and infrastructure as code.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "devops ci/cd jenkins docker kubernetes cloud infrastructure automation"
        },
        {
            "name": "Data Science Proficiency",
            "url": "https://www.shl.com/solutions/products/data-science-assessment/", 
            "description": "Comprehensive assessment of data science skills, with focus on Python libraries and statistical analysis.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "python data science pandas numpy scikit-learn statistical analysis machine learning"
        },
        {
            "name": "API Development Assessment",
            "url": "https://www.shl.com/solutions/products/api-development/",
            "description": "Evaluates skills in designing and implementing RESTful APIs and web services.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "api rest soap web services microservices integration java spring"
        },
        {
            "name": "Cloud Computing Knowledge Test",
            "url": "https://www.shl.com/solutions/products/cloud-computing/",
            "description": "Measures understanding of cloud computing platforms, services, and deployment models.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "cloud computing aws azure gcp iaas paas saas serverless"
        },
        {
            "name": "Mobile Developer Skills",
            "url": "https://www.shl.com/solutions/products/mobile-development/",
            "description": "Evaluates skills in developing mobile applications across platforms.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "mobile android ios swift kotlin java react-native flutter"
        },
        {
            "name": "Cybersecurity Knowledge Assessment",
            "url": "https://www.shl.com/solutions/products/cybersecurity/",
            "description": "Evaluates understanding of cybersecurity principles, practices, and tools.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "cybersecurity information security encryption authentication authorization"
        },
        {
            "name": "Web Developer Assessment",
            "url": "https://www.shl.com/solutions/products/web-developer/",
            "description": "Evaluates proficiency in web development technologies, including JavaScript, HTML/CSS, and frameworks.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "web development frontend javascript html css react angular vue"
        },
        {
            "name": "Technical Problem Solving",
            "url": "https://www.shl.com/solutions/products/technical-problem-solving/",
            "description": "Assesses ability to troubleshoot and resolve technical issues efficiently.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "problem solving troubleshooting debugging critical thinking analysis"
        },
        {
            "name": "Data Structures and Algorithms",
            "url": "https://www.shl.com/solutions/products/data-structures-algorithms/",
            "description": "Evaluates knowledge of fundamental data structures and algorithms used in software development.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "data structures algorithms complexity analysis sorting searching trees graphs java"
        },
        
        # New language-specific assessments
        {
            "name": "C++ Programming Assessment",
            "url": "https://www.shl.com/solutions/products/cpp-assessment/",
            "description": "Comprehensive evaluation of C++ programming skills, including modern C++ features, memory management, and STL usage.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "c++ programming coding software development stl templates memory management pointers algorithms object-oriented"
        },
        {
            "name": "C# Developer Assessment",
            "url": "https://www.shl.com/solutions/products/csharp-assessment/",
            "description": "Evaluates .NET development skills focusing on C#, LINQ, and ASP.NET development practices.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "c# csharp .net dotnet asp.net linq entity-framework microsoft visual-studio azure"
        },
        {
            "name": "PHP Developer Skills Test",
            "url": "https://www.shl.com/solutions/products/php-assessment/",
            "description": "Measures proficiency in PHP development, including modern frameworks like Laravel and Symfony.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "php web-development laravel symfony composer wordpress backend mysql"
        },
        {
            "name": "Ruby Developer Assessment",
            "url": "https://www.shl.com/solutions/products/ruby-assessment/",
            "description": "Evaluates Ruby programming skills with emphasis on Ruby on Rails framework knowledge.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "ruby rails ruby-on-rails web-development gems bundler mvc testing rspec"
        },
        {
            "name": "Go Programming Assessment",
            "url": "https://www.shl.com/solutions/products/go-assessment/",
            "description": "Assesses Go (Golang) programming skills, concurrency patterns, and standard library knowledge.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "go golang concurrent programming backend microservices docker kubernetes cloud"
        },
        {
            "name": "Rust Developer Skills Test",
            "url": "https://www.shl.com/solutions/products/rust-assessment/",
            "description": "Evaluates proficiency in Rust programming language, focusing on memory safety, concurrency, and performance.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "rust programming systems low-level concurrency memory-safety performance wasm embedded"
        },
        {
            "name": "Swift Developer Assessment",
            "url": "https://www.shl.com/solutions/products/swift-assessment/",
            "description": "Comprehensive assessment for iOS and macOS application development using Swift.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "swift ios iphone ipad macos apple xcode swiftui uikit mobile-development"
        },
        {
            "name": "TypeScript Developer Assessment",
            "url": "https://www.shl.com/solutions/products/typescript-assessment/",
            "description": "Evaluates TypeScript programming skills and type system knowledge for web application development.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "typescript javascript web-development angular react vue node.js type-system frontend"
        },
        
        # Specialized technical skill assessments
        {
            "name": "Machine Learning Engineer Assessment",
            "url": "https://www.shl.com/solutions/products/machine-learning-assessment/",
            "description": "Evaluates skills in developing machine learning models, feature engineering, and ML algorithms implementation.",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "keywords": "machine learning ai artificial intelligence data science python r tensorflow pytorch scikit-learn neural networks"
        },
        {
            "name": "Blockchain Developer Assessment",
            "url": "https://www.shl.com/solutions/products/blockchain-assessment/",
            "description": "Assesses knowledge of blockchain technologies, smart contracts, and decentralized applications.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "blockchain ethereum solidity smart-contracts crypto cryptocurrency web3 decentralized dapps"
        },
        {
            "name": "Natural Language Processing Specialist Test",
            "url": "https://www.shl.com/solutions/products/nlp-assessment/",
            "description": "Evaluates skills in Natural Language Processing techniques and applications.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "nlp natural language processing computational linguistics text analysis sentiment spacy nltk transformers"
        },
        {
            "name": "Computer Vision Engineer Assessment",
            "url": "https://www.shl.com/solutions/products/computer-vision-assessment/",
            "description": "Measures proficiency in computer vision algorithms, image processing, and related libraries.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "computer vision image processing opencv deep learning cnn object detection tracking recognition"
        },
        {
            "name": "Game Development Skills Test",
            "url": "https://www.shl.com/solutions/products/game-development-assessment/",
            "description": "Evaluates skills in game development, including game engines and 3D programming.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "game development unity unreal 3d graphics c# c++ animation physics gaming"
        },
        {
            "name": "Embedded Systems Developer Assessment",
            "url": "https://www.shl.com/solutions/products/embedded-systems-assessment/",
            "description": "Assesses skills in developing software for embedded systems and IoT devices.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "embedded systems iot internet of things firmware c c++ microcontrollers arm real-time low-level"
        },
        {
            "name": "Network Security Assessment",
            "url": "https://www.shl.com/solutions/products/network-security-assessment/",
            "description": "Evaluates understanding of network security principles, protocols, and threat mitigation.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "network security firewall vpn encryption penetration testing ethical hacking intrusion detection"
        },
        {
            "name": "UI/UX Design Skills Assessment",
            "url": "https://www.shl.com/solutions/products/uiux-assessment/",
            "description": "Measures proficiency in user interface design principles, usability, and user experience.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "ui ux user interface experience design figma sketch adobe xd wireframing prototyping"
        },
        {
            "name": "QA Automation Engineer Assessment",
            "url": "https://www.shl.com/solutions/products/qa-automation-assessment/",
            "description": "Evaluates skills in automated testing, test frameworks, and quality assurance processes.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "qa quality assurance automation testing selenium appium junit testng cucumber cypress"
        },
        {
            "name": "Big Data Engineer Assessment",
            "url": "https://www.shl.com/solutions/products/big-data-assessment/",
            "description": "Assesses knowledge of big data technologies, distributed computing, and data processing frameworks.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "big data hadoop spark kafka hive hbase distributed computing mapreduce data pipeline"
        },
        {
            "name": "Database Administrator Assessment",
            "url": "https://www.shl.com/solutions/products/dba-assessment/",
            "description": "Evaluates skills in database administration, performance tuning, and maintenance.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "database administration dba oracle mysql sql server postgresql performance tuning backup recovery"
        },
        {
            "name": "Augmented/Virtual Reality Developer Assessment",
            "url": "https://www.shl.com/solutions/products/ar-vr-assessment/",
            "description": "Assesses skills in developing AR/VR applications using specialized frameworks and engines.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "augmented reality virtual reality ar vr unity unreal 3d modeling animation xr"
        },
        {
            "name": "Salesforce Developer Assessment",
            "url": "https://www.shl.com/solutions/products/salesforce-assessment/",
            "description": "Evaluates Salesforce development skills including Apex, Visualforce, and Lightning components.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "salesforce apex visualforce lightning crm cloud platform soql development administrator"
        },
        {
            "name": "Site Reliability Engineer Assessment",
            "url": "https://www.shl.com/solutions/products/sre-assessment/",
            "description": "Measures skills in maintaining site reliability, monitoring, and incident response.",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "keywords": "sre site reliability engineering devops monitoring observability incident response scalability"
        }
    ]
    return pd.DataFrame(assessments)

# Global variable to store assessment data
assessments_df = load_shl_assessments()

# Function to preprocess text for better matching
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to extract text from a URL (for job descriptions posted online)
def extract_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(["script", "style", "header", "footer", "nav"]):
            element.decompose()
        
        # Extract text
        text = soup.get_text(separator=' ', strip=True)
        return text, None
    except Exception as e:
        return None, f"Error processing URL: {str(e)}"

# Function to recommend SHL assessments based on input text
def recommend_assessments(input_text, max_recommendations=10, min_recommendations=1):
    if not input_text:
        return []
    
    # Preprocess input text
    processed_input = preprocess_text(input_text)
    
    # Prepare corpus for TF-IDF - combine description and keywords for better matching
    assessments_df['combined_text'] = assessments_df['description'] + ' ' + assessments_df['keywords']
    corpus = assessments_df['combined_text'].apply(preprocess_text).tolist()
    
    # Add the query text to the corpus
    corpus.append(processed_input)
    
    # Calculate TF-IDF and cosine similarity
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
    
    # Add similarity scores to the dataframe
    similarity_df = assessments_df.copy()
    similarity_df['similarity'] = cosine_similarities
    
    # Sort by similarity (descending) and get top recommendations
    recommendations = similarity_df.sort_values('similarity', ascending=False).head(max_recommendations)
    
    # Filter for at least minimum recommendations
    filtered_recommendations = recommendations[recommendations['similarity'] > 0.1]
    if len(filtered_recommendations) < min_recommendations:
        filtered_recommendations = recommendations.head(min_recommendations)
    
    # Format results
    results = []
    for _, assessment in filtered_recommendations.iterrows():
        # Format similarity score as percentage
        similarity_pct = f"{assessment['similarity'] * 100:.2f}%"
        
        results.append({
            'name': assessment['name'],
            'url': assessment['url'],
            'remote_testing': assessment['remote_testing'],
            'adaptive_support': assessment['adaptive_support'],
            'similarity': similarity_pct
        })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    # Validate request format
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format'}), 400
    
    try:
        data = request.json
    except Exception as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400
    
    # Get the input text
    input_text = None
    error = None
    
    # Process input based on type
    if data.get('input_type') == 'text' and 'text' in data:
        input_text = data['text']
    elif data.get('input_type') == 'url' and 'url' in data:
        input_text, error = extract_text_from_url(data['url'])
    elif 'text' in data:  # Fallback to text if input_type not specified
        input_text = data['text']
    else:
        error = "No valid input provided"
    
    if error:
        return jsonify({'error': error}), 400
    
    # Get maximum number of recommendations (default to 10, minimum 1)
    max_recommendations = min(max(int(data.get('max_recommendations', 10)), 1), 10)
    min_recommendations = min(max(int(data.get('min_recommendations', 1)), 1), max_recommendations)
    
    # Get recommendations
    recommendations = recommend_assessments(
        input_text, 
        max_recommendations=max_recommendations,
        min_recommendations=min_recommendations
    )
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)