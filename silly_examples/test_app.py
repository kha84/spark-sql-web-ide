import streamlit as st
import random

def generate_random_number(min_value, max_value):
    return random.randint(min_value, max_value)

def main():
    st.title("Random Number Generator with Increment")
    
    # Initialize the session state
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    
    # Create two columns layout
    col1, col2 = st.columns(2)
    
    # Column 1 (Left column) - Random number generation
    # User input for the range
    min_range = col1.number_input("Enter the minimum value:", value=1)
    max_range = col1.number_input("Enter the maximum value:", value=100)
        
    # Check condition and display error
    if min_range >= max_range:
        col1.error("Error: Minimum value must be less than the maximum value.")
    else:
        # Empty space for horizontal centering of the button
        col1.write("")
        col1.write("")
        
       
        if st.button("Generate Random Number"):
            random_number = generate_random_number(min_range, max_range)
            col1.success(f"Random number: {random_number}")
            
            # Increment the counter on button click
            st.session_state.counter += 1
            col1.write(f"Button has been clicked {st.session_state.counter} times.")
    
    # Column 2 (Right column) - Additional text
    col2.write("This is some text displayed in the right column.")
    col2.write("You can add more content here as needed.")
    col2.write("Feel free to customize the layout and styling!")

if __name__ == "__main__":
    main()

