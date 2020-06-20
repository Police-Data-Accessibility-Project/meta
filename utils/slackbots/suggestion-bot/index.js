/* 
 * Slack Suggestion Bot
 * Send suggestions on channels to join based on keywords in introductions
 * June 19, 2020
 *
 * This is written in Vanilla-ish JS with Express (No Slack SDK or Framework)
 * To see how this can be written in Bolt, https://glitch.com/edit/#!/apphome-bolt-demo-note
 */

const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios'); 
const qs = require('qs');

const signature = require('./verifySignature');
const message = require('./message');
const JsonDB = require('node-json-db');
const db = new JsonDB('introductions7', true, false);  // TODO: figure out a sensible name

const app = express();

const apiUrl = 'https://slack.com/api';

const channelId = 'G015JU147RC';  // TODO: replace with #_introduceyourself channel id
// This one is a private channel used for testing.

/*
 * Parse application/x-www-form-urlencoded && application/json
 * Use body-parser's `verify` callback to export a parsed raw body
 * that you need to use to verify the signature
 *
 * Forget this if you're using Bolt framework or either SDK, otherwise you need to implement this by yourself to verify signature!
 */

const rawBodyBuffer = (req, res, buf, encoding) => {
  if (buf && buf.length) {
    req.rawBody = buf.toString(encoding || 'utf8');
  }
};

app.use(bodyParser.urlencoded({verify: rawBodyBuffer, extended: true }));
app.use(bodyParser.json({ verify: rawBodyBuffer }));


/*
 * Endpoint to receive events from Events API.
 * managed from https://api.slack.com/apps/A015Q3Q5HS9/event-subscriptions?
 */

app.post('/slack/events', async(req, res) => {
  console.log("hit the event endpoint");
  switch (req.body.type) {
      
    case 'url_verification': {
      // verify Events API endpoint by returning challenge if present
      res.send({ challenge: req.body.challenge });
      break;
    }
      
    case 'event_callback': {
      // Verify the signing secret
      if (!signature.isVerified(req)) {
        res.sendStatus(404);
        return;
      } 
      
      // Request is verified --
      else {
        
        const {type, user, channel, tab, text, bot_id, event_ts, client_msg_id} = req.body.event;
        
        if(type === 'message') {
          
          if(channel == channelId && typeof bot_id == 'undefined' && typeof client_msg_id !== 'undefined') { 
            // this isn't a message from a bot and it isn't a meta-message from slack            
            
            try {
              const data = db.getData(`/${client_msg_id}`)
              // const data = db.getData(`/${user}/data`);
              // console.log("We've already messaged this user. Don't say hello again.");
              console.log("We've already messaged this message. Don't say hello again.");
            } catch(error) {
              // haven't seen this user before
              // DM back to the user
              const timestamp = new Date();
              // db.push(`/${user}`, timestamp, true);
              db.push(`/${client_msg_id}`)
              message.send(channel, text, event_ts);
            }; 

          }
        }
       
      }
      break;
    }
    default: { res.sendStatus(404); }
  }
});



/* Running Express server */
const server = app.listen(5000, () => {
  console.log('Express web server is running on port %d in %s mode', server.address().port, app.settings.env);
});


app.get('/', async(req, res) => {
  res.send('There is no web UI for this code sample. To view the source code, click "View Source"');
});