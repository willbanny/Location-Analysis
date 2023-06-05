# Location-Analysis
Final Project repo - Location Analysis project

- best to start with very simple set of features (pure Google API?) and do an initial K means? Develop out from there with extra features

### Steps:

1. Data collection/sourcing
2. Create ETL packages for these sources and put into database
3. Create database map for relationships between different datasets
4. Create a final clean dataset to use for model
5. Test out different unsupervised clustering models and analyse results
6. Refactor code and improve results by adding features etc!

### Initial Tasks:

Will needs to do: set up macrobond api calling, source relevant data. 

1. get set up on Google API and figure out how to access features. See if you can find features going back in time too!
example video: https://m.youtube.com/watch?v=YwIu2Rd0VKM&pp=ygUgR29vZ2xlIG1hcHMgYXBpIGZpbmQgbmVhcmJ5IGJhcnM%3D
2. Get list of towns and cities in UK (say all places above 50k population)? Get their geo centroid (last part also a google api task)
3. Get crime data by town/city/region
4. Get the deprivation data, maybe need to figure out how to average it across bigger area (as very micro level)https://data.cdrc.ac.uk/dataset/index-multiple-deprivation-imd
