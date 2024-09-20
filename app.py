import streamlit as st
import pickle
import numpy as np

# Load the pre-trained model
with open('models/lgbm_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


# Define the ordinal mapping
ordinal_mapping = {
    0: "Very Poor",
    1: "Poor",
    2: "Average",
    3: "Good",
    4: "Excellent",
    5: "Outstanding"
}

# Define satisfaction mapping
satisfaction_mapping = {0: 'neutral or dissatisfied', 1: 'satisfied'}


# Function to convert user-friendly input back to numeric for prediction
def ordinal_to_numeric(input_value):
    reverse_mapping = {v: k for k, v in ordinal_mapping.items()}
    return reverse_mapping[input_value]



# Function to predict satisfaction
def predict_satisfaction(online_boarding, delay_ratio, inflight_wifi, passenger_class, travel_type, inflight_entertainment, 
                         flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness):
    
    X_new = np.array([online_boarding, delay_ratio, inflight_wifi, passenger_class, travel_type, inflight_entertainment, 
                      flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness]).reshape(1, -1)
    
    y_pred_new = loaded_model.predict(X_new)
    return y_pred_new


# Streamlit app title and layout
st.title("Flight Satisfaction Prediction")
st.markdown("**Get an instant prediction of flight satisfaction based on various factors.**")

# Create two columns for a better layout
col1, col2 = st.columns(2)

# Column 1 - Collecting Delay and Distance Info
with col1:
    st.header("Flight Information")
    
    arrival_delay = st.number_input('Arrival Delay (minutes)', min_value=0.0, step=1.0, help="Total minutes flight was delayed upon arrival.")
    departure_delay = st.number_input('Departure Delay (minutes)', min_value=0.0, step=1.0, help="Total minutes flight was delayed upon departure.")
    flight_distance = st.number_input('Flight Distance (km)', min_value=0.0, value=1000.0, step=1.0, help="Distance between departure and destination in kilometers.")

    # Calculate total delay and delay ratio
    total_delay = arrival_delay + departure_delay
    delay_ratio = total_delay / (flight_distance + 1)
    
# Column 2 - Collecting User Preferences for Flight Service
with col2:
    st.header("Service Ratings")

    inflight_wifi = st.selectbox('Inflight Wifi Service', list(ordinal_mapping.values()), help="Rate the inflight WiFi service.")

    online_boarding = st.selectbox('Online Boarding', list(ordinal_mapping.values()), help="Rate the online boarding process.")

    ease_online_booking = st.selectbox('Ease of Online Booking', list(ordinal_mapping.values()), help="Rate the ease of booking the flight online.")

    seat_comfort = st.selectbox('Seat Comfort', list(ordinal_mapping.values()), help="Rate the comfort level of the seat.")

    inflight_entertainment = st.selectbox('Inflight Entertainment', list(ordinal_mapping.values()), help="Rate the inflight entertainment options.")

    on_board_service = st.selectbox('On-board Service', list(ordinal_mapping.values()), help="Rate the quality of on-board service.")
    leg_room_service = st.selectbox('Leg Room Service', list(ordinal_mapping.values()), help="Rate the legroom space during the flight.")
    
    cleanliness = st.selectbox('Cleanliness', list(ordinal_mapping.values()), help="Rate the cleanliness of the flight environment.")
    
# Convert ordinal inputs to numeric values
inflight_wifi_num = ordinal_to_numeric(inflight_wifi)
online_boarding_num = ordinal_to_numeric(online_boarding)
ease_online_booking_num = ordinal_to_numeric(ease_online_booking)
seat_comfort_num = ordinal_to_numeric(seat_comfort)
inflight_entertainment_num = ordinal_to_numeric(inflight_entertainment)
on_board_service_num = ordinal_to_numeric(on_board_service)
leg_room_service_num = ordinal_to_numeric(leg_room_service)
cleanliness_num = ordinal_to_numeric(cleanliness)

# Organizing additional options in a horizontal layout
st.header("Additional Travel Information")

col3, col4 = st.columns(2)

with col3:
    passenger_class = st.selectbox('Class', ['Business', 'Eco', 'Eco Plus'], help="Select the class of your travel.")
    
with col4:
    travel_type = st.selectbox('Type of Travel', ['Business travel', 'Personal Travel'], help="Specify the purpose of your travel.")

# Convert class and travel type to numeric values
class_mapping = {'Business': 0, 'Eco': 1, 'Eco Plus': 2}
travel_type_mapping = {'Business travel': 0, 'Personal Travel': 1}

passenger_class_num = class_mapping[passenger_class]
travel_type_num = travel_type_mapping[travel_type]

# Button to make the prediction
if st.button('Predict Satisfaction'):
    # Make the prediction
    prediction = predict_satisfaction(online_boarding_num, delay_ratio, inflight_wifi_num, passenger_class_num, travel_type_num, 
                                      inflight_entertainment_num, flight_distance, seat_comfort_num, leg_room_service_num, 
                                      on_board_service_num, ease_online_booking_num, cleanliness_num)
    
    
    # Map the numeric prediction to the satisfaction label
    satisfaction_label = satisfaction_mapping[int(prediction[0])]

    
    # Display the prediction with interactivity
    if satisfaction_label == 'satisfied':
        st.success(f"✅ **Prediction: {satisfaction_label.capitalize()}**")
    else:
        st.warning(f"⚠️ **Prediction: {satisfaction_label.capitalize()}**")

