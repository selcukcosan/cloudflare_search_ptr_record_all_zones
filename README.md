This Python scripts search and find the FQDN DNS names for specified IP address (PTR) record in all DNS zones in Cloudflare.
You need to get Beaarer Token ID to search and retrieve the records. 
**_NOTE:_**  `output` The script search first 500 zones by default `zones?page=1&per_page=500`

If you have more than 500 DNS zones, you need to run the script again after change the page number `zones?page=X&per_page=500`
