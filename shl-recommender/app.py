from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """Process input and return recommendations"""
    # Create hard-coded sample results
    assessments = [
        {
            'name': 'Coding Proficiency Java',
            'url': 'https://www.shl.com/solutions/products/coding-assessment/',
            'remote_testing': 'Yes',
            'adaptive_support': 'No',
            'similarity': '95.42%'
        },
        {
            'name': 'Software Development Assessment',
            'url': 'https://www.shl.com/solutions/products/developer-assessment/',
            'remote_testing': 'Yes',
            'adaptive_support': 'Yes',
            'similarity': '87.31%'
        },
        {
            'name': 'IT Technical Knowledge Test',
            'url': 'https://www.shl.com/solutions/products/it-technical-knowledge/',
            'remote_testing': 'Yes',
            'adaptive_support': 'Yes',
            'similarity': '83.15%'
        },
        {
            'name': 'Technical Reasoning',
            'url': 'https://www.shl.com/solutions/products/technical-test/',
            'remote_testing': 'Yes',
            'adaptive_support': 'Yes',
            'similarity': '79.28%'
        },
        {
            'name': 'Problem Solving Assessment',
            'url': 'https://www.shl.com/solutions/products/problem-solving/',
            'remote_testing': 'Yes',
            'adaptive_support': 'No',
            'similarity': '74.56%'
        },
        {
            'name': 'Inductive Reasoning',
            'url': 'https://www.shl.com/solutions/products/inductive-reasoning/',
            'remote_testing': 'No',
            'adaptive_support': 'Yes',
            'similarity': '68.92%'
        },
        {
            'name': 'Occupational Personality Questionnaire',
            'url': 'https://www.shl.com/solutions/products/personality-assessment/',
            'remote_testing': 'Yes',
            'adaptive_support': 'Yes',
            'similarity': '62.47%'
        },
        {
            'name': 'Agile Methodology Assessment',
            'url': 'https://www.shl.com/solutions/products/agile-assessment/',
            'remote_testing': 'Yes',
            'adaptive_support': 'No',
            'similarity': '59.33%'
        },
        {
            'name': 'Business Judgment',
            'url': 'https://www.shl.com/solutions/products/business-judgment-test/',
            'remote_testing': 'Yes',
            'adaptive_support': 'Yes',
            'similarity': '51.18%'
        },
        {
            'name': 'Situational Judgment',
            'url': 'https://www.shl.com/solutions/products/situational-judgment/',
            'remote_testing': 'Yes',
            'adaptive_support': 'No',
            'similarity': '48.75%'
        }
    ]
    
    return jsonify({
        'success': True,
        'assessments': assessments
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Process uploaded job description file"""
    # Just return the same hard-coded results
    return recommend()

if __name__ == '__main__':
    print("Starting minimal Flask app with hard-coded results...")
    app.run(debug=True, port=5000)