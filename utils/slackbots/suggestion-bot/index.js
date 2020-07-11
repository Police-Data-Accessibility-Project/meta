// const AWS = require('aws-sdk');
const axios = require('axios');
const qs = require('qs');

const signature = require('./verifySignature');
const message = require('./message');

const apiUrl = 'https://slack.com/api';
const channelId = 'C013XMN8RL3';

/**
 * Demonstrates a simple HTTP endpoint using API Gateway. You have full
 * access to the request and response payload, including headers and
 * status code.

 */
exports.handler = async (event, context) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    let body;
    let statusCode = '200';
    const headers = {
        'Content-Type': 'application/json',
    };

    try {
        switch (event.httpMethod) {
            case 'POST':
            console.log("hit the event endpoint");
            let event_body = JSON.parse(event.body);
            console.log("switch case on type");
            console.log("type: " + event_body.type);
                
            switch (event_body.type) {

              case 'url_verification': {
                // verify Events API endpoint by returning challenge if present
                console.log("sending back the challenge");
                body = { "challenge": event_body.challenge };
                break;
              }
                
              case 'event_callback': {
                // Verify the signing secret
                if (!signature.isVerified(event)) {
                  console.log("failed to verify signature");
                  throw new Error("Unverified signature. Does this message have required metadata from Slack? Have secrets been exported?");
                }
                console.log("Request is verified");
                const {type, user, channel, tab, text, bot_id, ts, client_msg_id, thread_ts} = event_body.event;
                
                if(type === 'message') {
                  
                  if(channel == channelId && typeof bot_id == 'undefined' && typeof client_msg_id !== 'undefined'
                    && (typeof thread_ts == 'undefined' || thread_ts == ts)) { 
                    // this isn't a message from a bot and it isn't a meta-message from slack
                    console.log(text);
                    let result = await message.send(channel, text, ts);
                    console.log(result);

                  }
                 
                }
                else if (type === 'app_home_opened'){
                  const args = {
                    "token": process.env.SLACK_BOT_TOKEN,
                    "user_id": user,
                    "view": JSON.stringify({ 
                         "type":"home",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": ":wave: This app gives suggestions on which channels to join based on volunteers' introductions. It's just a simple keyword match, this app doesn't persist any data about you."
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "If you'd like to contribute, you'll find the code <https://github.com/Police-Data-Accessibility-Project/Police-Data-Accessibility-Project/tree/develop/utils/slackbots/suggestion-bot|here>, please feel free to make a PR. To get it deployed, for now you'll have to reach out to @Katie since she's hosting it."
                                    }
                                },
                                {
                                    "type": "context",
                                    "elements": [
                                        {
                                            "type": "plain_text",
                                            "text": "Author: @Katie\nAdmin: @Zach - Slack Admin "
                                        }
                                    ]
                                }
                            ]
                      })
                  };
                  let result = await axios.post(`${apiUrl}/views.publish`, qs.stringify(args));
                }
                break;
              }
              default: 
                throw new Error(`Unsupported type "${event_body.type}"`);
            }
                break;
            default:
                throw new Error(`Unsupported method "${event.httpMethod}"`);
        }
    } catch (err) {
        statusCode = '400';
        body = err.message;
    } finally {
        body = JSON.stringify(body);
    }

    return {
        statusCode,
        body,
        headers,
    };
};
