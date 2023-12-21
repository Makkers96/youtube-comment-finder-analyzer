import google.generativeai as genai
import os

key = os.getenv('google_key')
genai.configure(api_key=key)

generation_config = {
    "temperature": 0,
    "max_output_tokens": 2048,
    "top_p": 1,
    "top_k": 1,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

text_model = genai.GenerativeModel('gemini-pro',
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)


def evaluate_positivity(comment):
    prompt = f"""
    You are a researcher who is evaluating YouTube comments on the following scoring system:
    1 - Negative
    2 - Slightly Negative
    3 - Neutral
    4 - Slightly Positive
    5 - Positive
    
    For the following comment, respond with the number that most appropriately rates the comment on how positive/negative it is towards the creator of the video (Big Lips McGee).
    
    Examples:
    
    Comment: thankyou to bring this up, great research lead to awesome vid
    Rating: 5

    Comment: Jesus your A crybaby,
    Rating: 1
    
    Comment: Game.. is dead.. sadly the P2W system has won..
    Rating: 3
    
    Comment: Don't agree with all of your points. I think SBI made faction warfare non-lethal to encourage new players to partake more rather then make whales swipe more. Not saying it shouldn't be IP capped tho. Absolutely agree in regards to the  .4 resources been added to the game. There was literally no reason to add that to the game other then the whales.
    Rating: 2
    
    Comment: why did I watch a video from this whiner?
    Rating: 2
    
    Comment: this is why i hate doing tracking
    Rating: 3
    
    Comment: 🤣🤣🤣🤣 Lmao
    Rating: 4
    
    Comment: I feel bad for the guy
    Rating: 3
    
    Comment: what happens if you hit a shapeshifter with a purge/cleanse?
    Rating: 3
    
    Comment: Big Mcgee I totally agree with you bro, this update is dog sh*t, before the update I was actually actually able to compete against higher IP classes and outplay other players in solo content, pretty much If the other player has an awaked weapon I’m probably gonna die even if they make many mistakes…
    Rating: 4
    
    Comment: {comment}
    Rating:"""
    result = text_model.generate_content(prompt)
    if result:
        response = result.text
        print(f"LLM Response For Positivity Rating: {response}")
    else:
        response = "Couldn't get a response from the llm."

    return response
