from typing import Any, Text, Dict, List, Union, Optional
# from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

import requests
import json
import os
import pandas as pd

import os

# load_dotenv()

# airtable_api_key=os.getenv("AIRTABLE_API_KEY")
# base_id=os.getenv("BASE_ID")
# table_name=os.getenv("TABLE_NAME")

# def create_health_log(confirm_exercise, exercise, sleep, diet, stress, goal):
#     request_url=f"https://api.airtable.com/v0/{base_id}/{table_name}"

#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {airtable_api_key}",
#     }  
#     data = {
#         "fields": {
#             "Exercised?": confirm_exercise,
#             "Type of exercise": exercise,
#             "Amount of sleep": sleep,
#             "Stress": stress,
#             "Diet": diet,
#             "Goal": goal,
#         }
#     }
#     try:
#         response = requests.post(
#             request_url, headers=headers, data=json.dumps(data)
#         )
#         response.raise_for_status()
#     except requests.exceptions.HTTPError as err:
#         raise SystemExit(err)
    
#     return response
#     print(response.status_code)

# class ValidateHealthForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_health_form"

#     async def validate_confirm_exercise(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if value:
#             return {"confirm_exercise": True}
#         else:
#             return {"exercise": "None", "confirm_exercise": False }

class ActionSubmitResults(Action):
    def name(self) -> Text:
        return "action_submit_results"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        confirm_exercise = tracker.get_slot("confirm_exercise")
        exercise = tracker.get_slot("exercise")
        sleep = tracker.get_slot("sleep")
        stress = tracker.get_slot("stress")
        diet = tracker.get_slot("diet")
        goal = tracker.get_slot("goal")

        # response = create_health_log(
        #         confirm_exercise=confirm_exercise,
        #         exercise=exercise,
        #         sleep=sleep,
        #         stress=stress,
        #         diet=diet,
        #         goal=goal
        #     )

        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []

class ActionFindMovie(Action):
    def name(self) -> Text:
        return "action_find_movie"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

    ####TODO: searching at csv - specific format of input as a dict(/) of [id, name]?
        genre = tracker.get_slot("movie")
        #print(genre)
        df = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+'/tmdb_5000_movies.csv', sep=',', usecols = ['title', 'genres'])
        df = df[df['genres'].str.contains(genre, case=False)]
        df_selected = df.sample(n=5)
        recommendation_list = df_selected['title'].to_list()
        message = "You can watch these:\n"
        for i in range(5):
            #message += 
            message += str(i+1) + ". " + recommendation_list[i] + "\n"
        #exercise = tracker.get_slot("exercise")
        #sleep = tracker.get_slot("sleep")
        #stress = tracker.get_slot("stress")
        #diet = tracker.get_slot("diet")
        #goal = tracker.get_slot("goal")

        # response = create_health_log(
        #         confirm_exercise=confirm_exercise,
        #         exercise=exercise,
        #         sleep=sleep,
        #         stress=stress,
        #         diet=diet,
        #         goal=goal
        #     )

        #dispatcher.utter_message("Thanks, your answers have been recorded!")
        dispatcher.utter_message(message)

        return []