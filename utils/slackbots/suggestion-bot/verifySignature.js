/* ******************************************************************************
 * Signing Secret Varification
 * 
 * Signing secrets replace the old verification tokens. 
 * Slack sends an additional X-Slack-Signature HTTP header on each HTTP request.
 * The X-Slack-Signature is just the hash of the raw request payload 
 * (HMAC SHA256, to be precise), keyed by your app’s Signing Secret.
 *
 * More info: https://api.slack.com/docs/verifying-requests-from-slack
 *
 * Tomomi Imura (@girlie_mac)
 * ******************************************************************************/

const crypto = require('crypto');
const timingSafeCompare = require('tsscmp');

const isVerified = (req) => { 
  const signature = req.headers['X-Slack-Signature'];
  const timestamp = req.headers['X-Slack-Request-Timestamp'];
  const hmac = crypto.createHmac('sha256', process.env.SLACK_SIGNING_SECRET);
  const [version, hash] = signature.split('=');
  // Check if the timestamp is too old
  const fiveMinutesAgo = ~~(Date.now() / 1000) - (60 * 5);
  if (timestamp < fiveMinutesAgo) return false;
  hmac.update(`${version}:${timestamp}:${req.body}`);
  const hex = hmac.digest('hex');
  return timingSafeCompare(hex, hash);
}; 
  
module.exports = { isVerified };