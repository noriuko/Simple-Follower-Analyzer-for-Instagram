import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# --- CUSTOM UI WIDGETS ---

class GradientButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        # Colors: Instagram Blue (#0095f6) to Purple (#833AB4)
        self.color1 = "#0095f6"
        self.color2 = "#833AB4"
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self._draw_gradient()
        self._draw_text()

    def _hex_to_rgb(self, hex_col):
        return tuple(int(hex_col[i:i+2], 16) for i in (1, 3, 5))

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def _draw_gradient(self):
        r1, g1, b1 = self._hex_to_rgb(self.color1)
        r2, g2, b2 = self._hex_to_rgb(self.color2)

        # Draw vertical lines to simulate gradient
        for i in range(self.width):
            r = int(r1 + (r2 - r1) * (i / self.width))
            g = int(g1 + (g2 - g1) * (i / self.width))
            b = int(b1 + (b2 - b1) * (i / self.width))
            color = self._rgb_to_hex((r, g, b))
            self.create_line(i, 0, i, self.height, fill=color)

    def _draw_text(self):
        self.create_text(self.width/2, self.height/2, text=self.text, fill="white", 
                         font=("Segoe UI", 10, "bold"))

    def _on_click(self, event):
        self.move(tk.ALL, 1, 1) # Press effect
        self.update()
        self.after(100, lambda: self.move(tk.ALL, -1, -1))
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.config(cursor="hand2")

    def _on_leave(self, event):
        self.config(cursor="")

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, variable, command=None, width=50, height=26, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg="white", **kwargs)
        self.variable = variable
        self.command = command
        self.width = width
        self.height = height
        
        # Colors
        self.on_color = "#00d26a"  # Green
        self.off_color = "#ff4d4d" # Red
        self.knob_color = "white"
        
        self.bind("<Button-1>", self._toggle)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
        
        self._draw()

    def _draw(self):
        self.delete("all")
        state = self.variable.get()
        
        # Draw Background Pill
        fill_color = self.on_color if state else self.off_color
        
        # Rounded rectangle simulation
        radius = self.height / 2
        self.create_oval(0, 0, self.height, self.height, fill=fill_color, outline="")
        self.create_oval(self.width-self.height, 0, self.width, self.height, fill=fill_color, outline="")
        self.create_rectangle(radius, 0, self.width-radius, self.height, fill=fill_color, outline="")

        # Draw Knob
        padding = 3
        knob_size = self.height - (padding * 2)
        
        if state:
            x = self.width - padding - knob_size
        else:
            x = padding
            
        self.create_oval(x, padding, x+knob_size, padding+knob_size, fill=self.knob_color, outline="")

    def _toggle(self, event):
        self.variable.set(not self.variable.get())
        self._draw()
        if self.command:
            self.command()


# --- MAIN APP ---

class InstagramCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Follower Analyzer v1.1.0")
        self.root.geometry("550x850")
        self.root.configure(bg="#fafafa")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

