set -o errexit

pip install -r requirements.txt

cd frontend/
npm install -D webpack-cli
npm run build

cd ..
python manage.py collectstatic --noinput
python manage.py migrate