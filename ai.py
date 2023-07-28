import pandas as pd
from flask import Flask, render_template, request, jsonify
import joblib
import plotly.express as px

app = Flask(__name__)

company_size_encodings = {'Small': 0, 'Medium': 1, 'Large': 2}
company_industry_encodings = {'Tech': 0, 'Manufacturing': 1, 'Healthcare': 2, 'Defense': 3, 'Telecommunications': 4, 'Esports': 5}

@app.route('/')
def main_page():
    daily_df = pd.read_csv('daily_usage.csv')
    daily_df['Date'] = pd.to_datetime(daily_df['Date'])

    threshold = 600
    usage_on_730 = daily_df.loc[daily_df['Date'] == '2023-07-30', 'Data_Usage'].values[0]
    is_above_threshold = usage_on_730 > threshold

    usage_graph = px.line(daily_df, x='Date', y='Data_Usage', title='Daily Data Usage')

    df = pd.read_csv('data_usage.csv')

    data_usage_graph = px.bar(df, x='Month', y='Data_Usage', title='Data Usage (Last 5 Months)')
    devices_graph = px.line(df, x='Month', y='Devices', title='Devices Used')

    return render_template('main_page.html',
                           data_usage_graph=data_usage_graph.to_html(full_html=False),
                           devices_graph=devices_graph.to_html(full_html=False),
                           is_above_threshold=is_above_threshold,
                           usage_graph=usage_graph.to_html(full_html=False))

@app.route('/if_change_page')
def if_change_page():
     return render_template('if_change_page.html')


@app.route('/att-plan', methods=['POST'])
def determine_att_plan():
    data = request.json
    
    company_size = data.get('company_size')
    num_devices = int(data.get('num_devices'))
    company_industry = data.get('company_industry')
    
    company_size_encoded = company_size_encodings.get(company_size, -1)
    company_industry_encoded = company_industry_encodings.get(company_industry, -1)
    
    if company_size_encoded == -1 or company_industry_encoded == -1:
        return jsonify({'error': 'Invalid company size or industry'}), 400
    
    recommended_plan = recommend_plan(num_devices, company_size_encoded, company_industry_encoded)
    
    # Get the plan details based on the recommended plan
    plan_details = get_plan_details(recommended_plan)  
    
    return jsonify(plan_details)

# Define a function to determine the recommended plan based on input (example logic)
def recommend_plan(num_devices, company_size_encoded, company_industry_encoded):

    if num_devices <= 10 and company_size_encoded == 0 and company_industry_encoded == 0:
        return 0  # AT&T Basic Plan
    elif num_devices <= 20 and company_size_encoded == 1 and company_industry_encoded == 2:
        return 1  # AT&T Standard Plan
    else:
        return 2  # AT&T Premium Plan

# Define a function to get plan details based on the plan label
def get_plan_details(plan_label):
 
    plan_mapping = {
        0: {'name': 'AT&T Basic Plan', 'price': '$160 per month', 'speed': 'Up to 1 Gbps'},
        1: {'name': 'AT&T Standard Plan', 'price': '$225 per month', 'speed': 'Up to 2 Gbps'},
        2: {'name': 'AT&T Premium Plan', 'price': '$395 per month', 'speed': 'Up to  5Gbps'}
    }
    
    return plan_mapping.get(plan_label, {})

if __name__ == "__main__":
    app.run(debug=True)