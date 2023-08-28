import json
from .pipeLineLogic import logic


def lambda_handler(event, context):
    # Getting the data from the event object
    try:
        college_data = json.loads(event["body"])
        college_url = college_data.get("college_url")
        college_name = college_data.get("college_name")
        email_url = college_data.get("email_url")
        college_data_resp = logic.scrap_data(college_url, email_url, college_name)
        if college_data_resp:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Data inserted successfully for {c_name}".format(c_name=college_name)
                })
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Could not inserted data for {c_name}".format(c_name=college_name)
                })
            }
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Something is wrong!!"
            })
        }