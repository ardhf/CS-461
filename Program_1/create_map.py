import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use('TkAgg')

# City connections
connections = [
    ("Anthony", "Bluff_City"),
    ("Bluff_City", "Kiowa"),
    ("Kiowa", "Attica"),
    ("Attica", "Harper"),
    ("Attica", "Medicine_Lodge"),
    ("Augusta", "Winfield"),
    ("Winfield", "Andover"),
    ("Andover", "Leon"),
    ("Leon", "Wichita"),
    ("Caldwell", "South_Haven"),
    ("South_Haven", "Bluff_City"),
    ("Bluff_City", "Mayfield"),
    ("El_Dorado", "Towanda"),
    ("Towanda", "Andover"),
    ("Andover", "Augusta"),
    ("Augusta", "Emporia"),
    ("Florence", "McPherson"),
    ("McPherson", "Hillsboro"),
    ("Hillsboro", "El_Dorado"),
    ("Greensburg", "Coldwater"),
    ("Coldwater", "Pratt"),
    ("Harper", "Anthony"),
    ("Anthony", "Argonia"),
    ("Argonia", "Rago"),
    ("Hutchinson", "Newton"),
    ("Newton", "Haven"),
    ("Junction_City", "Abilene"),
    ("Abilene", "Marion"),
    ("Marion", "Manhattan"),
    ("Manhattan", "Topeka"),
    ("Kingman", "Cheney"),
    ("Cheney", "Pratt"),
    ("Pratt", "Hutchinson"),
    ("Marion", "McPherson"),
    ("McPherson", "Newton"),
    ("Newton", "Emporia"),
    ("Mayfield", "Wellington"),
    ("Wellington", "Caldwell"),
    ("Caldwell", "Argonia"),
    ("McPherson", "Salina"),
    ("Salina", "Lyons"),
    ("Lyons", "Hillsboro"),
    ("Medicine_Lodge", "Attica"),
    ("Attica", "Kiowa"),
    ("Kiowa", "Coldwater"),
    ("Newton", "McPherson"),
    ("McPherson", "Hutchinson"),
    ("Hutchinson", "Florence"),
    ("Rago", "Viola"),
    ("Viola", "Sawyer"),
    ("Salina", "Abilene"),
    ("Abilene", "Hays"),
    ("Sawyer", "Pratt"),
    ("Pratt", "Zenda"),
    ("Wellington", "Oxford"),
    ("Oxford", "Mayfield"),
    ("Mayfield", "Mulvane"),
    ("Mulvane", "South_Haven"),
    ("Wichita", "Derby"),
    ("Derby", "Clearwater"),
    ("Clearwater", "Cheney"),
    ("Cheney", "Mulvane"),
    ("Mulvane", "Andover"),
    ("Andover", "Newton"),
    ("Newton", "El_Dorado")
]

class CityConnectionsGUI:
    def __init__(self, master, cities):
        self.master = master
        self.cities = cities
        master.title("City Connections Map")

        # Create a frame to hold the canvas and toolbar
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create Figure and FigureCanvasTkAgg
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)

        # Create toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()

        # Pack toolbar and canvas
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.plot_map()

    def plot_map(self):
        self.ax.clear()

        # Plot cities
        for city, (lat, lon) in self.cities.items():
            self.ax.plot(lon, lat, 'ro', markersize=5)
            self.ax.annotate(city, (lon, lat), xytext=(5, 5), textcoords='offset points', fontsize=8)

        # Plot connections (only for cities that are in the given subset)
        for city1, city2 in connections:
            if city1 in self.cities and city2 in self.cities:
                lon1, lat1 = self.cities[city1][1], self.cities[city1][0]
                lon2, lat2 = self.cities[city2][1], self.cities[city2][0]
                self.ax.plot([lon1, lon2], [lat1, lat2], 'b-', linewidth=0.5, alpha=0.5)

        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        self.ax.set_title('City Connections Map')
        self.ax.grid(True)
        self.canvas.draw()

def main(cities):
    global sample_cities
    sample_cities = cities
    root = tk.Tk()
    gui = CityConnectionsGUI(root, cities)
    
    # Handle window close event
    def on_closing():
        plt.close('all')  # Close all matplotlib figures
        root.quit()       # Stop the mainloop
        root.destroy()    # Destroy the root window

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
