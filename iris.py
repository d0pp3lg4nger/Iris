#################################################################################

# @Title: Iris Project
# @Author: Arthur Clemente Machado
# @version: 0.1
# @Date: 19/12/2024
# @Description: This script calculates the distance and velocity of a planet in relation to Earth, 
# based on the time entered by the user. The user can select a planet and enter the initial and final times 
# to calculate the distance and velocity. The results are displayed in the graphical interface.

#################################################################################
# Import the necessary libraries
import pygame
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
import sys
import os
from PIL import Image, ImageTk
from astropy import units as u
from astropy.coordinates import get_body
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
#################################################################################

# Function to initialize the background music
def play_background_music():
    pygame.mixer.init()  # Initialize pygame's audio mixer
    pygame.mixer.music.load(resource_path('background_music/space_song.mp3'))  # Replace with the path to your music file
    pygame.mixer.music.play(-1, 0.0)  # Play the music in an infinite loop (-1 means infinite loop)

# Function to stop the music (if necessary)
def stop_background_music():
    pygame.mixer.music.stop()

# Function to calculate distance and velocity
class Orbital:
    def __init__(self, planet, time1, time2):
        self.planet_name = planet.lower()
        self.time1 = time1
        self.time2 = time2
        with solar_system_ephemeris.set('builtin'):
            self.earth1 = get_body('earth', self.time1)
            self.planet1 = get_body(self.planet_name, self.time1)
            self.earth2 = get_body('earth', self.time2)
            self.planet2 = get_body(self.planet_name, self.time2)
        self.distance1 = self.earth1.separation_3d(self.planet1)
        self.distance2 = self.earth2.separation_3d(self.planet2)
        self.time_difference = (self.time2 - self.time1).to('s').value  # Interval in seconds
        self.velocity = (self.distance2 - self.distance1).to('km') / self.time_difference  # Velocity in km/s

    def get_distance(self):
        return self.distance2.to('km')

    def get_velocity(self):
        return self.velocity

def resource_path(relative_path):
    """Get the correct path for resources in the executable"""
    try:
        # For PyInstaller runtime environment
        base_path = sys._MEIPASS
    except Exception:
        # For development environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to format the distance
def format_distance(distance_km):
    formatted_distance = f"{distance_km:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted_distance

# Function to calculate and display results in the GUI
def calculate(time1_entry, time2_entry, result_label):
    planet = planet_name
    time1_str = time1_entry.get().strip()
    time2_str = time2_entry.get().strip()
    
    try:
        time1 = Time(time1_str)
        time2 = Time(time2_str)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter the times in the correct format (YYYY-MM-DD HH:MM:SS).")
        return

    try:
        orb = Orbital(planet, time1, time2)
        distance_km = orb.get_distance().value
        velocity_km_s = orb.get_velocity().value

        formatted_distance = format_distance(distance_km)
        formatted_velocity = format_distance(velocity_km_s)

        if planet == "Earth":
            result_label.config(text="You are already on Earth!")
        else:
            result_label.config(text=f"Distance: {formatted_distance} km\nVelocity: {formatted_velocity} km/s")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to open the time entry screen
