import csv
import json

# Open the CSV
f = open( './reddit-data-final.csv', 'rU' )
# Change each fieldname to the appropriate field name. I know, so difficult.
reader = csv.DictReader( f, fieldnames = ( "Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair", "Text", "Stickied", "Over 18", "Is Video"))
# Parse the CSV into JSON
out = json.dumps( [ row for row in reader ] )
print("JSON parsed!")
# Save the JSON
f = open( './reddit-data-final.json', 'w')
f.write(out)
print("JSON saved!")
