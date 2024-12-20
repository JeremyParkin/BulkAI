import streamlit as st


# Set Streamlit configuration
st.set_page_config(page_title="MIG Freeform Analysis Tool",
                   page_icon="https://www.agilitypr.com/wp-content/uploads/2018/02/favicon-192.png",
                   layout="wide")


st.header("Example Prompts")
st.subheader("Client Info")
named_entity = st.text_input("Named Entity", "")
if len(named_entity) == 0:
    named_entity = "[BRAND]"

topic_list = st.text_input("Comma seperated topic List", "")
st.subheader("Example Prompts")
st.info("NOTE: These prompts are not perfect. They may not even be good. They are just examples to get you started.")
st.write("Update the prompt examples with the appropriate details for your use case and refine as needed.")


with st.expander("Product finder"):
    f"""
    Please analyze the following story to see if any {named_entity} products appear in it. 
    If yes, respond with only the list of names. If no, respond with just the word 'No': 
    """

with st.expander("Spokesperson finder"):
    f"""
    Please analyze the following story to see if any {named_entity} spokespeople appear in it. 
    If yes, respond with only the list of names. If no, respond with just the word 'No': 
    """

with st.expander("Topic finder"):
    f"""
    Please analyze the following story to see if {named_entity} is explicitly associated with any of the following topics in it:
    [{topic_list}].
    If yes, respond with only the list of topic names. If no, respond with just the word 'No': 
    """

with st.expander("Sentiment"):
    f"""
    Analyze the sentiment of the following news story toward the {named_entity}. Focus on how the organization is portrayed using the following criteria to guide your analysis:\n
    POSITIVE: Praises or highlights the {named_entity}'s achievements, contributions, or strengths. \n
    NEUTRAL: Provides balanced or factual coverage of the {named_entity} without clear positive or negative framing. Mentions the {named_entity} in a way that is neither supportive nor critical.\n
    NEGATIVE: Criticizes, highlights failures, or blames the {named_entity} for challenges or issues.\n
    Note: Focus your analysis strictly on the sentiment toward {named_entity} rather than the broader topic or context of the story. 
    Provide a single-word sentiment classification (POSITIVE, NEUTRAL, or NEGATIVE) followed by a colon, then a one to two sentence explanation supporting your assessment. 
    If {named_entity} is not mentioned in the story, please reply with the phrase "NOT RELEVANT". Here is the story:
    """

    # f"""
    # Analyze the tone or sentiment of the following news story specifically toward the named entity, {named_entity}. Focus on how the entity is portrayed, directly or indirectly, in terms of achievements, actions, or associations. Determine whether the sentiment is Positive, Neutral, or Negative based on the language, context, and overall framing of the entity within the story. Use the following criteria to guide your analysis:\n
    # POSITIVE: Praises or highlights the entity's achievements, contributions, or strengths. Uses favorable or supportive language toward the entity. Attributes beneficial or advantageous outcomes to the entity's actions.\n
    # NEUTRAL: Provides balanced or factual coverage regarding the entity without clear positive or negative framing. Avoids strong language or bias in favor of or against the entity. Mentions the entity in a way that is neither supportive nor critical.\n
    # NEGATIVE: Criticizes, highlights failures, or associates the entity with challenges or issues. Uses unfavorable, disparaging, or hostile language toward the entity. Attributes negative outcomes or controversies to the entity's actions or decisions.\n
    # Note: Focus your analysis strictly on the sentiment toward {named_entity} rather than the broader topic or context of the story. Provide a single-word sentiment classification (Positive, Neutral, or Negative) followed by a colon, then a one to two sentence explanation supporting your assessment.\n
    # If {named_entity} is not mentioned in the story, please reply with the phrase "NOT RELEVANT: {named_entity} not mentioned in the story. Here is the story:\n
    # """

with st.expander("Junk checker"):
    f"""
    Analyze the following news story or broadcast transcript to determine the type of coverage for the {named_entity}. Your response should be a single label from the following categories:\n
 - Press Release – The content appears to be directly from a press release or promotional material.\n
 - Advertisement – The brand mention is part of an advertisement or sponsored content.\n
 - Legitimate News – The brand is mentioned within a genuine news story or editorial context.\n
 Reply with only the category label that best fits the coverage.
    """
