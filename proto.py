import streamlit as st

st.write("Choose destination: \n")
st.write("Tandoor (T); Viceroy (V); Maruti (M); Evergreen (E)")

dest = st.text_input("Enter code: ")
qty = st.text_input("Enter number of people: ")

def calculate_price(dest, qty):
    qty = int(qty)  
    if dest == 'T' or dest == 'V' or dest == 'M':
        if qty > 5:
            price = (qty - 5) * 20 + 100
        else:
            price = 100
        else:
            price = 100
    elif dest == 'E':
        if qty > 5:
            price = (qty - 5) * 30 + 150
        else:
            price = 150
    else:
        price = None  # Invalid destination
    return price

if dest and qty:
    price = calculate_price(dest, qty)
    if price is not None:
        st.write(f"Your fare is {price}")
    else:
        st.write("Invalid destination code.")

    ye = st.text_input("Do you accept? (Y/N)")
    if ye.upper() == 'Y':
        st.write("Thank you for accepting the fare! Connecting you with a driver shortly")
    elif ye.upper() == 'N':
        st.write("We're sorry to hear that. Please choose another destination or adjust the number of people.")
