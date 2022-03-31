from ast import keyword
from typing import Any, Text, Dict, List, Union, Optional
# from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset

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
        keyword = tracker.get_slot("movie_key")
        #print(genre)
        df = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+'/tmdb_5000_movies.csv', sep=',', usecols = ['title', 'genres', 'keywords'])
        df = df[df['genres'].str.contains(genre, case=False)]
        message = "You can watch these:\n"
        if (keyword != None):
            df_with_key = df[df['keywords'].str.contains(keyword, case=False)]
            if (int(df_with_key.size/3) == 0):
                message = "I can't find any movie with your given keyword. Yet, you can still watch these:\n"
            else:
                df = df_with_key
        if int(df.size/3) > 5:
            df_selected = df.sample(n=5)
        else:
            df_selected = df
        recommendation_list = df_selected['title'].to_list()
        i=0
        for x in recommendation_list:
            i += 1
            message += str(i) + ". " + x + '\n'
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

        return [AllSlotsReset()]