# --- FAMOUS ACCOUNTS DATABASE ---
        self.famous_accounts = {
            # --- USER ADDED / BULGARIAN SPECIFIC ---
            'donbrutar', 'hyperkong_', 'fen.sektor', '4a1axd', 'bobby',

            # --- POP ICONS & MUSIC ---
            'taylorswift', 'arianagrande', 'justinbieber', 'selenagomez', 'rihanna',
            'beyonce', 'drake', 'billieeilish', 'edsheeran', 'theweeknd',
            'ladygaga', 'shakira', 'dualipa', 'brunomars', 'adele',
            'cardib', 'nickiminaj', 'mileycyrus', 'katyperry', 'shawnmendes',
            'eminem', 'coldplay', 'postmalone', 'lizzobeeating', 'demilovato',
            'harrystyles', 'niallhoran', 'liampayne', 'louist91', 'zayn',
            'badbunnypr', 'jbalvin', 'maluma', 'daddy_yankee', 'karolg', 'anitta',
            'rosalia.vt', 'sabrinacarpenter', 'oliviarodrigo', 'sza', 'dojacat',
            'travisscott', 'kendricklamar', 'megan_thee_stallion', 'jackharlow',
            'camilacabello', 'khalid', 'halsey', 'imagine_dragons', 'maroon5',
            'samsmith', 'eltonofficial', 'madonna', 'cher', 'celinedion',
            'jenniferlopez', 'mariah_carey', 'britneyspears', 'pink', 'aliciakeys',
            'lilnasx', 'charlieputh', 'jonasbrothers', 'nickjonas', 'joejonas',
            'future', 'lilbaby', 'gunna', 'playboicarti', 'liluzivert', '21savage',
            'asaprocky', 'tylerthecreator', 'frankocean', 'weeknd', 'lanadelrey',

            # --- K-POP ---
            'blackpinkofficial', 'roses_are_rosie', 'jennierubyjane', 'lalalalisa_m', 'sooyaaa__',
            'bts.bighitofficial', 'jin', 'agustd', 'jm', 'thv', 'jungkook.97', 'rkive', 'uarmyhope',
            'twicetagram', 'got7.with.igot7', 'straykids_official', 'skzoo_official',
            'aespa_official', 'redvelvet.smtown', 'nct', 'nct127', 'txt_bighit',
            'enhypen', 'itzy.all.in.us', 'newjeans_official', 'ivestarship',

            # --- HOLLYWOOD & ACTORS ---
            'therock', 'vindiesel', 'kevinhart4real', 'willsmith', 'chrishemsworth',
            'robertdowneyjr', 'tomholland2013', 'zendaya', 'timotheechalamet',
            'ryanreynolds', 'blakelively', 'gal_gadot', 'wonderwoman',
            'scarlettjohanssonworld', 'jasonmomoa', 'hughjackman', 'prattprattpratt',
            'leonardodicaprio', 'tomcruise', 'markruffalo', 'chrisevans', 'paulrudd',
            'milliebobbybrown', 'finnwolfhardofficial', 'sadiesink_', 'noahschnapp',
            'gatenm123', 'calebmclaughlin', 'jennaortega', 'florencepugh',
            'anyataylorjoy', 'henrycavill', 'austinbutler', 'margotrobbie',
            'jenniferaniston', 'courteneycoxofficial', 'lisakudrow', 'mleblanc',
            'mattyperry4', 'davidschwimmer', 'reeseaterspoon', 'nicolekidman',
            'priyankachopra', 'deepikapadukone', 'akshaykumar', 'amitabhbachchan',
            'shahrukhkhan', 'ranveersingh', 'katrinakaif', 'aliaabhatt', 'shraddhakapoor',

            # --- MODELS & FASHION ---
            'kendalljenner', 'gigihadid', 'bellahadid', 'caradelevingne',
            'emrata', 'irinashayk', 'romeestrijd', 'winnieharlow', 'elsahosk',
            'haileybieber', 'ashleygraham', 'naomicampbell', 'tyrabanks', 'cindycrawford',
            'heidiklum', 'adrianalima', 'gisele', 'mirandakerr', 'rosiehw',
            'karliekloss', 'candicesswanepoel', 'taylor_hill', 'josephineskriver',
            'sarasampaio', 'laisribeiro', 'jastookes', 'marthahunt',
            'victoriassecret', 'voguemagazine', 'harpersbazaarus', 'elleusa',
            'gucci', 'louisvuitton', 'chanelofficial', 'dior', 'prada',
            'versace', 'balenciaga', 'ysl', 'fendi', 'givenchy',
            'burberry', 'hermes', 'valentino', 'armani', 'dolcegabbana',
            'calvinklein', 'tomford', 'ralphlauren', 'michaelkors', 'off____white',

            # --- THE KARDASHIAN/JENNER CLAN ---
            'kimkardashian', 'khloekardashian', 'kourtneykardash', 'krisjenner',
            'kyliejenner', 'scottdisick', 'robkardashianofficial',
            'kyliecosmetics', 'kkwbeauty', 'skims', 'goodamerican', 'poosh',

            # --- ATHLETES (Football, NBA, F1, Combat) ---
            'cristiano', 'leomessi', 'neymarjr', 'k.mbappe', 'paulpogba',
            'davidbeckham', 'sergioramos', 'toni.kr8s', 'hazardeden_10',
            'garethbale11', 'mosalah', 'luissuarez9', 'lewandowski',
            'erling.haaland', 'vinijr', 'pedri', 'judebellingham', 'ziyech',
            'zlatanibrahimovic',
            'kingjames', 'stephencurry30', 'kevindurant', 'giannis_an34',
            'russwest44', 'jameshardenstore', 'kawhileonard', 'kyrieirving',
            'lameloball', 'klaythompson', 'damianlillard', 'lukadoncic',
            'tom_brady', 'odell', 'patrickmahomes', 'traviskelce',
            'serenawilliams', 'rogerfederer', 'rafaelnadal', 'djokernole',
            'usainbolt', 'simonebiles', 'tigerwoods', 'michaelphelps',
            'lewishamilton', 'maxverstappen1', 'charles_leclerc', 'landonorris',
            'danielricciardo', 'carlossainz55', 'georgerussell63', 'schecoperez',
            'conormcgregor', 'khabib_nurmagomedov', 'floydmayweather', 'canelo',
            'miketyson', 'jakepaul', 'loganpaul', 'francisngannou', 'adesanya',

            # --- SPORTS TEAMS & ORGS ---
            'fcbarcelona', 'realmadrid', 'psg', 'manchesterunited', 'manchestercity',
            'liverpoolfc', 'chelseafc', 'arsenal', 'juventus', 'acmilan', 'fcbayern',
            'inter', 'atleticodemadrid', 'borussiadortmund', 'galatasaray',
            'championsleague', 'fifaworldcup', 'premierleague', 'laliga', 'nba', 'nfl', 'ufc', 'f1',
            '433', 'goal', 'espnfc', 'brfootball', 'houseofhighlights', 'sportscenter',

            # --- MEME ACCOUNTS (Big Traffic) ---
            '9gag', 'fuckjerry', 'daquan', 'memezar', 'pubity', 'sarcasm_only',
            'ladbible', 'barstoolsports', 'worldstar', 'hoodclips', 'epicfunnypage',
            'tank.sinatra', 'thefatjewish', 'beige.cardigan', 'dudewithsign',
            'shitheadsteve', 'middleclassfancy', 'betches', 'mytherapistsays',
            'so.shauna', 'crazybitchprobs', 'bitch', 'trevornoah', 'kalesalad',
            'subwaycreatures', 'kidsgettinghurt', 'influencersinthewild',

            # --- PETS & ANIMALS ---
            'jiffpom', 'nala_cat', 'itsdougthepug', 'marutaro', 'realgrumpycat',
            'tuckerbudzyn', 'juniperfoxx', 'venustwofacecat', 'tunameltsmyheart',
            'pumpkintheraccoon', 'loki', 'hamlet_the_piggy', 'iamlilbub',
            'smoothiethecat', 'marniethedog', 'norbertthedog', 'tecuaniventura',
            'dean.schneider', 'blackjaguarwhitetiger', 'natgeowild', 'animalplanet',

            # --- YOUTUBERS / STREAMERS / INFLUENCERS ---
            'mrbeast', 'pewdiepie', 'ksi', 'ishowspeed', 'kaicenat', 'adinross',
            'pokimanelol', 'xqc', 'ninja', 'dream', 'tommyinnit', 'markiplier',
            'jacksepticeye', 'miniminter', 'wroetoshaw', 'zerkaa', 'behzinga', 'vikkstagram',
            'khaby00', 'charlidamelio', 'addisonraee', 'jamescharles', 'emmachamberlain',
            'daviddobrik', 'zachking', 'camerondallas', 'nashgrier', 'lelepons',
            'hannahstocking', 'brentrivera', 'larray', 'avani', 'dixiedamelio',
            'noahbeck', 'brycehall', 'joshuariau', 'nessabarrett', 'bellapoarch',
            'inanna',

            # --- BRANDS (Tech, Food, Lifestyle) ---
            'apple', 'google', 'microsoft', 'samsung', 'sony', 'playstation', 'xbox', 'nintendo',
            'tesla', 'spacex', 'nasa', 'natgeo', 'nationalgeographic', 'discovery',
            'netflix', 'hulu', 'disneyplus', 'hbomax', 'primevideo', 'disney',
            'marvel', 'starwars', 'pixar', 'warnerbros', 'universalpictures',
            'spotify', 'applemusic', 'tiktok', 'instagram', 'youtube', 'twitter', 'facebook',
            'nike', 'adidas', 'puma', 'reebok', 'underarmour', 'newbalance', 'jordan',
            'vans', 'converse', 'supremenewyork', 'stussy', 'kith',
            'cocacola', 'pepsi', 'redbull', 'monsterenergy', 'starbucks',
            'mcdonalds', 'burgerking', 'kfc', 'subway', 'tacobell', 'chipotle',
            'wendys', 'dunkin', 'pizzahut', 'dominos', 'nutella', 'oreo',

            # --- BEAUTY & MAKEUP ---
            'sephora', 'maccosmetics', 'maybelline', 'lorealparis', 'nyxcosmetics',
            'fentybeauty', 'hudabeauty', 'anastasiabeverlyhills', 'morphebrushes',
            'urbandecaycosmetics', 'narsissist', 'tartecosmetics', 'benefitcosmetics',
            'colourpopcosmetics', 'jeffreestarcosmetics', 'nikkietutorials', 'mannymua733',

            # --- BUSINESS & LEADERS ---
            'billgates', 'elonmusk', 'jeffbezos', 'markzuckerberg', 'richardbranson',
            'oprah', 'barackobama', 'michelleobama', 'dalailama', 'malala',
            'gordonramsay', 'jamieoliver', 'nusr_et', 'saltbae', 'foodgod',
            'garyvee', 'grantcardone', 'tonyrobbins', 'daveramsey',

            # --- TRAVEL & PHOTOGRAPHY ---
            'beautifuldestinations', 'earth', 'earthpix', 'passionpassport',
            'travelandleisure', 'condenasttraveler', 'lonelyplanet',
            'muradosmann', 'chrisburkard', 'brandonwoelfel', 'humansofny',

            # --- GAMING ---
            'fortnite', 'callofduty', 'minecraft', 'leagueoflegends', 'valorant',
            'apexlegends', 'pubg', 'roblox', 'gta5', 'rockstargames',
            'easportsfifa', 'nba2k', 'fazeclan', 'tsm', '100thieves', 'cloud9'
        }
        # Variables
        self.following_path = ""
        self.followers_path = ""
        self.ignore_famous_var = tk.BooleanVar(value=True)
        self.show_fans_var = tk.BooleanVar(value=True) 

        # --- MODERN UI DESIGN ---
        
        # Main container
        main_container = tk.Frame(root, bg="#fafafa")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        # Using a gradient for the header background
        header_frame = tk.Canvas(main_container, height=70, highlightthickness=0)
        header_frame.pack(fill="x", pady=(0, 12))
        
        # Draw gradient header
        w_header = 520
        h1 = "#0095f6"
        h2 = "#833AB4"
        r1, g1, b1 = tuple(int(h1[i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(h2[i:i+2], 16) for i in (1, 3, 5))
        
        # --- FIX: Loop range matches width exactly to prevent color calculation errors ---
        for i in range(w_header): 
            r = int(r1 + (r2 - r1) * (i / w_header))
            g = int(g1 + (g2 - g1) * (i / w_header))
            b = int(b1 + (b2 - b1) * (i / w_header))
            color = '#%02x%02x%02x' % (r, g, b)
            header_frame.create_line(i, 0, i, 70, fill=color)

        header_frame.create_text(250, 35, text="Simple Follower Analyzer", 
                                font=("Segoe UI", 18, "bold"), fill="white")
        

        # File Selection Card
        file_card = tk.Frame(main_container, bg="white", relief="flat", bd=0)
        file_card.pack(fill="x", pady=(0, 10))
        file_card.configure(highlightbackground="#dbdbdb", highlightthickness=1)
        
        card_padding = tk.Frame(file_card, bg="white")
        card_padding.pack(fill="both", expand=True, padx=15, pady=12)
        
        tk.Label(card_padding, 
                text="📁 Select Your Instagram Data Files", 
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="#262626").pack(anchor="w", pady=(0, 10))

        # Following file row
        following_frame = tk.Frame(card_padding, bg="white")
        following_frame.pack(fill="x", pady=5)
        
        self.btn_following = GradientButton(following_frame, 
                                          text="📄 Select following.json",
                                          command=self.load_following,
                                          width=200,
                                          height=35)
        self.btn_following.pack(side="left", padx=(0, 12))
        
        self.lbl_following = tk.Label(following_frame, 
                                     text="No file selected",
                                     fg="#8e8e8e",
                                     bg="white",
                                     font=("Segoe UI", 9))
        self.lbl_following.pack(side="left")

        # Followers file row
        followers_frame = tk.Frame(card_padding, bg="white")
        followers_frame.pack(fill="x", pady=5)
        
        self.btn_followers = GradientButton(followers_frame,
                                          text="📄 Select followers_1.json",
                                          command=self.load_followers,
                                          width=200,
                                          height=35)
        self.btn_followers.pack(side="left", padx=(0, 12))
        
        self.lbl_followers = tk.Label(followers_frame,
                                     text="No file selected",
                                     fg="#8e8e8e",
                                     bg="white",
                                     font=("Segoe UI", 9))
        self.lbl_followers.pack(side="left")

        # Options Card
        options_card = tk.Frame(main_container, bg="white", relief="flat", bd=0)
        options_card.pack(fill="x", pady=(0, 10))
        options_card.configure(highlightbackground="#dbdbdb", highlightthickness=1)
        
        options_padding = tk.Frame(options_card, bg="white")
        options_padding.pack(fill="both", expand=True, padx=15, pady=10)
        
        # 1. Famous Checkbox replacement (Toggle)
        row1 = tk.Frame(options_padding, bg="white")
        row1.pack(fill="x", pady=2)
        
        self.switch_famous = ToggleSwitch(row1, variable=self.ignore_famous_var)
        self.switch_famous.pack(side="left", padx=(0, 10))
        
        tk.Label(row1, 
                 text="Filter out verified celebrities & famous accounts",
                 font=("Segoe UI", 10), bg="white", fg="#262626").pack(side="left")
        
        # Subtext for count
        tk.Label(options_padding,
                text=f"       ({len(self.famous_accounts)} accounts in database)",
                font=("Segoe UI", 8),
                fg="#8e8e8e",
                bg="white").pack(anchor="w", padx=(50, 0), pady=(0, 5))

        # 2. Show Fans Checkbox replacement (Toggle)
        row2 = tk.Frame(options_padding, bg="white")
        row2.pack(fill="x", pady=5)
        
        self.switch_fans = ToggleSwitch(row2, variable=self.show_fans_var)
        self.switch_fans.pack(side="left", padx=(0, 10))
        
        tk.Label(row2, 
                 text="Show 'Fans' (people who follow you but you don't follow back)",
                 font=("Segoe UI", 10), bg="white", fg="#262626").pack(side="left")

        # Compare Button
        # Gradient Button filling wider
        self.btn_compare = GradientButton(main_container,
                                        text="🔍 ANALYZE NOW",
                                        command=self.process_files,
                                        width=480, # Make it wide
                                        height=45)
        self.btn_compare.pack(pady=(0, 12))

        # Results Card
        results_card = tk.Frame(main_container, bg="white", relief="flat", bd=0)
        results_card.pack(fill="both", expand=True)
        results_card.configure(highlightbackground="#dbdbdb", highlightthickness=1)
        
        results_padding = tk.Frame(results_card, bg="white")
        results_padding.pack(fill="both", expand=True, padx=15, pady=12)
        
        tk.Label(results_padding,
                text="📊 Analysis Results",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="#262626").pack(anchor="w", pady=(0, 8))

        # Results text area
        self.result_area = scrolledtext.ScrolledText(results_padding,
                                                     width=75,
                                                     height=32,
                                                     font=("Consolas", 9),
                                                     bg="#f8f8f8",
                                                     fg="#262626",
                                                     relief="flat",
                                                     padx=10,
                                                     pady=10)
        self.result_area.pack(fill="both", expand=True)
        
        self.result_area.insert(tk.END, "Ready to analyze your Instagram followers!\n\n")
        self.result_area.insert(tk.END, "1. Select your following.json file\n")
        self.result_area.insert(tk.END, "2. Select your followers_1.json file\n")
        self.result_area.insert(tk.END, "3. Click 'ANALYZE NOW' to see results\n\n")
        self.result_area.insert(tk.END, f"✨ Database contains {len(self.famous_accounts)} verified accounts")

    def load_following(self):
        path = filedialog.askopenfilename(
            title="Select following.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            filename = path.split("/")[-1]
            if "following" not in filename.lower():
                messagebox.showerror("Wrong File Selected", 
                    f"You selected '{filename}'.\n\nPlease make sure to select the file named 'following.json' (or similar).")
                return

            self.following_path = path
            self.lbl_following.config(text=f"✅ {filename}",
                                     fg="#0095f6",
                                     font=("Segoe UI", 9, "bold"))

    def load_followers(self):
        path = filedialog.askopenfilename(
            title="Select followers_1.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            filename = path.split("/")[-1]
            if "followers" not in filename.lower():
                messagebox.showerror("Wrong File Selected", 
                    f"You selected '{filename}'.\n\nPlease make sure to select the file named 'followers_1.json' (or similar).")
                return

            self.followers_path = path
            self.lbl_followers.config(text=f"✅ {filename}",
                                     fg="#0095f6",
                                     font=("Segoe UI", 9, "bold"))

    def extract_users(self, filepath):
        users = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            items = []
            if isinstance(data, dict):
                if 'relationships_following' in data:
                    items = data['relationships_following']
                elif 'relationships_followers' in data:
                    items = data['relationships_followers']
            elif isinstance(data, list):
                items = data

            for item in items:
                found = False
                if 'title' in item and item['title']:
                    users.add(item['title'])
                    found = True
                
                if not found and 'string_list_data' in item:
                    for entry in item['string_list_data']:
                        if 'value' in entry:
                            users.add(entry['value'])
                            found = True
                        elif 'href' in entry and not found:
                            if 'instagram.com/' in entry['href']:
                                clean_user = entry['href'].rstrip('/').split('/')[-1]
                                users.add(clean_user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{str(e)}")
        return users

    def process_files(self):
        if not self.following_path or not self.followers_path:
            messagebox.showwarning("Missing Files",
                                 "Please select BOTH files before analyzing.")
            return

        following = self.extract_users(self.following_path)
        followers = self.extract_users(self.followers_path)

        if not following and not followers:
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END,
                                   "❌ Error: No usernames found in the files.\n\n")
            self.result_area.insert(tk.END,
                                   "Please check that you've selected the correct files.")
            return

        # Core comparison logic
        not_following_back = following - followers
        fans = followers - following

        # Filter famous accounts if enabled
        ignored_count = 0
        if self.ignore_famous_var.get():
            original_count = len(not_following_back)
            not_following_back = {user for user in not_following_back 
                                 if user not in self.famous_accounts}
            ignored_count = original_count - len(not_following_back)

        # Sort for display
        not_following_back_sorted = sorted(list(not_following_back))
        fans_sorted = sorted(list(fans))

        # Display results
        self.result_area.delete(1.0, tk.END)
        
        # Statistics
        self.result_area.insert(tk.END, f"📊 Total Following: {len(following)}\n")
        self.result_area.insert(tk.END, f"📊 Total Followers: {len(followers)}\n")
        if self.ignore_famous_var.get() and ignored_count > 0:
            self.result_area.insert(tk.END, 
                                   f"🌟 Filtered {ignored_count} verified/famous accounts\n")
        self.result_area.insert(tk.END, "\n" + "─" * 40 + "\n")

        # Section 1: Not following back (ALWAYS SHOW)
        self.result_area.insert(tk.END, 
                               f"❌ NOT FOLLOWING YOU BACK ({len(not_following_back_sorted)} users)\n")
        self.result_area.insert(tk.END, "─" * 40 + "\n\n")
        if not_following_back_sorted:
            for i, user in enumerate(not_following_back_sorted, 1):
                self.result_area.insert(tk.END, f"{i:3d}. @{user}\n")
        else:
            self.result_area.insert(tk.END, "   Everyone you follow is following you back! 🎉\n")
        
        # Section 2: Fans (ONLY SHOW IF CHECKBOX IS CHECKED)
        if self.show_fans_var.get():
            self.result_area.insert(tk.END, "\n\n")
            self.result_area.insert(tk.END, 
                                   f"💚 YOUR FANS ({len(fans_sorted)} users)\n")
            self.result_area.insert(tk.END, 
                                   "   (They follow you, but you don't follow them back)\n")
            self.result_area.insert(tk.END, "─" * 40 + "\n")
            if fans_sorted:
                for i, user in enumerate(fans_sorted, 1):
                    self.result_area.insert(tk.END, f"{i:3d}. @{user}\n")
            else:
                self.result_area.insert(tk.END, "   You follow back everyone who follows you!\n")
        
        self.result_area.insert(tk.END, "\n" + "═" * 40 + "\n")
        self.result_area.insert(tk.END, "Analysis complete! 🎯\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramCheckerApp(root)
    root.mainloop()
