import streamlit as st
import requests
import json

# Define the Flask endpoint URL
FLASK_ENDPOINT = "https://app.wha7.com/clothes"  # Adjust the endpoint to your Flask server URL

# Add Custom CSS for Styling
st.markdown(
    """
    <style>
.card {
    background-color: #f9f9f9;
    border-radius: 15px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
    margin-bottom: 20px;
    max-width: 300px;
}
.card img {
    border-radius: 10px;
}
.card h2 {
    font-family: 'Arial', sans-serif;
    color: #000000; /* Changed text color to black */
}
.card p {
    color: #000000; /* Changed text color to black */
}
.card a {
    font-size: 14px;
    color: #007BFF;
    text-decoration: none;
}
</style>
    """,
    unsafe_allow_html=True
)

# Streamlit app starts here
st.title("Clothing Suggestion App")

# User inputs their phone number
phone_number = st.text_input("Enter your phone number:")

# Trigger the request only if a phone number is provided
if st.button("Get Clothes Recommendation") and phone_number:
    # Make the POST request to the Flask server
    try:
        response = requests.post(
            FLASK_ENDPOINT,
            data={"From": phone_number}  # Send the phone number as form data
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        clothes_data = response.json()
        print(clothes_data)
        st.title("Clothing Recommendations")

        # Process the data with Grid Layout
        cols = st.columns(2)  # Create two columns for a grid layout

        for idx, item in enumerate(clothes_data['clothes']):
            for key, value in item.items():
                with cols[idx % 2]:
                    # Handling missing images and URLs
                    # Handling missing images, URLs, descriptions, and prices
                    image_url = value['images'][0] if value.get('images') and len(value['images']) > 0 else None
                    product_url = value['urls'][0] if value.get('urls') and len(value['urls']) > 0 else "#"
                    price = value['price'][0] if value.get('price') and len(value['price']) > 0 else "Price not available"

                    

                    # Creating each card
                    st.markdown(
                        f"""
                        <div class="card">
                            {'<img src="' + image_url + '" width="100%">' if image_url else ''}
                            <h2>{key.title()}</h2>
                            <p><strong>Price:</strong> ${price}</p>
                            <a href="{product_url}" target="_blank" style="text-decoration: none;">
                                <button style="padding: 10px 15px; background-color: #007bff; color: white; border: none; cursor: pointer;">See Product</button>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting the server: {e}")

# Add some spacing or any additional UI elements if necessary
st.markdown("---")
st.text("Please make sure the Flask server is running at the specified endpoint.")
