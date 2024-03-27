import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key= st.secrets["GOOGLE_API_KEY"])

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
        response = model.generate_content([input,image, "The story should have a beautiful title related to the context of the story", "A beautiful, insigtful moral lesson should be mentioned at the end of the story"])
    else:
        response = model.generate_content(image)

    response = response.text
    return response

# Streamlit app
def upload_picture():
    uploaded_file = st.file_uploader("Upload Picture", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Picture', use_column_width=True)
        return image

# Function to display the sample picture options
def use_sample_picture():
    sample_option = st.selectbox('Select a sample picture:', ['Dog', 'Jungle', 'Auditorium'])
    sample_images = {
        'Dog': './dog.jpeg',
        'Jungle': './jungle.png',
        'Auditorium':  './auditorium.png',
    }
    if sample_option in sample_images:
        image = Image.open(sample_images[sample_option])
        st.image(image, caption=sample_option, use_column_width=True)
        return image

st.set_page_config(page_title="Image To Story", page_icon="✨")
st.markdown("""
    <style>
        .header {
            font-size: 56px;
            color: #1E90FF; /* Change the color as per your preference */
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* Add shadow effect */
        }
        .response {
            font-size: 54px;
            color: green; /* Change the color as per your preference */
            text-align: left;
            margin-bottom: 20px;
        }
        .ouput {
            font-size: 29px;
            color: #333333; /* Change the color as per your preference */
            line-height: 1.5;
            padding: 10px;
            border-radius: 5px;
            background-color: #f0f0f0; /* Change the background color as per your preference */
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)
created_style = """
    color: #888888; /* Light gray color */
    font-size: 99px; /* Increased font size */
""" 
st.markdown("<p style='{}'>➡️created by 'Muhammad Zain Attiq'</p>".format(created_style), unsafe_allow_html=True)
st.markdown('<h1 class="header">Image To Story</h1>', unsafe_allow_html=True)
with st.expander("About the app..."):
    st.info("This is a AI powered story generator app which will convert your images to interesting stories by assuming some characters and building a story around them. You will just upload the image and select that what type of story you want.")

story_genre = st.radio("Select the story genre", horizontal= True, options=[
    "Adventure",
    "Romance",
    "Mystery",
    "Science Fiction",
    "Fantasy",
    "Thriller",
    "Historical Fiction",
    "Horror",
    "Drama",
    "Comedy",
    "Motivational"
])
if story_genre:
    instructions= f"Craft an engaging {story_genre} story inspired by the provided image. The story should stick to the {story_genre} genre. Your story should seamlessly integrate with the visual elements, bringing them to life through vivid descriptions and imaginative storytelling. Aim for a minimum of 100 words to ensure depth and richness in your story. You should only use Islamic named characters in your story"


choice = st.radio("Choose an option:", ("Upload Picture", "Use Sample Picture"))
image = None
if choice == "Upload Picture":
    image = upload_picture()
elif choice == "Use Sample Picture":
    image = use_sample_picture()

submit = st.button("Generate Story..")
if submit and instructions and image:
    response = get_gemini_response(instructions, image)
    st.markdown('<h1 class="response">Here is your Story...</h1>', unsafe_allow_html=True)
    st.write(response)