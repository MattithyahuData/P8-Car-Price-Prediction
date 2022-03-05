# 🚘 Car Price Prediction: Project Overview 
* End to end project researching the effects certain attributes have on the value of a car
* Optimised Random Forest Regressor using RandomizedSearchCV to reach the best model
* Built a client facing API using flask 
* Deployed Model in using Heroku for wider use 

[View Deployed Model](https://carsalepricecalc.herokuapp.com/)

## Table of Contents 
*   [Resources](#resources)<br>
*   [Data Collection](#DataCollection)<br>
*   [Data Pre-processing](#DataPre-processing)<br>
*   [Data Warehousing](#DataWarehousing)<br>
*   [Exploratory data analysis](#EDA)<br>
*   [Data Visualisation & Analytics](#Dataviz)<br>
*   [Feature Engineering](#FeatEng)<br>
*   [ML/DL Model Building](#ModelBuild)<br>
*   [Model Optimisation](#ModelOpt)<br>
*   [Model Evaluation](#ModelEval)<br>
*   [Deployment](#ModelDeploy)<br>
*   [Project Management (Agile/Scrum/Kanban)](#Prjmanage)<br>
*   [Project Evaluation](#PrjEval)<br>
*   [Looking Ahead](#Lookahead)<br>
*   [Questions & Contact me](#Lookahead)<br>

<a name="Resources"></a>  

## Resources Used
**Python 3, PostgreSQL, SQL, Tableau, Heroku** 

[**Anaconda Packages:**](requirements.txt) **pandas numpy pandas_profiling ipywidgets sklearn matplotlib seaborn sqlalchemy kaggle psycopg2 ipykernel flask**<br><br>
Powershell command for installing anaconda packages used for this project    
```powershell
pip install pandas numpy pandas_profiling ipywidgets sklearn matplotlib seaborn sqlalchemy kaggle psycopg2 ipykernel flask
```

<a name="DataCollection"></a>  

## [Data Collection](Code/P8_Code.ipynb)
Powershell command for data import using kaggle API <br>
```powershell
!kaggle datasets download -d nehalbirla/vehicle-dataset-from-cardekho -p ..\Data --unzip 
```
[Data source link](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho)
[Data](Data/car data.csv)
*  Rows: 301 / Columns: 9
    *   Year    
    *   Selling_Price   
    *   Present_Price   
    *   Kms_Driven  
    *   Fuel_Type   
    *   Seller_Type 
    *   Transmission    
    *   Owner

 

<a name="DataPre-processing"></a>  

## [Data Pre-processing](Code/joining_data.sql)
After I had all the data I needed, I needed to check it was ready for exploration and later modelling. I made the following changes and created the following variables:   
*   General NULL and data validity checks  
*   Web-scraped conversion data for the corresponding years for Rupees to GBP. 
*   Used SQL to join this data and apply the conversions respectively 
    *   I created substitute columns from Lakhs to GBP and used those instead 

```sql
SELECT	P8Car_Prices.*, 
		P8IND_to_GBP.Conversion, 
		(P8Car_Prices.Selling_Price * Conversion)*100000 AS GBP_Selling_Price,
		(P8Car_Prices.Present_Price * 100000) * (SELECT P8IND_to_GBP.Conversion
												FROM P8IND_to_GBP
												WHERE Year = 2017) AS GBP_Present_Price
FROM P8Car_Prices 
INNER JOIN P8IND_to_GBP 
ON P8Car_Prices.Year = P8IND_to_GBP.Year;
```

<a name="DataWarehousing"></a>

## [Data Warehousing](Code/P8_Code.ipynb)
I warehouse all data in a Postgre database for later use and reference.

*   ETL in python to PostgreSQL Database.
*   Formatted column headers to SQL compatibility. 


```python 
# Function to warehouse data in a Postgre database 
def store_data(data,tablename):
    """
    :param data: variable, enter name of dataset you'd like to warehouse
    :param tablename: str, enter name of table for data 
    """

    # SQL table header format
    tablename = tablename.lower()
    tablename = tablename.replace(' ','_')

    # Saving cleaned data as csv
    data.to_csv(f'../Data/{tablename}_clean.csv', index=False)

    # Engine to access postgre
    engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/projectsdb')

    # Loads dataframe into PostgreSQL and replaces table if it exists
    data.to_sql(f'{tablename}', engine, if_exists='replace',index=False)

    # Confirmation of ETL 
    return("ETL successful, {num} rows loaded into table: {tb}.".format(num=len(data.iloc[:,0]), tb=tablename))
 
# Calling store_data function to warehouse cleaned data
store_data(data,"P8 Car Price Prediction")
```

<a name="EDA"></a>  

## [Exploratory data analysis](Code/P8_Code.ipynb) 
I looked at the distributions of the data and the value counts for the various categorical variables that would be fed into the model. Below are a few highlights from the analysis.
*   More than 70% of cars were bought brand new. 
*   There are over 5 times more manual cars than automatic cars in the data 

<img src="images/categoricalfeatures_countdistrib.png" />

*   The distribution plot shows the distribution of numeric columns 

<img src="images/categoricalfeatures_distrib.png" />

*   The features are not strongly correlated generally. 
*   The kms_driven are inversely correlated to the year of sale, which makes sense because older cars are more likely to have driven further than those with a more recent year (larger year)
<img src="images/correlation.png" />

<a name="Dataviz"></a>  

## [Data Visualisation & Analytics](https://public.tableau.com/app/profile/mattithyahu/viz/P8CarPriceAnalysis/Dashboard?publish=yes)
[View Interactive Dashboard](https://public.tableau.com/app/profile/mattithyahu/viz/P8CarPriceAnalysis/Dashboard?publish=yes)
*   I created an interactive dashboard to interactively analyse the reltionships between features.

<!-- Dashboard -->

<!-- <div class='tableauPlaceholder' id='viz1646433888255' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='P8CarPriceAnalysis&#47;Dashboard' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1646433888255');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1827px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script> -->

<a name="FeatEng"></a>  

## [Feature Engineering](Code/P8_Code.ipynb) 
I transformed the categorical variables 'fuel_type', 'seller_type', and 'transmission' into dummy variables. I also split the data into train and tests sets with a test size of 20%.
*   One Hot encoding to encode values

```python
# One Hot encoding for remaining categorical field 
data = pd.get_dummies(data, drop_first = True)

# Viewing first 5 rows
data.head()

# Using train test split to split train and test data 
X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.20, random_state=23, shuffle=True)

# Viewing shape of train / test data
print(X_train.shape)
print(X_test.shape)
```
  

<a name="ModelBuild"></a> 

## [ML/DL Model Building](Code/P8_Code.ipynb)

I used the RandomForestRegressor because of its performative benefits. RFRs have some key advantages that make them most suitable for certain problems and situations:
*   It automates missing values present in the data
*   Normalising of data is not required as it uses a rule-based approach

```python
# Calling RFRegressor for the regression use case 
regressor=RandomForestRegressor()

# Training model on training data byy fitting it with train data
regressor.fit(X_train, y_train)
```

<!-- <img src="images/Crossvalidation.png" /> -->
<!-- 
<a name="ModelPerf"></a> 

## [Model performance](Code/P6_Code.ipynb)
*   **RandomForestRegressor** : Accuracy = 84.45%  -->

<a name="ModelOpt"></a> 

## [Model Optimisation](Code/P8_Code.ipynb)
In this step, I used RandomizedSearchCV to find the best parameters to optimise the performance of the model. 

```python
# Setup random hyperparameter search for LogisticRegression
regressor = RandomizedSearchCV(estimator = regressor, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)

# Training model on training data byy fitting it with train data
regressor.fit(X_train, y_train)
```

<a name="ModelEval"></a> 

## [Model Evaluation](Code/P8_Code.ipynb)
*   I used the r2_score to see the error associated with the model. But because it is a regression use case, I can’t give an accuracy score. 
An R-Squared value above 0.7 would generally be seen as showing a high level of correlation. The model achieved a R2 value of 0.828.
A value of 0.5 means that half of the variance in the outcome variable is explained by the model.

*   Plotting the actual and predicted values for both the training and test sets shows how accuracy and linear correlation decreases only slightly in the test data. 
<img src="images/trainevaluation.png" />
<img src="images/testevaluation.png" />

 

<a name="ModelProd"></a> 

## [Model Productionisation](app.py)
I built a flask REST API endpoint that was hosted on a local webserver before Heroku deployment. The API endpoint takes in request values and returns prediction of diabetes diagnosis. I also optimised and formatted the frontend using HTML and CSS. 

*   This code takes user input from the model frontend to run it through the model and returns and input.
<br>

```python
# Creating flask app / Initiating app
app = Flask(__name__)

# Load pickle model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

# Define the home page
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')
```

<a name="ModelDeploy"></a> 

## [Deployment](https://carsalepricecalc.herokuapp.com/)
The end point was deployed using the Heroku cloud platform. Click above to use it!  

<a name="Prjmanage"></a> 

## [Project Management (Agile/Scrum/Kanban)](https://www.atlassian.com/software/jira)
* Resources used
    * Jira
    * Confluence
    * Trello 

<a name="PrjEval"></a> 

## [Project Evaluation]() 
*   WWW
    *   The end-to-end process
    *   Use larger data 
    *   Use data tailored to European cars 
*   EBI 
    *   Frontend Tuning
    *   Try other algorithms 

<a name="Lookahead"></a> 

## Looking Ahead
*   What next
*   Can this be used on something like WeBuyanycar.com?? 

<a name="Questions"></a> 

## Questions & Contact me 
For questions, feedback, and contribution requests contact me
* ### [Click here to email me](mailto:contactmattithyahu@gmail.com) 
* ### [See more projects here](https://mattithyahudata.github.io/)




