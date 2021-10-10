# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
mname = 'facebook/blenderbot-400M-distill'
model = BlenderbotForConditionalGeneration.from_pretrained(mname)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet,SessionStarted,ActionExecuted, EventType ,AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from database_connectivity import DataUpdate,Datafetch,Datamenu,Datafetch_cuisine
from translate import Trans
import requests
#
# API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-90M"
# headers = {"Authorization": "Bearer api_BveRBnKHBIDYKcWFWvlFdUgqyNizkpNSMI"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World from my first action python code!")

        return []

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_order_food"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="aao kha lo khana!")
#
#         return []


# #####################################
# class Validate_food_order(FormValidationAction):
#
#     def name(self) -> Text:
#         return "validate_order_food_form"
#
#     def run(self, dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         #dispatcher.utter_message(text="check hoga validation")
#
#         return []
#
#     def validate_food_item(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
#         """Validate slot value."""
#         #dispatcher.utter_message(text="validate_name chal rha h kya")
#         if not slot_value:
#             return {"food_item": None}
#         else:
#             return {"food_item": slot_value}




class ActionSubmitProject(Action):
    def name(self) -> Text:
        return "action_submit_order"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("food_item")
        #print("email id  is  : ", user_name)

        full_order_list=Datafetch(tracker.sender_id)



        str=""
        if len(full_order_list) ==0:
            dispatcher.utter_message(text="Sorry, Please select items to place your order")
            return []

        dispatcher.utter_message(template="utter_order_placed")

        for x in full_order_list:
            str+="・"+x[0]+"\n"

        dispatcher.utter_message(str)

        return []


class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        #return [SlotSet("food_item", None)]
        return [AllSlotsReset()]



### action for placed_order

class Action_order_preview(Action):

    def name(self) -> Text:
        return "action_order_preview"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        x=tracker.get_slot("food_item")
        if x!=None:
            x=x.lower()

        full_list=Datamenu(None)
        print(x)
        print(full_list)

        flag=0
        for y in full_list:
            print(y[0].lower())
            if x==y[0].lower():
                flag=1
                break

        if flag==0:
            dispatcher.utter_message(template="utter_select_from_menu")
            dispatcher.utter_message(template="utter_show_menu")
            xy = ""
            for y in full_list:
                xy += y[0]
                xy += "\n"
            dispatcher.utter_message(xy)



        else:
            x=x.lower()
            DataUpdate(tracker.sender_id, x)
            # full_order.append(x)

            dispatcher.utter_message(template="utter_temp_order")


        return[SlotSet("food_item", None)]
#



class ActionSessionId(Action):
    def name(self) -> Text:
        return "action_session_id"

    async def run(
    self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id=tracker.sender_id
        dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        return []




#############################################################################action session restart

# class ActionSessionStart(Action):
#     def name(self) -> Text:
#         return "action_session_start"
#
#     # @staticmethod
#     # def fetch_slots(tracker: Tracker) -> List[EventType]:
#     #     """Collect slots that contain the user's name and phone number."""
#     #
#     #     slots = []
#     #     for key in ("name", "phone_number"):
#     #         value = tracker.get_slot(key)
#     #         if value is not None:
#     #             slots.append(SlotSet(key=key, value=value))
#     #     return slots
#
#     async def run(
#       self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#
#         # the session should begin with a `session_started` event
#         events = [SessionStarted()]
#
#         # any slots that should be carried over should come after the
#         # `session_started` event
#         # events.extend(self.fetch_slots(tracker))
#
#         # an `action_listen` should be added at the end as a user message follows
#         events.append(ActionExecuted("action_listen"))
#
#         return events


#### Action for printing menu
class Action_show_menu(Action):
    def name(self) -> Text:
        return "action_show_menu"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cusene=tracker.get_slot("cuisine_type")
        print(cusene)
        full_menu=Datamenu(cusene)

        dispatcher.utter_message(template="utter_show_menu")
        xy=""
        for x in full_menu:
            xy+=x[0]
            xy+="\n"

        #print(xy)
        dispatcher.utter_message(xy)

        return []



class Action_show_cuisine(Action):                 #action for available cuisines
    def name(self) -> Text:
        return "action_show_cuisine"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        clist=Datafetch_cuisine()
        print(clist)
        dispatcher.utter_message(template="utter_list_cuisine_line")
        xy = ""
        for x in clist:
            if x[0]== None:
                continue
            xy+="・"
            xy += x[0]
            xy += "\n"
        # print(xy)
        dispatcher.utter_message(xy)
        return []

class Action_nlu_fallback(Action):

    def name(self) -> Text:
        return "action_nlu_fallback"



    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get('text')
        #print(message)
        # output = query({
        #     "inputs": {
        #         "past_user_inputs": [],
        #         "generated_responses": [],
        #         "text": '"{}"'.format(message),
        #      },
        # })
        # print(output)

        inputs = tokenizer([message], return_tensors='pt')
        reply_ids = model.generate(**inputs)
        out=(tokenizer.batch_decode(reply_ids))
        out=out[0]
        print(out[4:-4])
        out=out[4:-4]
        jap=Trans(out)
        out+="  ( "
        out+=jap
        out+= "  ) "
        dispatcher.utter_message(out)


        # for key, value in output.items():
        #     dispatcher.utter_message(value)
        #     break
        return []