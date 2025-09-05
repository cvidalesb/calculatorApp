import streamlit as st
import math

# Set page config
st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🧮",
    layout="centered"
)

# Title
st.title("🧮 Simple Calculator")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # Input section
    st.subheader("Enter Numbers")
    
    # Number inputs
    num1 = st.number_input("First Number", value=0.0, step=0.1)
    num2 = st.number_input("Second Number", value=0.0, step=0.1)
    
    # Operation selection
    operation = st.selectbox(
        "Select Operation",
        ["Addition", "Subtraction", "Multiplication", "Division", "Power", "Square Root", "Percentage"]
    )

with col2:
    # Calculate button and result
    st.subheader("Result")
    
    if st.button("Calculate", type="primary"):
        try:
            if operation == "Addition":
                result = num1 + num2
                st.success(f"Result: {num1} + {num2} = {result}")
                
            elif operation == "Subtraction":
                result = num1 - num2
                st.success(f"Result: {num1} - {num2} = {result}")
                
            elif operation == "Multiplication":
                result = num1 * num2
                st.success(f"Result: {num1} × {num2} = {result}")
                
            elif operation == "Division":
                if num2 != 0:
                    result = num1 / num2
                    st.success(f"Result: {num1} ÷ {num2} = {result}")
                else:
                    st.error("Error: Division by zero is not allowed!")
                    
            elif operation == "Power":
                result = num1 ** num2
                st.success(f"Result: {num1}^{num2} = {result}")
                
            elif operation == "Square Root":
                if num1 >= 0:
                    result = math.sqrt(num1)
                    st.success(f"Result: √{num1} = {result}")
                else:
                    st.error("Error: Cannot calculate square root of negative number!")
                    
            elif operation == "Percentage":
                result = (num1 / 100) * num2
                st.success(f"Result: {num1}% of {num2} = {result}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Additional features
st.markdown("---")
st.subheader("Additional Features")

# Quick calculations
st.write("**Quick Calculations:**")

col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Clear All"):
        st.rerun()

with col4:
    if st.button("Example: 10 + 5"):
        st.info("Set First Number to 10, Second Number to 5, and select Addition")

with col5:
    if st.button("Example: 25% of 200"):
        st.info("Set First Number to 25, Second Number to 200, and select Percentage")

# Instructions
st.markdown("---")
st.subheader("How to Use")
st.markdown("""
1. **Enter Numbers**: Input your first and second numbers in the number fields
2. **Select Operation**: Choose the mathematical operation you want to perform
3. **Calculate**: Click the "Calculate" button to see the result
4. **Special Operations**:
   - **Square Root**: Only uses the first number
   - **Percentage**: Calculates what percentage the first number is of the second number
   - **Power**: Raises the first number to the power of the second number
""")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit* 🚀")
