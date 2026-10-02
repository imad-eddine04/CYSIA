from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load bundle
try:
    bundle = pickle.load(open('bedad_Loan.sav', 'rb'))
    model = bundle['model']
    scaler = bundle['scaler']
    model_columns = bundle['columns']
except FileNotFoundError:
    print("Error: bedad_Loan.sav not found!")


@app.route('/')
def index():
    return render_template('Before.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get numerical values from form (matching Before.html names)
        raw_data = {
            'credit_score': float(request.form.get('credit_score')),
            'annual_income': float(request.form.get('annual_income')),
            'loan_amount': float(request.form.get('loan_amount')),
            'employment_duration': float(request.form.get('employment_duration')),
            'Age': float(request.form.get('age')),
            'Children_Count': float(request.form.get('children')),
            'Previous_Loan_Count': float(request.form.get('prev_loans')),
            'Vehicle_Ownership': 1 if request.form.get('vehicle') == 'Yes' else 0
        }

        # Handle Categorical Dummies
        df_input = pd.DataFrame(columns=model_columns)
        df_input.loc[0] = 0  # Initialize with zeros

        # Set numericals
        for col, val in raw_data.items():
            if col in df_input.columns: df_input.loc[0, col] = val

        # Set dummy flags
        emp_col = f"EmploymentStatus_{request.form.get('employment_status')}"
        mar_col = f"MaritalStatus_{request.form.get('marital_status')}"

        if emp_col in df_input.columns: df_input.loc[0, emp_col] = 1
        if mar_col in df_input.columns: df_input.loc[0, mar_col] = 1

        # Scale and Predict
        scaled = scaler.transform(df_input)
        res = model.predict(scaled)[0]
        return render_template('After.html', data=res)

    except Exception as e:
        return f"Prediction Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)
