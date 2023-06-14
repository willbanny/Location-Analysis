import streamlit as st


def about():
    st.title("About")
    st.write("""Location Scoring is an app designed to find the best locations for Care Homes across England. We partition England into latitude and longitude coordinates separated by 250m districts, used some clever maths to figure out their nearest features and then some clever machine learning to cluster those districts together. Then we used some more clever maths to figure out which districts have the most care homes and where similar districts without care homes are.

This is the crux of our app. Showing real estate developers the best places to build in order exploit the most vulnerable segment of the population. At least the location will be great.""")


    tab1, tab2, tab3= st.tabs(["Team", "Maths", "Model"])
    with tab1:
        st.header("Team")
        st.write("Bland")
    with tab2:
        st.header("Maths")
        st.write("It's Clever")
        st.balloons()
    with tab3:
        st.header("Model")
        st.write("K-Means classifier with 100 clusters and standard params. It is fit to all the points (they aren't actually districts) accross England. We then predict the group of each care home.")
if __name__ == "__main__":
    about()
