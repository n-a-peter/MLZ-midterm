# Predicting loan approval or refusal

This project trains a model on a dataset to determing is an individual's request for a loan should be approved or not. It is important to guage a person's capacity to repay a loan otherwise lenders such as banks will lose money withougt any guarantee of repayment. Certain characteristics or features associated with people can determine the likelihood that their loan request will be approved.

## Exploratory data analysys
Exploratory data analysis was performed on the dataset. There are no missing values, however the column names contain some extra white spaces which had to be removed. Also the loan-status decision of 'Approved' or 'Rejected' were converted to integers '1' and '0' respectively. This loan-status variable is our target variable which we would like to predict. There was also a redundant loan_id column that was deleted from the dataset.

## Model training
To train a machine model to predict the target variable (i.e. loan_status), we have to find out the best possible model to use. This entails selecting a number of models and tuning them to find out which model performs best with respect to a given metric. The metric used here is the roc_auc_score and the root-mean-squared error (rmse). We would like the best model to have the highest roc_auc_score and the smallest rmse value.

Given that the target variable is a binary feature, it can be best presented as a classification task. We tried three different classifiers:
- LogisticRegression
- DecisionTreeClassifier
- RandomForestClassfier

To get the best peformance from model training, it is usual to split the dataset into three parts: training, validation, and test sets. The training is used to train the model, while the validation is used for tuning the model, and finally the test set is used for testing the final model.

For the LogisticRegression, we found that the 'lbfgs' solver peforms better than the 'liblinear' solver. We also tuned the regularization factor value 'C' and found the best value of C=10 which gave an roc_auc_score of 0.89, and an rmse score of 0.38 after 5-fold cross-validation.

For the DecisionTreeClassifier, we tuned the max_depth parameter and number of estimators and found that a max_depth of 4 for 10 estimators resulting in an roc_auc_score of 0.997 and an rmse score of 0.14. We did not proceed further to tune the minimum samples per leaf values because we already have almost 100% roc_auc_score.

For the RandomForestClassifier, we found the optimal number of estimators to be 60, and the maximum depth to be 10 resulting in an roc_auc_score of 0.992 and an rmse of 0.14.

Comparing the three classifiers above the DecisionTreeClassifier has the best combined values for the roc_auc_score and the rmse. Hence we chose this classifier as the best and used it to train the combined train and validation data sets. We finally tested it's performance on the test dataset and obtained an roc_auc_score of 0.996 and an rmse of 0.14, which shows that the model is able to predict unseen values very accurately.