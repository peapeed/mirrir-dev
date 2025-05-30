#persona.py
#Responsible for defining and updating the user's persona style

default_user_style = {
    "formality": "casual",        # or "formal"
    "emoji_usage": True,          # or False
    "sentence_length": "short"    # or "long"
}
def get_default_persona():
    return default_user_style.copy()

def analyze_user_input(text, current_style):
    new_style = current_style.copy()
    # updates here...

    # Placeholder rules:
    if "!" in text or "?" in text:
        new_style["formality"] = "casual"
    if any(emoji in text for emoji in ["😎", "😊", "😂", "🥲"]):
        new_style["emoji_usage"] = True
    if len(text.split()) > 10:
        new_style["sentence_length"] = "long"
    else:
        new_style["sentence_length"] = "short"

    return new_style