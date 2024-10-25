def get_sales_strategy_prompt(month, business_context):
    return f"""
    Given the current month of {month} and the business context of {business_context}, 
    suggest ways to increase sales by leveraging events in different geographical regions of India. 
    Map these suggestions into a calendar for the month.
    """

def get_product_list_prompt(domain):
    return (
        f"Check the domain given and gather info about products it sells. "
        f"Only provide list of products/services nothing else in below given output format. "
        f"{{\"product_list\":[]}} Domain: {domain}"
    )