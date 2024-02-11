import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Penguin Prediction App

This app predicts the **Palmer Penguin** species!

""")

st.sidebar.header('User Input Features')


# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        island = st.sidebar.selectbox('Island',('Biscoe','Dream','Torgersen'))
        sex = st.sidebar.selectbox('Sex',('male','female'))
        bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1,59.6,43.9)
        bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1,21.5,17.2)
        flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0,231.0,201.0)
        body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0,6300.0,4207.0)
        data = {'island': island,
                'bill_length_mm': bill_length_mm,
                'bill_depth_mm': bill_depth_mm,
                'flipper_length_mm': flipper_length_mm,
                'body_mass_g': body_mass_g,
                'sex': sex}
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df,penguins],axis=0)

# Encoding of ordinal features
# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
encode = ['sex','island']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy], axis=1)
    del df[col]
df = df[:1] # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)


st.subheader('Prediction')
penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
st.write(penguins_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)

# Penguin information section
st.write("""
## About Penguins

### Adelie Penguins
Adelie penguins are one of the three species included in the Palmer penguins dataset. Here are some key characteristics:
- **Habitat**: Adelie penguins primarily inhabit the coastal areas of Antarctica.
- **Appearance**: They have a black head and back with a white belly, and they are the smallest of the three species.
- **Behavior**: Adelie penguins are known for their curious and energetic behavior, often forming large breeding colonies.

### Chinstrap Penguins
Chinstrap penguins are another species found in the Palmer penguins dataset. Here's what you need to know about them:
- **Habitat**: Chinstrap penguins are found in the Antarctic Peninsula and nearby islands.
- **Appearance**: They have a distinctive black line under their chin, giving them their name. They are medium-sized penguins.
- **Behavior**: Chinstrap penguins are agile swimmers and often hunt for fish, squid, and krill in the waters surrounding their colonies.

### Gentoo Penguins
Gentoo penguins are the third species included in the Palmer penguins dataset. Here are some facts about them:
- **Habitat**: Gentoo penguins inhabit various locations around the Antarctic Peninsula and nearby islands.
- **Appearance**: They have a white patch above their eyes and a wide orange beak. They are the largest of the three species.
- **Behavior**: Gentoo penguins are known for their loud vocalizations and elaborate courtship rituals. They build nests using rocks and pebbles and can dive to great depths in search of food.

For more detailed information about each penguin species and their habitats, behaviors, and conservation status, please refer to reputable sources such as scientific journals and conservation organizations.
""")


