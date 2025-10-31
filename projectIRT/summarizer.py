import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

def summarize_text(text, max_input_chars=4000, language="English"):
    """
    Generates a clear, well-structured summary of the input text using the Gemini AI model.

    Parameters:
    - text (str): Full text to summarize.
    - max_input_chars (int): Max number of characters to process from the text.
    - language (str): Language in which the summary should be written. Defaults to English.
    """

    # Load environment variables
    load_dotenv()

    # Retrieve Gemini API key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY",'AIzaSyCVt5PymS9YFhshVJdWtR4wGcoKZFxP6t8')
    if not GEMINI_API_KEY:
        raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    # Initialize the model
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {e}")

    # Trim text to avoid token overflow
    trimmed_text = text[:max_input_chars]

    # Optional internal analysis (not used in output)
    try:
        _ = model.generate_content(
            f"""Analyze the following text to understand:
            - Main subject and objective
            - Key arguments or themes
            - Relevant statistics or facts
            - Structure and tone
            - Intended audience and purpose

            Do not output anything; this analysis is for internal use only.

            Text:
            {trimmed_text}
            """,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=100
            )
        )
    except Exception as e:
        logging.warning(f"Internal analysis skipped due to error: {e}")

    # Summarization prompt
    summary_prompt = f"""
        You are a professional summarization assistant. Your task is to generate a clear, concise, and paragraph-based summary of the given text.
        
        Guidelines:
        - Start with an introductory paragraph that defines the main topic and purpose.
        - Use logical paragraph structure to group themes or arguments.
        - Integrate important facts, statistics, or examples where relevant.
        - Use transitional phrases to connect ideas.
        - Conclude with key takeaways or implications.
        - Summary length should be around 250–300 words.
        - Do not make reference to webpage.
        - Try not to use "This"
        - Make it understandable for someone unfamiliar with the original document.
        
        Text to summarize:
        {trimmed_text}
        """

    try:
        response = model.generate_content(
            summary_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                top_p=0.9,
                top_k=40,
                max_output_tokens=1500
            )
        )
        return response.text.strip()

    except Exception as e:
        logging.error(f"Failed to generate summary: {e}")
        return "Summary generation failed due to an error."