def get_sales_strategy_prompt(website, month, category_selected, events):
    events_str = "\n".join(
        f"{event[1]}: Happens on {event[2]} in {event[3]} - {event[4]}"
        for event in events
    )
    return f"""
    Given the website {website}, the current month of {month}, and the selected category {category_selected}, 
    suggest marketing campaigns to increase sales by leveraging the following events in different geographical regions of India for below given events:
    {events_str}
    Only include events that are relevant to the product category and have a high potential impact. Skip to return events that are not relevant or are nationally significant event like Gandhi Jayanti or other death anniversaries.
    Map these suggestions into a calendar for the month with detailed descriptions, marketing tips, and a score for each event based on relevance and impact.
    Don't include any other text, only the output format below.
    Output format:
    {{
        "15": {{
          "type": "high",
          "title": "Local Food Festival",
          "date": "{{month}} 15-17, {{year}}",
          "description": "Annual food festival attracting over 10,000 local food enthusiasts and families. Features local restaurants, food trucks, and cooking demonstrations.",
          "marketingTips": [
            "Set up a branded booth with product sampling",
            "Partner with complementary food vendors",
            "Run social media contests during the event",
            "Collect email signups with special festival-only offers"
          ],
          "score": 92,  // Score based on relevance and impact the product can have in event.
          "state": "Delhi"
        }},
        "20": {{
          "type": "medium",
          "title": "Tech Conference",
          "date": "{{month}} 20-22, {{year}}",
          "description": "Regional technology conference focusing on digital innovation and entrepreneurship. Attracts business leaders and tech professionals.",
          "marketingTips": [
            "Showcase your digital solutions",
            "Schedule one-on-one demos with potential clients",
            "Host a workshop or speaking session",
            "Offer exclusive conference attendee discounts"
          ],
          "score": 88,  // Score based on relevance and impact the product can have in event.
          "state": "Maharashtra"
        }}
    }}
    """

def get_product_list_prompt(scraped_data):
    return (
        f"Given the following raw data of websites of businesses and their products and services: {scraped_data},"
        f"Give maximum 10 broader category only of products/services of that business."
        f"Make sure it should be relevant to the business."
        f"Return the output in below given output format, nothing else, without backquotes"
        f"{{\"product_list\": [\"Object Name 1\", \"Object Name 2\", ...]}}"
    )
