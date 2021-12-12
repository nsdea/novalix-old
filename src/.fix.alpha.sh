echo 'Fixing Slash Commands...'

curl --location --request PUT 'https://discord.com/api/v9/applications/795743605221621782/commands' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bot ODI2NDAxOTI3OTMxMzYzMzU4.YGL8xQ.tr2A2av5FuuGSCE-Di40FEfKwiI' \
--data-raw '[]'

echo .
echo 'Done.'
echo 'WAIT before running this script again! You might get ratelimited.'