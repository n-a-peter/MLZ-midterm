import requests

#url = "http://localhost:9696/predict"  # docker and FastAPI url

url = "http://loan-serving-env.eba-3fmg4qvv.us-east-1.elasticbeanstalk.com/predict" # cloud url

#cloud_host_address = "loan-serving-env.eba-3fmg4qvv.us-east-1.elasticbeanstalk.com"

# client in test data that was not approved.
client = {
    'no_of_dependents': 2,
    'education': 'graduate',
    'self_employed': 'yes',
    'income_annum': 9400000,
    'loan_amount': 37300000,
    'loan_term': 14,
    'cibil_score': 383,
    'residential_assets_value': 7800000,
    'commercial_assets_value': 15900000,
    'luxury_assets_value': 27100000,
    'bank_asset_value': 7700000
 }

# client in test data that was approved
client_2 = {
    'no_of_dependents': 1,
    'education': 'not_graduate',
    'self_employed': 'yes',
    'income_annum': 7800000,
    'loan_amount': 22200000,
    'loan_term': 10,
    'cibil_score': 763,
    'residential_assets_value': 11200000,
    'commercial_assets_value': 1400000,
    'luxury_assets_value': 27000000,
    'bank_asset_value': 4900000
}

approval = requests.post(url, json=client).json()
print("Probability of approval = ", approval)


 