from ydata_profiling import ProfileReport
import pandas as pd

breast_df = pd.read_csv("breast_cancer.csv")
profile_breast = ProfileReport(breast_df, title="Breast Cancer Report")
profile_breast.to_notebook_iframe()
profile_breast.to_file("Breast_Report.html")

Insurance_df = pd.read_csv("insurance.csv")
profile_insurance = ProfileReport(Insurance_df, title="Insurance Report")
profile_insurance.to_notebook_iframe()
profile_insurance.to_file("Insurance_Report.html")

diabetes_df = pd.read_csv("diabetes2.csv")
profile_diabetes = ProfileReport(diabetes_df, title="Diabetes Report")
profile_diabetes.to_notebook_iframe()
profile_diabetes.to_file("Diabetes_Report.html")

heart_df = pd.read_csv("heart.csv")
profile_heart = ProfileReport(heart_df, title="Heart Report")
profile_heart.to_notebook_iframe()
profile_heart.to_file("Heart_Report.html")
