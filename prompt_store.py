def get_prompt(month, business_context):
    return f"""
    Given the current month of {month} and the business context of {business_context}, 
    suggest ways to increase sales by leveraging events in different geographical regions of India. 
    Map these suggestions into a calendar for the month.
    """