source .venv/bin/activate
pip install --upgrade pip     
pip install requirements.txt  
reflex init
reflex export --frontend-only
rm -f public
unzip frontend.zip -d public
rm -f frontend.zip
deactivate   