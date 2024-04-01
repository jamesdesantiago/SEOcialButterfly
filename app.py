import streamlit as st
from seoanalyzer import analyze
import pandas as pd
import advertools as adv
import os
import datetime as dt
import requests
import xml.etree.ElementTree as ET

class QuestionsExplorer:
    def GetQuestions(self, questionType, userInput, countryCode):
        questionResults = []
        # Build Google Search Query
        searchQuery = questionType + " " + userInput + " "
        # API Call
        googleSearchUrl = "http://google.com/complete/search?output=toolbar&gl=" + \
            countryCode + "&q=" + searchQuery

        # Call The URL and Read Data
        result = requests.get(googleSearchUrl)
        tree = ET.ElementTree(ET.fromstring(result.content))
        root = tree.getroot()
        for suggestion in root.findall('CompleteSuggestion'):
            question = suggestion.find('suggestion').attrib.get('data')
            questionResults.append(question)

        return questionResults

google_api_key = st.secrets["google_api_key"]
google_cse_id = st.secrets["google_cse_id"]

st.title('seocial_buterfly')
st.write('SEOcial Butterfly is a powerful SEO research tool built with Streamlit. Designed to optimize websites for search engines by providing comprehensive insights and actionable recommendations. The tool performs keyword analysis, metadata checks, backlink tracking, and usability analysis, all presented in an intuitive, user-friendly interface. With SEOcial Butterfly, enhancing your websites SEO performance becomes a breeze.')

t1, t2, t3 = st.tabs(['Site Analysis', 'Serp Analysis', 'Keyword Coverage'])

with t1:
    with st.expander('Site Instructions'):
        st.write('Site Analysis')
        st.write('Enter the URL of the site you want to analyze and the link to the XML sitemap.')
        st.write('Click the "Analyze" button to start the analysis.')
        st.write('The results will be displayed below.')

    # Create a form for user input
    with st.form(key='site_analyzer'):
        # Text input for the site URL
        site_url = st.text_input('Site URL', help='Enter the URL of the site you want to analyze.')

        # Text area for the sitemap XML content
        sitemap_xml = st.text_ipnut('Sitemap (XML)', help='Enter the link of the XML sitemap here.')

        # Form submit button
        submit_button = st.form_submit_button('Analyze')

    # You can add functionality here to process the input data when the form is submitted
    if submit_button:
        output = analyze(site_url, sitemap_xml)
        df = pd.DataFrame(output['pages'])

        st.write('Site URL:', site_url)
        st.dataframe(df)

with t2:
    with st.expander('Serp Instructions'):
        st.write('Serp Analysis (Search Engine Results Page reviews the top ranking web pages for a specific search query. SERP analysis helps you understand the competition and identify opportunities to improve your website ranking.)') 
        st.write('Now you know who is ranked first on Google, but you dont know why.')
        st.write('Enter the search query you want to analyze.')
        st.write('Click the "Analyze" button to start the analysis.')
        st.write('The results will be displayed below.')

    # Create a form for user input
    with st.form(key='serp_analyzer'):
        # Text input for the search query
        search_query = st.text_input('Search Query', help='Enter the search query you want to analyze.')

        # Form submit buttonn
        submit_button = st.form_submit_button('Analyze')

    # You can add functionality here to process the input data when the form is submitted
    if submit_button:
        positions = list(range(1, 101, 10))
        res = adv.serp_goog(key=google_api_key, cx=google_cse_id, q=search_query, gl=["us"], start=positions)
        res_small = res[["searchTerms","rank","title","snippet","formattedUrl"]].copy()

        st.write('Search Query:', search_query)
        st.write('SERP Analysis Results:')

        st.write(res_small)
    
with t3:
    with st.form(key='keyword_coverage'):

        # Form submit button
        submit_button = st.form_submit_button('Generate Keyword List')
    
    # Processing form submission
    if submit_button:
        # Create an object of the QuestionsExplorer Class
        qObj = QuestionsExplorer()
        
        # Call the method and pass the parameters
        questions = qObj.GetQuestions("is", search_query, "us")
        
        # Convert the list of questions to a pandas DataFrame
        questions_df = pd.DataFrame(questions, columns=['Question'])

        st.subheader("Questions Found:")
        st.dataframe(questions_df)