def open_time_entry(planet):
    global planet_name
    planet_name = planet
    time_entry_window = Toplevel(root)
    time_entry_window.title(f"Set Time for {planet.capitalize()}")
    time_entry_window.geometry("1980x1080")
    
    # Load the background image
    bg_image = Image.open(resource_path("images/background.png"))  # Replace with the path to your background image
    bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Adjust the image size to the window size
    bg_image = ImageTk.PhotoImage(bg_image)
    
    # Label for background image
    bg_label = tk.Label(time_entry_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the background image

    # Load the planet image
    planet_image = Image.open(resource_path(f"images/{planet_name}.png"))  # Replace with the path to the planet's image
    planet_image = planet_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the planet image
    planet_image_tk = ImageTk.PhotoImage(planet_image)  # Convert the image to a format understood by Tkinter

    # Display the planet image
    planet_image_label = tk.Label(time_entry_window, image=planet_image_tk, bg="black")
    planet_image_label.image = planet_image_tk  # Keep a reference to the image
    planet_image_label.place(relx=0.5, rely=0.25, anchor="center")  # Position the image in the window

    # Add the planet name to the window
    planet_name_label = tk.Label(time_entry_window, text=f"{planet.capitalize()}", font=("Helvetica", 36, "bold"), fg="white", bg="black")
    planet_name_label.grid(row=0, column=0, pady=10, padx=10)
    planet_name_label.place(relx=0.5, rely=0.08, anchor="center")

    # Label for time
    time1_label = tk.Label(time_entry_window, text="Enter the initial time (YYYY-MM-DD HH:MM:SS):", font=("Helvetica", 20, "bold"), bg="black", fg="white")
    time1_label.grid(row=0, column=0, pady=5)
    time1_label.place(relx=0.5, rely=0.4, anchor="center")
    
    # Time entry
    time1_entry = tk.Entry(time_entry_window, font=("Helvetica", 18, "bold"), relief="solid", borderwidth=2)
    time1_entry.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
    time1_entry.place(relx=0.5, rely=0.47, anchor="center")
    
    time2_label = tk.Label(time_entry_window, text="Enter the final time (YYYY-MM-DD HH:MM:SS):", font=("Helvetica", 20, "bold"), bg="black", fg="white")
    time2_label.grid(row=2, column=0, pady=5)
    time2_label.place(relx=0.5, rely=0.59, anchor="center")
    
    time2_entry = tk.Entry(time_entry_window, font=("Helvetica", 18, "bold"), relief="solid", borderwidth=2)
    time2_entry.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
    time2_entry.place(relx=0.5, rely=0.66, anchor="center")

    # Button to calculate
    calculate_button = tk.Button(time_entry_window, text="Calculate", command=lambda: calculate(time1_entry, time2_entry, result_label), font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised", bd=2)
    calculate_button.grid(row=4, column=0, pady=15)
    calculate_button.place(relx=0.5, rely=0.77, anchor="center")

    # Label to display the result
    result_label = tk.Label(time_entry_window, text="Distance and velocity will be displayed here.", font=("Helvetica", 20, "bold"), fg="white", bg="black")
    result_label.grid(row=5, column=0, pady=10)
    result_label.place(relx=0.5, rely=0.87, anchor="center")

    # Keep a reference to the image to prevent it from being discarded
    bg_label.image = bg_image


# Create the main graphical interface
root = tk.Tk()
root.title("Iris Project")
root.geometry("1920x1080")  # Window size

# Load the background image
background_image = Image.open(resource_path("images/background.png"))  # Replace with the path to your background image
background_image = background_image.resize((1920, 1080))  # Adjust the image size
background_tk = ImageTk.PhotoImage(background_image)

# Create the Canvas and add the background image
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack(fill="both", expand=True)

# Place the image on the canvas
canvas.create_image(0, 0, image=background_tk, anchor="nw")

# Set the centered title
title_label = tk.Label(root, text="IRIS PROJECT", font=("Helvetica", 38, "bold"), fg="white", bg="black")
title_label.place(relx=0.5, rely=0.1, anchor="center")

# Load planet images
planet_images = ["images/mercury.png", "images/venus.png", "images/earth.png", "images/mars.png", "images/jupiter.png", "images/saturn.png", "images/uranus.png", "images/neptune.png"]
planet_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

def add_black_background(image_path):
    # Load the image with transparency
    img = Image.open(resource_path(image_path)).convert("RGBA")
    
    # Create a new black image with the same size as the original image
    black_bg = Image.new("RGBA", img.size, (0, 0, 0, 255))  # black background (0, 0, 0) and opacity 255
    
    # Paste the original image over the black background
    black_bg.paste(img, (0, 0), img)  # Using the third parameter to maintain transparency

    return black_bg

# Add planet images for click with name below
# Adjust the creation of buttons and labels to increase the vertical distance
for i, image in enumerate(planet_images):
    img = add_black_background(image)  # Remove white border and add black background
    img = img.resize((200, 200))  # Resize
    img_tk = ImageTk.PhotoImage(img)
    
    # Create a button with the image
    planet_button = tk.Button(root, image=img_tk, command=lambda p=planet_names[i]: open_time_entry(p))
    planet_button.image = img_tk  # Keep a reference to the image
    planet_button.place(relx=(i % 4) * 0.25 + 0.125, rely=(i // 4) * 0.3 + 0.4, anchor="center")  # Increasing the vertical space between planets
    
    # Create a Label with the planet name below the image
    planet_label = tk.Label(root, text=planet_names[i], font=("Helvetica", 20, "bold"), fg="white", bg="black")
    # Adjust vertical distance for planets in the second row (planets in the second line)
    if i < 4:
        planet_button.place(relx=(i % 4) * 0.25 + 0.125, rely=0.36, anchor="center")
        planet_label.place(relx=(i % 4) * 0.25 + 0.125, rely=(i // 4) * 0.3 + 0.53, anchor="center")  # Larger distance for the second row
    else:
        planet_button.place(relx=(i % 4) * 0.25 + 0.125, rely=0.76, anchor="center")
        planet_label.place(relx=(i % 4) * 0.25 + 0.125, rely=(i // 4) * 0.3 + 0.62, anchor="center")  # Adjustment for the planets in the first row

# Start the background music when opening the program
play_background_music()

# Start the graphical interface
root.mainloop()
