# Predicting loan approval or refusal

This project trains a model on a dataset to determing if an individual's request for a loan should be approved or not. It is important to guage a person's capacity to repay a loan otherwise lenders such as banks will lose money withougt any guarantee of repayment. Certain characteristics or features associated with people can determine the likelihood that their loan request will be approved.

## Project files
- The dataset is "loan-approval-dataset.csv.
- The jupyter notebook is "loan_approval.ipynb" and contains the exploratory data analysis and model evaluation and predictions.
- The final ML model trained is in "train.py"
- The saved ML model is "model.bin".
- The script used to deploy the model online as a webservice is "predict.py"
- The script used to predict new users is in "test.py"
- The script used to manage the cloud deployment dependencies is in "Dockerfile"

## How to make use of this repository (repo for short)
To make use of this repository and run the codes to train the model and test predictions do the following in a terminal (preferably linux-like):
- clone the repository: "git clone [repo url]"
- change directory to the repo: "cd [repo name]"
- Install uv : "pip install uv" or "sudo apt install uv"
- Install the virtual environment: "uv sync --locked"
- Run the train.py script: "uv run python train.py"
- Run the predict.py script: "uv run predict.py"
- Uncomment the url for FastAPI in test.py script and then in a new terminal: "uv run python test.py"
- Kill the webservice then build the docker image: "docker build -t predict-loan-status ."
- Run the docker image "docker run -it --rm -p 9696:9696 predict-loan-status"
- In a new terminal run : "uv run python test.py"
- SSH into an virtual machine in the cloud and repeat the steps above.
- Then for elastic bean stalk run: uv run eb init –p docker –r [region] loan-serving-env
- Then run: "uv run eb create loan-serving-env".
- Modifie the url in test.py script to the cloud url you get after the previous step.
- Then run: "uv run python test.py"
- Finally terminate the instance: "uv run eb terminate loan-serving-env"
- Type the name of the enviroment at the prompt request and wait until it shuts down.
- Shut down the EC2 instance.

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

Comparing the three classifiers above the DecisionTreeClassifier has the best combined values for the roc_auc_score and the rmse. Hence we chose this classifier as the best and used it to train the combined train and validation data sets. We finally tested its performance on the test dataset and obtained an roc_auc_score of 0.996 and an rmse of 0.14, which shows that the model is able to predict unseen values very accurately.

## Deploying resulting ML model as a web service
To make this model useful to external party (e.g. the credit analyst in the bank), is it necessary for the model to be hosted where it can be easily accessed. Hosting it as a web service fulfils this condition. Here we first save the model as a script and then use FastAPI with uvicorn to deploy it as a web service. This web service can be queried with new user information through the following url below:

url = "http://localhost:9696/predict"

To deal with dependencies, we can use virtual environment such as those defined with uv to isolate versions of libraries to our web service. We could also go a step further to containerise our webservice which will facilitate deployment to the cloud. We use docker for such a containerization. After creating a dockerfile and doing the containerization with the commands below, the webservice can still be accessed through the same url above.

docker build -t predict-loan-status .

docker run -it --rm -p 9696:9696 predict-loan-status

To evaluate a customer's loan request, we can run:

uv run python test.py

and the result of the evaluation will be displayed in the command line.


## Deploying resulting web service in the cloud

Containerization makes the web service suitable for deployment in the cloud. For this, we would use elastic bean stalk.

This requires renting a virtual EC2 machine on AWS, SSHing into it, and then installing the required libraries. Next we install the aws elastic bean stalk command line interface "awsebcli" and use it to deploy our webservice to the cloud. Upon deployment, the webservice can be queried using the following url from the test.py script.

url = "http://loan-serving-env.eba-3fmg4qvv.us-east-1.elasticbeanstalk.com/predict"

You would need to comment the docker url and then uncomment this cloud url to test it.

The following pictures are screenshots of the model deployment in action:

![Commandline deployment code](screenshots/Deployment_command_line.PNG)
Command line code for the deployment.


![Cloud deployment running](screenshots/Cloud_deployment_running.PNG)
Cloud service can be seen running under cloud applications.


![Cloud loan-serving-environment](screenshots/Cloud_environment.PNG)
Cloud service can be seen running under environments.


![Predictions from cloud service](screenshots/predictions_from_cloud_service.PNG)
Predictions can be made by running test.py in the virtual environment and with different queries we get differnt results.


![Termination of cloud service](screenshots/terminating_cloud_service.PNG)
Terminating the could service with "eb terminate"


![Terminated instances](screenshots/Terminated_instances.PNG)
Terminated instances in the cloud.
