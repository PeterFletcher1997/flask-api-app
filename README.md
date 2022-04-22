# Flask-Lightspeed-App

### Receives incoming webhooks from lightpeed ecom and posts re-formated json to ligthspeed retail. 
The purpose of this app is to assist stores with the lightspeed omnichannel solution that are having issues with Quebec orders not leaving the lightpseed ecom inventory. 
</br></br>
#### Required evironment variables for the contianer:

| Variable      | Function  | Required |
|---------------|-----------|----------|
| SEND_URL      | url that the app will send re-formated jsons to | Yes |
| FROM_EMAIL    | email that will act as the 'sender' to notify new orderes being uploaded to LS | Yes | 
| FROM_PASS     | app password used to log into 'sender', will default to FROM_EMAIL | Yes |
| TO_EMAIL      | email that will recive updates as new orders are uploaded to LS | No|
| CLIENT_ID     | client ID from lightspeed retail | Yes |
| CLIENT_SECRET | client Secret from lightspeed retail | Yes | 
| REFRESH_TOKEN | refresh token from lightspeed retail | Yes | 


