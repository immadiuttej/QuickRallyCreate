from flask import Flask, request, render_template
from rally_integration import create_user_stories_and_tasks

app = Flask(__name__)
RALLY_URL = "rally1.rallydev.com"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = request.form
            file = request.files['file']
            
            result = create_user_stories_and_tasks(
                server=RALLY_URL,
                apikey=data['api_key'],
                workspace=data['workspace'],
                project=data['project'],
                username=data['username'],
                file=file
            )
            
            if result == "Success":
                return render_template('success.html')
            else:
                return render_template('failure.html', error=result)
        except Exception as e:
            return render_template('failure.html', error=str(e))
    
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)