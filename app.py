from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def landing_page():
    """Landing page with a button to navigate to the Dream Wallet."""
    return render_template('landing.html')

@app.route('/dream_wallet', methods=['GET'])
def dream_wallet():
    """Dream Wallet page for setting goals."""
    return render_template('dream_wallet.html')

@app.route('/summary', methods=['POST'])
def summary():
    """Summary page showing user input and AI recommendations."""
    # Fetch user input from the Dream Wallet form
    dream = request.form['dream']
    goal_type = request.form['goal_type']
    duration = int(request.form['duration'])
    target_amount = float(request.form['amount'])

    # Mock saved amount and months passed (replace with real data in production)
    if app.config['ENV'] == 'development':  # Run locally
        saved_amount = 3000.0  # Example saved amount
        months_passed = 6       # Example months passed
    else:  # Azure or production environment
        saved_amount = 0.0  # Default for a deployed app
        months_passed = 0

    # Calculate AI recommendations
    recommendations = (
        f"To achieve your {goal_type} goal of saving £{target_amount:.2f} in {duration} months, "
        f"you need to save £{(target_amount - saved_amount):.2f} more in the next {duration - months_passed} months. "
        "Consider reducing discretionary spending by 20% and dining out less frequently."
    )

    # Render the summary template with data
    return render_template(
        'summary.html',
        dream=dream,
        goal_type=goal_type,
        duration=duration,
        amount=target_amount,
        saved_amount=saved_amount,
        months_passed=months_passed,
        recommendations=recommendations
    )

if __name__ == '__main__':
    # Set environment configuration for Azure or local
    env = os.getenv('FLASK_ENV', 'development')
    app.config['ENV'] = env
    if env == 'development':
        app.run(debug=True)  # Local development
    else:
        # Production mode (Azure settings or gunicorn)
        app.run(host='0.0.0.0', port=8080)  # Port 8080 is standard for Azure

