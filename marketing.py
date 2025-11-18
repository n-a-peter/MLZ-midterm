import requests

# url = "http://0.0.0.0:9696/predict"
url = "http://localhost:9696/predict"

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


approval = requests.post(url, json=client).json()
print("Probability of approval = ", approval)


#{'no_of_dependents': 1,
# 'education': 'graduate',
# 'self_employed': 'yes',
# 'income_annum': 8700000,
# 'loan_amount': 30000000,
# 'loan_term': 12,
# 'cibil_score': 543,
# 'residential_assets_value': 21900000,
# 'commercial_assets_value': 12700000,
# 'luxury_assets_value': 30600000,
# 'bank_asset_value': 12700000}
 