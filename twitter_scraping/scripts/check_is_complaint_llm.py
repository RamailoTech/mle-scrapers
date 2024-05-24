import openai
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("API_KEY")
openai.api_type = os.getenv("API_TYPE")

def get_system_prompt():
    system_prompt = """Is the following text describing a complaint about indian railway services. Answer 1 if true and 0 if not. Answer only 1 or 0, nothing else.
    Example 1:
    Mr @narendramodi will let people die/substandard service & so on  on Indian  Railways but won't privatise.

    Output: 1

    Example 2:
    Happy 52nd Birthday to Fastest Rajdhani Express in Indian Railways ""The Mumbai Rajdhani""
    @WesternRly
    #indianrailways

    Output: 0"""
    return system_prompt

def check_complaint(extracted_text, model_name="gpt-3.5-turbo"):
    prompt = get_system_prompt()
    user_input = f"Text to evaluate: ```{extracted_text}```"
    response = openai.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
        max_tokens=4095,
    )

    # Ensure correct extraction of the response from the updated API
    response_content = response.choices[0].message.content.strip()
    # Check if response is either '1' or '0', directly return as integer
    if response_content in ['1', '0']:
        return int(response_content)
    else:
        # Fallback in case of unexpected output
        return 0

def process_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    # Process each row to check for complaint
    df['is_complaint_true'] = df['text'].apply(check_complaint)

    # Write the modified DataFrame back to an Excel file
    output_path = file_path.replace('.xlsx', '_complaints.xlsx')
    df.to_excel(output_path, index=False, engine='openpyxl')

# Usage
file_path = "output/final_data/final_twitter_railway_data_cleaned.xlsx"
process_excel(file_path)




# import openai
# import csv
# import os
# from dotenv import load_dotenv
# import json

# load_dotenv()
# openai.api_key = os.getenv("API_KEY")
# openai.api_type = os.getenv("API_TYPE")


# def get_system_prompt():
#     system_prompt = """Is the following text describing a complaint about indian railway services. Answer 1 if true and 0 if not. Answer only 1 or 0, nothing else.
#     Example 1:
#     Mr @narendramodi will let people die/substandard service & so on  on Indian  Railways but won't privatise .

#     Output: 1
    
#     Example 2:
#     Happy 52nd Birthday to Fastest Rajdhani Express in Indian Railways ""The Mumbai Rajdhani"" 
#     @WesternRly
#     #indianrailways
    
#     Output: 0"""
#     return system_prompt


# def check_complaint(extracted_text, model_name="gpt-3.5-turbo"):
#     prompt = get_system_prompt()
#     user_input = f"Text to evaluate: ```{extracted_text}```"
#     response = openai.chat.completions.create(
#         model=model_name,
#         messages=[
#             {"role": "system", "content": prompt},
#             {
#                 "role": "user",
#                 "content": user_input,
#             },
#         ],
#         temperature=0,
#         max_tokens=4095,
#     )

#     # Ensure correct extraction of the response from the updated API
#     response_content = response.choices[0].message.content.strip()
#     # Check if response is either '1' or '0', directly return as integer
#     if response_content in ['1', '0']:
#         return int(response_content)
#     else:
#         # Fallback in case of unexpected output
#         return 0


# def process_csv(file_path):
#     results = []
#     with open(file_path, mode='r', newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             complaint_status = check_complaint(row['text'])
#             row['is_complaint_true'] = complaint_status
#             results.append(row)

#     with open(file_path, mode='w', newline='', encoding='utf-8') as file:
#         fieldnames = results[0].keys() if results else []
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(results)


# file_path = "output/twitter_railway_data.csv"
# process_csv(file_path)
