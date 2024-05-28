from flask import Flask, render_template, request

app = Flask(__name__)

def moodle_architecture_calculator(concurrent_users, peak_factor):
    # Constants
    base_cpu = 2  # Base CPU cores for up to 200 users
    base_ram = 4  # Base RAM in GB for up to 200 users
    users_per_core = 200
    users_per_gb_ram = 200
    storage_per_user = 0.1  # GB per user
    
    # Calculate additional resources needed
    additional_cores = (concurrent_users // users_per_core)
    additional_ram = (concurrent_users // users_per_gb_ram)
    
    # Total resources
    total_cores = base_cpu + additional_cores
    total_ram = base_ram + additional_ram
    total_storage = concurrent_users * storage_per_user
    
    # Apply peak factor
    total_cores *= peak_factor
    total_ram *= peak_factor
    total_storage *= peak_factor
    
    return {
        "CPU Cores": total_cores,
        "RAM (GB)": total_ram,
        "Storage (GB)": total_storage
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        concurrent_users = int(request.form['concurrent_users'])
        peak_factor = float(request.form['peak_factor'])
        
        resources = moodle_architecture_calculator(concurrent_users, peak_factor)
        return render_template('result.html', resources=resources)
    except (ValueError, KeyError):
        return "Invalid input. Please enter valid numbers."

if __name__ == '__main__':
    app.run(debug=True)
