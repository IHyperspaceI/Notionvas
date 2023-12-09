# Notionvas
*This makes use of the Canvas LMS API as well as the Notion API to plug Canvas assignments into Notion*

## General Instructions  
1. Download the folder  
2. Follow setup instructions below  
3. Run the Python script every time you want to update the database  

**Notes**  
- If the files are still in a folder together and the preferences are set up correctly, you should just be able to run the Python script and it will display your assignments in the Notion database!  
- If there are any problems, please contact me on Discord @ihyperspacei or open an issue here

## Setup
Create a notion database with the following, in the same order:  
- Name (title)  
- Class (text)  
- Date (date)  
- Completed (checkbox)  
- Points (number)  
- AutoUpdate (checkbox)

These are case sensitive, example below:
![Notion Database.png](Docs%2FNotion%20Database.png)


### Getting The Information
**Canvas Link**
1. Literally just copy the base url for your Canvas access (e.g. xx.instructure.com)  
2. In UserPreferences.json, set the value of canvas_url to the link copied (should replace <URL>)

**Canvas Token/Key**
1. Navigate to your Canvas dashboard -> profile -> settings  
2. Scroll to Approved Integrations and add new access token

![Canvas Integrations Window.png](Docs%2FCanvas%20Integrations%20Window.png)
3. Copy and save token ID (you can't see this again without regenerating it)
4. In UserPreferences.json, set the value of canvas_key to the token copied (should replace <KEY>)

**Notion Database ID**
1. Log into Notion on a web browser
2. Navigate to your database page
3. Copy the string of characters in the URL from the / to the ?  
   - More info here: https://developers.notion.com/reference/retrieve-a-database#:~:text=To%20find%20a%20database%20ID,a%2032%20characters%20alphanumeric%20string  
4. In UserPreferences.json, set the value of notion_database_id to the string copied (should replace <DATABASE_ID>)

**Notion Token**  
1. Navigate to https://www.notion.so/my-integrations/
2. Create new integration
3. Enter the required fields
4. Copy the token
5. In UserPreferences.json, set the value of notion_token to the token copied (should replace <TOKEN>)