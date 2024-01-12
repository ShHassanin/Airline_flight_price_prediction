import streamlit as st
import joblib
import pandas as pd
import sklearn
import category_encoders
import datetime as dt

#load model and features names
Model= joblib.load("Model_.pkl")
Inputs= joblib.load("Columns.pkl")
#input lists
Airlines = joblib.load("Airlines.pkl")
Sources = joblib.load("Sources.pkl")
#Destinations = joblib.load("Destinations.pkl")
Source_to_dest = joblib.load("Source_dest.pkl")
stop_points = joblib.load("stop_points.pkl")

hours_mins_in_day = pd.date_range("00:00", "23:59", freq="1min").strftime('%H:%M').to_list()
shorts_cities = joblib.load("dict_cities.pkl")
routes = joblib.load("route.pkl")

#function to determine available_routes according to source,Destination have been selected
def stops_selection(source,destination):
    available_stops=[]
    for route in routes:
        if (route.split('→')[0].strip()==shorts_cities[source]) and (route.split('→')[-1].strip()==shorts_cities[destination]):
                available_stops.append(route.split('→')[1:-1])
    return     available_stops


# function to determine part of the day
def day_parts(x):
    h = int(x.split(':')[0])
    if h <= 4:
        return "mid night"
    elif h <= 7:
        return "early morning"
    elif h <= 11:
        return "morning"
    elif h<= 17:
        return 'afternoon'
    elif h <= 22:
        return "evening"
    elif h <= 23:
        return "night"

#function for yes/no options
def yes_no(x):
    return (1 if x=='Yes' else  0)

#function to convert layover
def layover(x):
    if x == '1 Short layover':
        return 1
    elif x == '1 Long layover':
        return 2
    elif x == '2 Long layover':
        return 3
    else:
        return 0


 #main 
def main():
    ## Setting up the page title and icon
    st.set_page_config(page_icon = 'planes.png',page_title= 'Flights price prediction')
    # Add a title in the middle of the page using Markdown and CSS
    st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>Flights price prediction</h1>", unsafe_allow_html=True)
    

    #record from user
    
    Airline = st.selectbox('Select Airline' ,Airlines)
    Source = st.selectbox('Select Source', Sources)
    #source is for a limitted distinations
    Destination = st.selectbox("Select Destination" ,Source_to_dest[Source])

    approx_Duration = st.slider('What is the approximate Duration (In hours)?' , 1.25,47.67,step=.01)
    
    Total_Stops = st.radio('How many stops ?',[0,1,2,3,4])
    
    day_of_journey = st.selectbox('Journey day',range(1,31) )#[ 1,  9, 12, 24, 27, 18,  3, 15,  6, 21])
    month_of_journey  = st.radio("Journey month:",[3,4,5,6],horizontal=True )

    arrival_day = st.selectbox("Arrival day:",range(1,31) )
    count_journey_days = (arrival_day) - (day_of_journey)

    dep_time = st.selectbox('What is the departure time the flight?' , hours_mins_in_day)
    arrival_time = st.selectbox('What is the arrival time of the flight?' , hours_mins_in_day)

    approx_Duration = arrival_time.split(':')[0]

    dep_day_part  = day_parts(dep_time)
    arrival_day_part  = day_parts(arrival_time)

    check_in_baggage_included = st.radio('Is check_in baggage included?',['Yes','No'],horizontal=True)
    
    #calculate rest features by calling its functions
    In_flight_meal = st.radio('Is In_flight meal included?',['Yes','No'],horizontal=True)
    Change_airports = st.radio('Is there Change airports?',['Yes','No'],horizontal=True)
    Business_class = st.radio('Is Business class?',['Yes','No'],horizontal=True)
    layover_ = st.radio('How much layover?',['1 Short layover','1 Long layover','2 Long layover','No layover'],horizontal=True)

    available_stops = stops_selection(Source,Destination)
    stops_points = st.selectbox("Select Stops if there :", available_stops )
    
#columns:Airline	Source	Destination	Duration	Total_Stops	day_of_journey	month_of_journey
    #	count_journey_days	dep_day_part	arrival_day_part	check-in baggage included	In-flight meal	Change airports	Business class	layover   'stop_points'


    #create the dataframe of the user's record 
    df =pd.DataFrame(columns=Inputs)
    df.at[0,'Airline']= Airline
    df.at[0,'Source']= Source
    df.at[0,'Destination']= Destination
    df.at[0,'Duration']=     approx_Duration
    df.at[0,'Total_Stops']=  Total_Stops
    df.at[0,'day_of_journey']= day_of_journey
    df.at[0,'month_of_journey']=  month_of_journey
    df.at[0,'count_journey_days']= count_journey_days
    df.at[0,'dep_day_part']= dep_day_part
    df.at[0,'arrival_day_part']= arrival_day_part
    df.at[0,'check-in baggage included']= yes_no(check_in_baggage_included)
    df.at[0,'In-flight meal']= yes_no(In_flight_meal)
    df.at[0,'Change airports']= yes_no(Change_airports)
    df.at[0,'Business class']=  yes_no(Business_class)
    df.at[0,'layover']= layover(layover_)
    df.at[0,'stop_points']= str(stops_points)


   
    
    #button to predict
    if st.button('predict'):
            
        st.dataframe(df)
        result= Model.predict(df)[0]
    
        st.success(f"Predicted Price for the flight is  =  {round(float(result),2)}")
     

if __name__ == '__main__':
    main()

