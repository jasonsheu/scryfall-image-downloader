import requests
import time
import os

SET_CODE = 'tla'
#make directories for set if it doesnt exist 

#make directories for set if it doesnt exist 

os.makedirs(f'images/{SET_CODE}', exist_ok=True)
for rarity in ['common', 'uncommon', 'rare', 'mythic']:
    #make directories for rarity if it doesnt exist
    os.makedirs(f'images/{SET_CODE}/{rarity}', exist_ok=True)
    #get all cards in the draft set, change the query for other sets
    r = requests.get(f"https://api.scryfall.com/cards/search?q=e:{SET_CODE}+cn>=1+cn<=286+r:{rarity}").json()
    #respect api rules
    time.sleep(0.1)
    print('got', r.get('total_cards'), 'cards of rarity', rarity)
    cards = r.get('data')
    #iterate through all cards for current rarity
    for card in cards:
        cardname = card.get('name')
        
        #handle mdfc cards and // in names
        if '/' in cardname:
            cardname = cardname.replace('/', '_')       
        color_mapping = {
                'W' : '1',
                'U' : '2',
                'B' : '3',
                'R' : '4',
                'G' : '5'
        }
        #special handling of MDFC cards to get both faces 
        if card.get('card_faces') is not None:
            # for color mapping of mdfc cards, use color of first face to keep the cards together in the file explorer
            first = card.get('card_faces')[0]
            color = first.get('color')
            if color is None or len(color) == 0:
                color_code = '0'
            elif len(color) > 1:
                color_code = '6'
            else:
                color_code = color_mapping.get(color[0])
            for idx, cardface in enumerate(card.get('card_faces')):
                image_url = cardface.get('image_uris').get('normal')
                save_path = f'images/{SET_CODE}/{rarity}/{color_code}_{cardname}_{idx}.jpg'
                response = requests.get(image_url)
                time.sleep(0.2)
                if response.status_code == 200:    
                    with open (save_path, 'wb') as file:
                        file.write(response.content)
                    print(f'downloaded image for {cardname}')
                else:
                    print(f"Failed to download image for {cardname}")
        #regular card case 
        else:
            #create color identity mapping to group images by color in file explorer, remove if not interested in sorty by color and only by name
            color = card.get('color_identity')
            if color is None or len(color) == 0:
                color_code = '0'
            elif len(color) > 1:
                color_code = '6'
            else:
                color_code = color_mapping.get(color[0])
           
            #get image url and download image
            image_url = card.get('image_uris').get('normal')
            save_path = f'images/{SET_CODE}/{rarity}/{color_code}_{cardname}.jpg'
            response = requests.get(image_url)
            time.sleep(0.2)
            if response.status_code == 200:    
                with open (save_path, 'wb') as file:
                    file.write(response.content)
                print(f'downloaded image for {cardname}')
            else:
                print(f"Failed to download image for {cardname}")
