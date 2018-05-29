echo 'Pull update code from branch master...'
git pull origin master 

echo 'restart PM2...' 
pm2 restart api-ki-42

echo 'API IS LIVE'

