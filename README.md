Simple Follower Analyzer

A clean, modern Python-Tkinter desktop application designed to help you audit your Instagram social circle. By analyzing your official Instagram data exports, this tool identifies users who don't follow you back and fans who follow you whom you haven't followed back.
✨ Features

    Privacy First: No login required. The app processes your data locally on your machine — your password never leaves your sight.

    Celebrity Filtering: Built-in database of over 500+ verified accounts (athletes, artists, brands, and meme pages) so your "Not Following Back" list isn't cluttered with famous people.

    Fan Detection: Toggleable option to see your "Fans" (people who follow you, but you don't follow them).

    Modern UI: Features a custom Instagram-inspired gradient interface, toggle switches, and an interactive results area.

    Safety Checks: Includes file validation to ensure you are uploading the correct JSON files.

🚀 How to Use
1. Get Your Data from Instagram

Since this app works offline, you need to request your data from Instagram:

    Go to Your Activity > Download your information.

    Select Download or transfer information.

    Choose Some of your information.

    Select Followers and Following.

    Make sure to select ALL TIME for the time range. Otherwise not all followers will be included

    Crucial: Change the Format to JSON (HTML will not work).

    Once the file arrives in your email, download and unzip it.

2. Run the Program

    Ensure you have Python installed.

    Run the script: double click on the py file to run it

    Click Select following.json and navigate to the file.

    Click Select followers_1.json and navigate to the file.

    Click ANALYZE NOW.

🛠️ Technical Details

    Language: Python 3

    Library: tkinter (Standard Library)

    Data Format: Parses Instagram's string_list_data and href structures found in official account exports.

    Custom Widgets: * GradientButton: A canvas-based widget for the signature Instagram aesthetic.

        ToggleSwitch: An iOS-style toggle for a cleaner user experience.

📋 Requirements

    Python 3.x

    No external pip dependencies are required (uses built-in json, tkinter, and filedialog).


KNOWN LIMITATIONS:
You might see people show up as Non-Following you back, but their accounts are unavaliable on Instagram. 
This is a limitation of the nature of the app and the data provided via instagram.
Deleted accounts and/or accounts blocking you arent always removed from the Following and Followers lists.

⚖️ Disclaimer

This tool is not affiliated with, authorized, maintained, sponsored, or endorsed by Instagram or any of its affiliates or subsidiaries. This is an independent and unofficial tool for personal data analysis.
