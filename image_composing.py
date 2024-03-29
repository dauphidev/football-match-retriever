import match_scraping as ms
from datetime import date
from PIL import Image, ImageDraw, ImageFont

#FONT_TYPE = ImageFont.truetype("OpenSans-Bold.ttf",40)
#HEADER_FONT_TYPE = ImageFont.truetype("OpenSans-Bold.ttf",20)
#FOOTER_FONT_TYPE = ImageFont.truetype("OpenSans-Bold.ttf",20)

# PIL text style
FONT_TYPE = ImageFont.load_default()
HEADER_FONT_TYPE = ImageFont.load_default()
FOOTER_FONT_TYPE = ImageFont.load_default()
FONT_COLOR = (255,255,255)
FOOTER_MESSAGE = "dauphinetdev"
DEF_BACKGROUND = "logos/midnight_blue.jpg"

def generate_image (match_strings, date):

    logo_dict = {}
    background = Image.open(DEF_BACKGROUND)
    image_text = ImageDraw.Draw(background)

    n = 0
    n_consec_comp = 0
    current_competition = ""

    # Competition area is 200x100 (with x height)
    for (m,c) in match_strings:

        diff_comp = c != current_competition

        if diff_comp:
            
            logo = logo_dict.get(c)
            if logo is None:
                logo = get_comp_logo(c)
                logo_dict[c] = logo
                print(f"[LOG: Cached the {c} logo]")

            # Pasting the logo, centered
            logo_area = (400, 100 + 100*n, 600, 200 + 100*n)
            background.paste(logo, logo_area)
            
            current_competition = c
            n_consec_comp = 0
            n += 1
        else:
            n_consec_comp += 1

        # Writing the match string
        text_pos = (50, 100 + 100*n)
        image_text.text( xy = text_pos, text = m, fill = FONT_COLOR, font = FONT_TYPE)

        n += 1

    # Footer Text
    image_text.text( xy=(450,950), text=FOOTER_MESSAGE, fill=FONT_COLOR, font=FOOTER_FONT_TYPE)
    github_logo = Image.open("logos/github_logo.png")
    background.paste(github_logo, (405,947), mask=github_logo)
    
    # Header Text
    image_text.text( xy=(200,30), text="Today, on {}, we've got the following matches:".format(date), fill=FONT_COLOR, font=HEADER_FONT_TYPE)
  
    return background
        
def get_comp_logo (competition):
    
    if competition == "Spanish La Liga":
        return Image.open("logos/laliga2.jpg")
    elif competition == "Premier League":
        return Image.open("logos/premierleague2.jpg")
    elif competition == "Portuguese Primeira Liga":
        return Image.open("logos/primeiraliga.jpg")
    elif competition == "Spanish Copa del Rey":
        return Image.open("logos/copadelrey.jpg")
    elif competition == "Italian Serie A":
        return Image.open("logos/seriea.png")
    elif competition == "Italian Coppa Italia":
        return Image.open("logos/coppaitalia.png")
    elif competition == "The FA Cup":
        return Image.open("logos/facup.jpg")
    elif competition == "German Bundesliga":
        return Image.open("logos/bundesliga.png")
    elif competition == "French Ligue 1":
        return Image.open("logos/ligue1.png")
    else:
        return Image.open("logos/laliga2.jpg")

def print_text (teams):
    curr_date = date.today().strftime("%B %d") + "th"
    matches = ms.get_matches_by_team(teams)
    print(f"Today, on {curr_date}, we've got the following matches:")
    for (m,c) in matches:
        print(m,c)
    
def get_image (teams):
    curr_date = date.today().strftime("%B %d") + "th"
    matches = ms.get_matches_by_team(teams)
    result = generate_image(matches, curr_date)
    result.save(f"generated_images/{curr_date}.jpg")
