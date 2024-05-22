import openai
import csv
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("API_KEY")
openai.api_type = os.getenv("API_TYPE")


def get_system_prompt():
    system_prompt = """You are a multi-class classification model. You will be given a complaint about services in the railways. Classify the given compaint into the following four categories:
        delay: The complaint is about delays and punctuality issues in the train schedules.
        crowding: The complaint is about overcrowding in the trains. 
        expensive: The complaint is about the railways having become expensive and unaffordable. 
        derail: The complaint is about trains derailing. 
        hygiene: The complaint concerns the cleanliness and sanitary conditions of the trains.
        management: The complaint addresses issues related to the overall administration and organization of the train services. Also inculdes reduction in the number of sleeper and 3AC coaches, which disproportionately affects poor and middle-class passengers.
 
        Answer 1 if it falls into the given category 0 if not. Answer only 1 or 0, nothing else. Also, check the synonyms of the given categories. Provide the output in JSON format.
                Note: The given complaint might fall in all/some/any category.

        Sample output format:
        {
            "delay":1,
            "crowding": 1,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":1
        }

        Example 1:
        #indianrailway   #IndianRailways  tejas express (bom - goa) What a magnificent train but what a poor schedule.. express train waiting at each and every station. 2 hour delay. poor service - Indian  Railways .

        Output:
        {
            "delay":1,
            "crowding": 0,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":1
        }

        Example 2:
        Big punctuality fraud is going on in Indian  Railways . This practice of bogus punctuality data must be stopped. Use technology and stop manipulation. Indian  #Railways  runs a monopoly and has no regulator. Accidents occur. Premium fares, dynamic pricing. Anything for poor?

        Output:
        {
            "delay":1,
            "crowding": 1,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":0
        }"""
    return system_prompt


def check_complaint(extracted_text, model_name="gpt-3.5-turbo"):
    prompt = get_system_prompt()
    user_input = f"Text to evaluate: ```{extracted_text}```"
    response = openai.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": user_input,
            },
        ],
        temperature=0,
        max_tokens=4095,
    )

    # Ensure correct extraction of the response from the updated API
    response_content = response.choices[0].message.content.strip()
    start_index = response_content.find("{")
    end_index = response_content.rfind("}")
    response_content = response_content[start_index : end_index + 1]
    response_content_json = json.loads(response_content)
    return response_content_json


def process_csv(file_path):
    results = []
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get the output from check_complaint function
            complaint_results = check_complaint(row["text"])

            # Add the results of check_complaint directly into the row dictionary
            row.update(
                {
                    "delay": complaint_results["delay"],
                    "crowding": complaint_results["crowding"],
                    "expensive": complaint_results["expensive"],
                    "derail": complaint_results["derail"],
                    "hygiene": complaint_results["hygiene"],
                    "management": complaint_results["management"],
                }
            )
            results.append(row)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        # Ensure all fields are written to the CSV, including new fields
        fieldnames = results[0].keys() if results else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


file_path = "output/indian_railways_complaints.csv"
process_csv(file_path)
