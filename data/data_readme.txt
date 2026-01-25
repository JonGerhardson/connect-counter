Code was changed on Jan. 25, 2026 after noticing some sites may have not been scraped correctly. 

The camera counts load via a javascript animation that rapidly counts the text up, like a ticker. Previously the script was hardcoded to wait 5 seconds to let this animation finish, which seems to have caused some abnormalities. 

The script now checks that number twice with a time interval between to validate the number hasn't changed before logging it. 

Please be aware of this issue if analyzing data for September 12, 2025 to January 19, 2026. Generally, the trend seems to be for the number of cameras to go up over time. A decline followed by an increase two weeks later was probably a bad scrape.  
