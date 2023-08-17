# Resold Cars Finale

## Group Members
- Emmanuel Antwi
- Luis Martinez
- Matt George
- Rashidah Namutebi
- Steven Steinbring
- Hunter Gilliam


## Dataset Used
[US Used Cars Dataset](https://www.kaggle.com/datasets/ananaymital/us-used-cars-dataset) by Ananaymital on [Kaggle](kaggle.com)

## Python Libraries Used
- Dask
- Pandas
- Flask

# The Data
Since the data was provided to us, all we needed to do was load it into a dataframe. The first issue we ran into, was that the data file was
too big to be loaded directly into a Pandas DataFrame because Pandas loads all the data into memory and we were getting errors. So, we found
a Python library that specializes in loading in larger datasets called Dask. The data was loaded in like so:

```python
import dask.dataframe as dd
import pandas as pd

df = dd.read_csv("./Data/used_cars_data.csv", dtype={'bed': 'object',
       'bed_height': 'object',
       'bed_length': 'object',
       'cabin': 'object',
       'sp_id' : 'float64',
       'dealer_zip' : 'object'})
```

We then took a look at all the columns in the dataset and decided which ones would be beneficial for our machine learning model and our
analysis. We decided to completely drop 27 columns due to some having very little data to work with and others just not beneficial for any
reason we need it. The following columns were dropped:

```python
columns_to_drop = ['savings_amount', 'width', 'description', 'engine_type', 'sp_id', 'listing_id',
                   'power', 'torque', 'trimId', 'trim_name', 'vehicle_damage_category', 'major_options', 
                   'main_picture_url', 'length', 'is_oemcpo', 'is_cpo', 'is_certified', 'height', 'front_legroom', 'fleet', 
                   'combine_fuel_economy', 'cabin', 'bed_length', 'bed_height', 'bed', 'back_legroom', 'wheelbase']
```

Once the columns were dropped from the Dask DataFrame we were then able to export it as partitioned csv files. The function ended up creating
just over 150 csv files.

Because we took out a good portion of columns, we were able to use Pandas to load all the data into one DataFrame. We used the python library
```glob``` to read through the files and import all the csv files. The code we used to do so was:

```python
import glob

# Create a pattern for the file names
pattern = 'Data/Filtered/data-*.csv'

# Use the glob module to get all the files matching the pattern
file_list = glob.glob(pattern)

# Read each file into a DataFrame and store them in a list
dfs = [pd.read_csv(file) for file in file_list]

# Concatenate all the DataFrames in the list into a single DataFrame
df = pd.concat(dfs, ignore_index=True)
```

Now we had a DataFrame with just over 2.8 million rows of data.

Visually analyzing the data, we were able to see some outliers that didn't seem to fit with the rest of the data.

![Image of a Scatter Plot](images/ScatterPlot.png)

As we can see, there is one loan outlier in the "Mileage" category way up just below 600,000 miles. We wanted to get rid of this outlier,
so we did by dropping anything with mileage about 400,000.

The following is a bar chart of the counts of body types.

![Image of a Bar Chart](images/BarChart.png)

We noticed, very obviously, that the top 3 body types were the Pickup Truck, Sedan, and SUV / Crossover with the SUV / Crossover almost doubling
the next. So we decided to make our machine learning model solely based on the ```SUV / Crossover``` body type. We have plenty of data over it
and this allows the model to be more niche to each specific body type because we could make one specifically for each.

## Model
Our goal for the model was to allow a user to predict an accurate price of a vehicle that they provide. We decided on using a ```RandomForestRegressor```
to achieve this. We had to sacrifice certain columns of data to allow for an easier experience for the user. 

We decided to only include the columns as follows:

```
body_type, has_accidents, make_name, mileage, model_name, owner_count, price, transmission, year
```

Because we had plenty of data to train on, we decided to completely omit a portion of the data to give us completely unseen testing data.
After the data was filtered to only "SUV / Crossover" we were left with just over 1.3 million rows. So, 1 million rows was saved into ```train_data.csv```
and the remaining rows into ```test_data.csv```

The first step into our model was to take ```train_data.csv``` and split that into easy to use train and test variables. We did so as shown:

```python
df = pd.read_csv('./Data/ModelData/train_data.csv')
y = df['price']
X = df.drop(columns='price')

X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2)
```

Next came building the pipeline. We did find that there were some rows that were missing some values, now instead of completely getting rid of those
rows, we wanted to impute the values because we found that gave us a more accurate model. To do so, we first needed to separate our columns into
numerical and categorical data. We just used a couple of simple list comprehension lines as follows:

```python
numerical_cols = [cname for cname in X_train.columns if X_train[cname].dtype in ['int64', 'float64']]

categorical_cols = [cname for cname in X_train.columns if X_train[cname].nunique() < 10 and 
                        X_train[cname].dtype == "object"]
```

Now that we know what columns are what, we are able to start preparing our pipeline for them. For our numerical imputer we are using ```SimpleImputer()```
and for our categorical imputer we are using a pipeline that consists of a ```SimpleImputer()``` and a ```OneHotEncoder()```. This is how we set
up our imputers:

```python
numerical_transformer = SimpleImputer(strategy='constant')

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
```

Now all we have to do is create our prepocessor and model and then plug it into a pipeline. Like so:

```python
model = RandomForestRegressor(n_estimators=150, random_state=1)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
])

pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
```

We can now fit the pipeline and then call it for predictions. After fitting and predicting, we ran a r2 score function and got a score
of 0.918. After we were happy with the model, we saved the model using the ```joblib``` library into ```SUV_model.pk1```