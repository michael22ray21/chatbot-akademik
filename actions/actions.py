# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction


class ActionSetTopic(Action):

    def name(self) -> Text:
        return "action_set_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if (tracker.latest_message['intent']['name'].startswith('ask_needs')) :
            text = tracker.latest_message['intent']['name'].replace("ask_needs_", "")
            text = text.replace("_", " ")

        elif (tracker.latest_message['intent']['name'].startswith('ask_step')) :
            text = tracker.latest_message['intent']['name'].replace("ask_step_", "")
            text = text.replace("_", " ")

        dispatcher.utter_message(text = "Oke!")

        return [SlotSet("current_topic", text)]


class ActionSayTopic(Action):

    def name(self) -> Text:
        return "action_say_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = tracker.get_slot('current_topic')
        if not topic:
            dispatcher.utter_message(
                text="Aku tidak tahu topik pembicaraan kita.")
        else:
            dispatcher.utter_message(
                text=f"Kita sedang membicarakan tentang {topic}.")

        return []


class ValidateAskStepPindahKelasForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_ask_step_pindah_kelas_form"

    def validate_step_number(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # validate the step number given by the user
        # regex representation : [\d](\.[\d\w])?\.?
        if re.search(r"[\d](\.[\d\w])?\.?", value.lower()):
            [SlotSet("current_query", value.lower())]
            dispatcher.utter_message(response = "utter_step_detail")
            return {"step_number": value.lower()}
        else:
            return {"step_number": None}

    def validate_continue(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # validate whether the user wants to continue or not
        if Tracker.get_intent_of_latest_message == "affirm":
            return {"continue": True, "step_number": None}
        else:
            return {"continue": False}
