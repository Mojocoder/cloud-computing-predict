# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
    Initial AWS Lambda function is used to decode POST-request data received from the 
    student portfolio website.

    Author: Explore Data Science Academy.
    Note:
    ---------------------------------------------------------------------
    The contents of this file should be added to a AWS  Lambda function 
    created as part of the EDSA Cloud-Computing Predict. 
    For further guidance around this process, see the README instruction 
    file which sits at the root of this repo.
    ---------------------------------------------------------------------
"""

# Lambda dependencies
import boto3  # Python AWS SDK
import json  # Used for handling API-based data.
import base64  # Needed to decode the incoming POST data

from botocore.exceptions import ClientError  # Catch errors on client side
import numpy as np  # array manipulation


def lambda_handler(event, context):
    # Perform JSON data decoding
    body_enc: object = event["body"]
    dec_dict = json.loads(base64.b64decode(body_enc))

    # Note that all of the POST data from our website form can now
    # be accessed via the `dec_dict` dictionary object.
    # For example, if we entered the name field as 'Student_name on the website' :
    # >>> dec_dict['name']
    # 'Student_name'

    # Create a response object to tell the website that the form data
    # was successfully received. We use the contents of the decoded JSON dictionary
    # to create this response. As the predict progresses, we'll include
    # more information about the AWS services we will invoke.

    # --- Write to dynamodb ---

    # ** Create a variable that can take a random value between 1 and 1 000 000 000.
    # This variable will be used as our key value i.e the ResponsesID and should be of type integer.
    # It is important to note that the ResponseID i.e. the rid variable, should take
    # on a unique value to prevent errors when writing to DynamoDB. **

    # --- Insert your code here ---
    rid = np.random.randint(1, 1000000000)  # <--- Replace this value with your code.
    # -----------------------------

    # ** Instantiate the DynamoDB service with the help of the boto3 library **

    # --- Insert your code here ---
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')  # <--- Replace this value with your code.
    # -----------------------------

    # Instantiate the table. Remember pass the name of the DynamoDB table created in step 4
    table = dynamodb.Table('Kevin-Reddy-Portfolio-Data')

    # ** Write the responses to the table using the put_item method. **

    # Complete the below code so that the appropriate
    # incoming data is sent to the matching column in your DynamoDB table
    # --- Insert your code here ---
    db_response = table.put_item(Item={'ResponsesID': rid,  # <--- Insert the correct variable
                                       'Name': dec_dict['name'],  # <--- Insert the correct variable
                                       'Email': dec_dict['email'],  # <--- Insert the correct variable
                                       'Cell': dec_dict['phone'],  # <--- Insert the correct variable
                                       'Message': dec_dict['message']  # <--- Insert the correct variable
                                       })
    # -----------------------------

    # ** Create a response object to inform the website
    #    that the workflow executed successfully. **

    email_text = 'Hello there! Thank you for your enquiry'

    # ** SES Functionality **

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    # --- Insert your code here ---
    SENDER = 'kevinreddyo@yahoo.com'
    # -----------------------------

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    # --- Insert your code here ---
    RECIPIENT = 'info.iceprojects1@gmail.com'
    # -----------------------------

    AWS_REGION = "eu-west-1"

    # The subject line for the email.
    # --- DO NOT MODIFY THIS CODE ---
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    # 'edsa.predicts@explore-ai.net', # <--- Uncomment this line once you have successfully tested your predict end-to-end
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,

        )

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])

    # ** Create a response object to inform the website
    #    that the workflow executed successfully. **

    lambda_response = {
            'statusCode': 200,
            'body': json.dumps({
            'Name': dec_dict['name'],
            'Email': dec_dict['email'],
            'Cell': dec_dict['phone'],
            'Message': dec_dict['message'],
            #'SES_response': ses_response,
            #'Email_message': email_text,
            'DB_response': db_response
        })
    }

    return lambda_response


# Find overwhelming sentiment in article

def find_max_sentiment(Comprehend_Sentiment_Output):
    sentiment_score = 0

    if Comprehend_Sentiment_Output[ 'Sentiment' ] == 'POSITIVE':
        sentiment_score = Comprehend_Sentiment_Output[ 'SentimentScore' ][ 'Positive' ]

    elif Comprehend_Sentiment_Output[ 'Sentiment' ] == 'NEGATIVE':
        sentiment_score = Comprehend_Sentiment_Output[ 'SentimentScore' ][ 'Negative' ]

    elif Comprehend_Sentiment_Output[ 'Sentiment' ] == 'NEUTRAL':
        sentiment_score = Comprehend_Sentiment_Output[ 'SentimentScore' ][ 'Neutral' ]

    else:
        sentiment_score = Comprehend_Sentiment_Output[ 'SentimentScore' ][ 'Mixed' ]

    print(sentiment_score, Comprehend_Sentiment_Output[ 'Sentiment' ])

    return Comprehend_Sentiment_Output[ 'Sentiment' ], sentiment_score


# Function dependencies
import numpy as np


def key_phrase_finder(list_of_important_phrases, list_of_extracted_phrases):
    listing = [ ]
    PhraseChecker = None

    res = str(list_of_extracted_phrases).split()

    for important_word in list_of_important_phrases:
        names = res
        names2 = [ word for word in names if important_word in word ]
        isnot_empty = np.array(names2).size > 0

        if isnot_empty == True:
            listing = np.append(listing, names2)

        else:
            listing = listing

    if np.array(listing).size > 0:
        PhraseChecker = True

    else:
        PhraseChecker = False

    return listing, PhraseChecker


def email_response(name, critical_phrase_list, list_of_extracted_phrases, AWS_Comprehend_Sentiment_Dump):
    # Function Constants
    SENDER_NAME = 'Place your name here'

    # --- Check for the sentiment of the message and find dominant sentiment score ---
    Sentiment_finder = find_max_sentiment(AWS_Comprehend_Sentiment_Dump)
    overwhelming_sentiment = Sentiment_finder[ 0 ]
    overwhelming_sentiment_score = Sentiment_finder[ 1 ]

    # --- Check for article critical phrases ---
    Phrase_Matcher_Article = key_phrase_finder(critical_phrase_list, list_of_extracted_phrases)
    Matched_Phrases_Article = Phrase_Matcher_Article[ 0 ]
    Matched_Phrases_Checker_Article = Phrase_Matcher_Article[ 1 ]

    # --- Check for project phrases ---
    Phrase_Matcher_Project = key_phrase_finder([ 'github', 'git', 'Git',
                                                 'GitHub', 'projects',
                                                 'portfolio', 'Portfolio' ],
                                               list_of_extracted_phrases)
    Matched_Phrases_Project = Phrase_Matcher_Project[ 0 ]
    Matched_Phrases_Checker_Project = Phrase_Matcher_Project[ 1 ]

    # --- Check for C.V phrases ---
    Phrase_Matcher_CV = key_phrase_finder([ 'C.V', 'resume', 'Curriculum Vitae',
                                            'Resume', 'CV' ],
                                          list_of_extracted_phrases)
    Matched_Phrases_CV = Phrase_Matcher_CV[ 0 ]
    Matched_Phrases_Checker_CV = Phrase_Matcher_CV[ 1 ]

    # --- Generate standard responses ---
    # === DO NOT MODIFY THIS TEXT FOR THE PURPOSE OF PREDICT ASSESSMENT ===
    Greetings_text = f'Good day {name},'

    CV_text = 'I see that you mentioned my C.V in your message. \
               I am happy to forward you my C.V in response. \
               If you have any other questions or C.V related queries please do get in touch. '

    Project_Text = 'The projects I listed on my site only include \
                    the ones not running in production. I have \
                    several other projects that might interest you.'

    Article_Text = 'In your message you mentioned my blog posts and data science articles. \
                   I have several other articles published in academic journals. \
                   Please do let me know if you are interested - I am happy to forward them to you'

    Negative_Text = f'I see that you are unhappy in your response. \
                    Can we please set up a session to discuss why you are not happy, \
                    be it with the website, my personal projects or anything else. \
                    \n\nLooking forward to our discussion. \n\nKind Regards, \n\nMy Name'

    Neutral_Text = f'Thank you for your email. Let me know if you need any additional information.\
                    \n\nKind Regards, \n\n{SENDER_NAME}'

    Farewell_Text = f'Thank you for your email.\n\nIf there is anything else I can assist \
                     you with please let me know and I will set up a meeting for us to meet\
                     in person.\n\nKind Regards, \n\n{SENDER_NAME}'
    # =====================================================================

    # --- Email Logic ---
    if overwhelming_sentiment == 'POSITIVE':
        if ((Matched_Phrases_Checker_CV == True) & \
                (Matched_Phrases_Checker_Article == True) & \
                (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, CV_text, Article_Text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) & \
              (Matched_Phrases_Checker_Article == False) & \
              (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, CV_text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) & \
              (Matched_Phrases_Checker_Article == False) & \
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, CV_text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) & \
              (Matched_Phrases_Checker_Article == True) & \
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) & \
              (Matched_Phrases_Checker_Article == False) & \
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) & \
              (Matched_Phrases_Checker_Article == False) & \
              (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) & \
              (Matched_Phrases_Checker_Article == True) & \
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, CV_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        else:
            mytuple = (Greetings_text, Project_Text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

    elif overwhelming_sentiment == 'NEGATIVE':
        mytuple = (Greetings_text, Negative_Text)
        Text = "\n \n".join(mytuple)

    else:
        mytuple = (Greetings_text, Neutral_Text)
        Text = "\n \n".join(mytuple)

    return Text