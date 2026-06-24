# main.py
from database import Database
#from collecte.collect_commune import peupler_communes
#from collecte.collect_ehpad import peupler_ehpad

def run_pipeline():
    db = Database()
    print("Début de la collecte...")
    
    # 1. On remplit le pivot ( avant tout)
    #peupler_communes(db)
    
    # 2. On remplit les typologies
    #peupler_ehpad(db)
    
    db.close()
    print(" Pipeline terminé.")

if __name__ == "__main__":
    run_pipeline()
    