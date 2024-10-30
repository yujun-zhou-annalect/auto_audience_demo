import streamlit as st
import pandas as pd
from pathlib import Path

# Custom CSS to improve the look
custom_css = """
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4A4A4A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .audience-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E90FF;
        margin-bottom: 0.5rem;
    }
    .audience-summary {
        background-color: #F0F8FF;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: black;
    }
    .audience-summary h4 {
        text-decoration: underline;
    }
    .attribute {
        border-radius: 5px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.9rem;
        color: #888;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #1C86EE;
    }
    .container {
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
    
</style>
"""

# Function to load CSV data
def load_csv_data(file_path):
    return pd.read_csv(file_path)

def main():
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Main header
    st.markdown("<h1 class='main-header'>Audience Recommendation Agent</h1>", unsafe_allow_html=True)
    
    # Load CSV data
    # Add a selectbox for version selection
    version = st.selectbox(
        'Select version',
        ('attribute_swap', 'naive_clustering')
    )
    
    # Determine the file to read based on the selected version
    if version == 'attribute_swap':
        file_to_read = "nl2aud_demo_attribute_swap_v2.csv"
    else:
        file_to_read = "nl2aud_demo_attribute_naive_clustering_v1.csv"


    # csv_file = "nl2aud_demo_attribute_swap_v2.csv"  
    df = load_csv_data(file_to_read)

    # Dropdown for audience prompts
    audience_prompts = df['Audience Description'].tolist()
    selected_prompt = st.selectbox("Assuming the user entered Audience Descpription is: ", audience_prompts)

    # Filter data based on selected prompt
    df = df[df['Audience Description'] == selected_prompt]

    # Display audience information
    st.subheader("Recommended Audiences")
    cols = st.columns(3)
    for i, col in enumerate(cols, start=1):
        with col:
            # Display local image
            image_path = Path(f"images/audience_{i}.png")
            if image_path.exists():
                st.image(str(image_path), caption=f"Audience {i}", use_column_width=True)
            else:
                st.write(f"Image for Audience {i} not found")

            st.markdown(f"<div class='audience-name'>{df[f'audience_name_{i}'].iloc[0]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='audience_oneliner'>{df[f'audience_oneliner_{i}'].iloc[0]}</div>", unsafe_allow_html=True)
   
            with st.container():
                st.markdown("<div class='button-container'>", unsafe_allow_html=True)                
                if st.button(f"View Details {i}"):
                    st.session_state['show_details'] = i
                    st.session_state['view'] = 'details'
                    st.rerun()
                
                if st.button(f"View Attributes {i}"):
                    st.session_state['show_attributes'] = i
                    st.session_state['view'] = 'attributes'
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)    

    # Display detailed summaries on separate pages
    if 'view' in st.session_state:
        if st.session_state['view'] == 'details' and 'show_details' in st.session_state:
            i = st.session_state['show_details']
            st.title(f"{df[f'audience_name_{i}'].iloc[0]}")
            
            # Display the image in the detailed view as well
            image_path = Path(f"images/audience_{i}.png")
            if image_path.exists():
                st.image(str(image_path), caption=f"Audience {i}", use_column_width=True)
            
            # Add your detailed summary content here
            st.write(f"{df[f'audience_summary_{i}'].iloc[0]}")
            # Add more details as needed
            if st.button("Back to Main Page"):
                del st.session_state['show_details']
                del st.session_state['view']
                st.rerun()
        
        elif st.session_state['view'] == 'attributes' and 'show_attributes' in st.session_state:
            i = st.session_state['show_attributes']
            st.title(f"Attributes for {df[f'audience_name_{i}'].iloc[0]}")
            
            # Display the attributes in the detailed view
            attributes = df[f'attribute_{i}'].iloc[0].split('AND')
            formatted_attributes = '<br>'.join([attr.strip() + '\n <br> AND' for attr in attributes[:-1]] + [attributes[-1].strip()])
            st.markdown(f"<div class='attribute'>{formatted_attributes}</div>", unsafe_allow_html=True)
            # Add more details as needed
            if st.button("Back to Main Page"):
                del st.session_state['show_attributes']
                del st.session_state['view']
                st.rerun()

if __name__ == "__main__":
    main()