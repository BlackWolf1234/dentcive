source .venv/bin/activate
pip install --upgrade pip     
pip install -r requirements.txt  
reflex init
reflex export --frontend-only
rm -rf public
unzip frontend.zip -d public
touch public/.nojekyll
rm -f frontend.zip
deactivate
