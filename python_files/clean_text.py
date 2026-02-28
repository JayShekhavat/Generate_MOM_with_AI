import re


# def clean_text(text):
#     text = re.sub(r'\s+', ' ', text)
#     return text.strip()


def clean_text(text):
    """
    Clean text by:
    - Replacing smart quotes with ASCII equivalents
    - Normalizing whitespace
    - Stripping leading/trailing spaces
    """
    if not isinstance(text, str):
        return text

    # FIX: Replace smart quotes and special characters
    replacements = {
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2013': '-',  # En dash
        '\u2014': '--',  # Em dash
        '\u2026': '...',  # Ellipsis
        '\u00a0': ' ',  # Non-breaking space
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Normalize whitespace (replace multiple spaces/tabs/newlines with single space)
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    return text.strip()



text = """Good morning everyone. Let’s start the weekly project review meeting. First, I want updates on the data integration module. Neha, can you go ahead?
Sure. So, the data cleaning pipeline is complete, and we’ve successfully processed last month’s dataset. However, we found some missing values in the customer activity logs. I’ve flagged those for validation.
Okay, how long will validation take?
Around two days. I need confirmation from the operations team.
Noted. Amit, what about the API development?
The main API is ready and working fine. We tested all endpoints locally. But deployment is pending because the staging server configuration isn’t finalized yet.
What’s blocking the configuration?
We need firewall permissions from IT. I sent the request yesterday.
Alright, follow up if no response by tomorrow.
From QA side, we completed functional testing of the login and dashboard modules. We found two minor bugs — one in report download and another in session timeout.
Are they critical?
No, both are low priority, but they should be fixed before release.
I’ll fix them today.
Good. Now let’s discuss the project timeline. We are slightly behind schedule. Can we still meet the deadline next Friday?
From data side, yes — if validation finishes on time.
Development is on track.
Testing can be completed in three days after fixes.
Great. Then the target release date remains unchanged.
Any other issues?
We need updated documentation for the dashboard features.
Amit, please share documentation by Wednesday.
Sure.
Alright, thanks everyone. Let’s meet again next Monday for progress review.
Thanks."""

cleaned_text = clean_text(text)