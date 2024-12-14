import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "API-KEY"
genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel('gemini-pro')


def main():
    st.set_page_config(page_title="SQL Query Generator 🌐", page_icon=":robot:")
    
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>SQL Query Generator 🌐</h1>
            <p>This tool helps you generate SQL queries easily by providing inputs. Just select your desired table, columns, conditions, and more!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    text_input=st.text_area("Enter your natural language description of the SQL query")

    submit=st.button("Generate query")
    if submit:
        with st.spinner("Generating query..."):
            template="""
                create a sql query snippet using the below text:


                    {text_input}


                i just want a SQL Query, generate it to be copied directly without any quotations.
            """
            
            formatted_template=template.format(text_input=text_input)
            response=model.generate_content(formatted_template)
            sql_query=response.text

            sql_query = response.text.strip().lstrip("'''sql").rstrip("'''")

            expected_output="""
                what would be the expected response of this sql query snippet:


                    {sql_query}


                Simple tabular response with example data without explanation to be printed like a table.
            """

            expected_output_formatted=expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text

            explanation="""
                Explain this SQL query:


                    {sql_query}


                please provite with simplest of explanation with the keywords used.
            """
            exp_output=explanation.format(sql_query=sql_query)
            explanation=model.generate_content(exp_output)
            explanation=explanation.text

            with st.container():
                st.success("SQL Query Generated Successfully! Here's your query:")
                st.code(sql_query, language="sql")
                st.success("Expected Output:")
                st.markdown(eoutput)
                st.success("Explanation:")
                st.markdown(explanation)



if __name__ == "__main__":
    main()
