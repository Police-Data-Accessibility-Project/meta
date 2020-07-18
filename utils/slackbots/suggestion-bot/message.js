const axios = require('axios'); 
const qs = require('qs');
const suggestions = require('./suggestions');

const API_URL = 'https://slack.com/api';

/*
 *  Handling DM messages
 */


/* Calling the chat.postMessage method to send a message */

const send = async(channel, text, thread) => {
  let message = '';
  let suggested = new Set();
  text = text.toLowerCase();
  for (let channelId in suggestions) {
    for (let i in suggestions[channelId]['keywords']) {
      let keyword = (suggestions[channelId]['keywords'][i]);
      if (text.includes(keyword.toLowerCase())) {
        suggested.add(channelId);
      }
    }
  }
  suggested = Array.from(suggested);
  if (suggested.length > 0){
    let suggestion_text = "• <#C014E2JGJAJ>\n";
    for (let i in suggested) {
      suggestion_text += `• <#${suggested[i]}>\n`;
    }
    message = `:wave: Welcome! Based on your introduction, we have a few suggestions for rooms to join:\n ${suggestion_text}`
  }
  else {
    message = `:wave: Welcome! We don't have any specific channel suggestions for you yet, so maybe start with <#C014E2JGJAJ>.`
  }
  const args = {
    token: process.env.SLACK_BOT_TOKEN,
    channel: channel,
    thread_ts: thread,
    text: message
  };

  let result;

  try {
      result = await axios.post(`${API_URL}/chat.postMessage`, qs.stringify(args));
      return result;
  } catch (e) {

      return e;
  }
};


module.exports = { send };
