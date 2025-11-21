import tkinter as tk
from tkinter import messagebox
import math

R = 6378137


class Triangle:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.lat_rad = math.radians(lat)
        self.lon_rad = math.radians(lon)
        self.x = None
        self.y = None
        self.z = None

    # Mokhtasate 3D
    def coordinates(self):
        self.x = math.cos(self.lat_rad) * math.cos(self.lon_rad)
        self.y = math.cos(self.lat_rad) * math.sin(self.lon_rad)
        self.z = math.sin(self.lat_rad)
        return (self.x, self.y, self.z)

    # zarbe noghtei
    def dot_product(p1, p2):
        dp = p1.x * p2.x + p1.y * p2.y + p1.z * p2.z
        # dp = max(min(dp, 1.0), -1.0)
        return math.acos(dp)

    # zaviyehaye dakheli
    def interior_angle(a, b, c):
        value = (math.cos(a)-(math.cos(b)*math.cos(c))) / \
            (math.sin(b)*math.sin(c))
        return math.acos(value)
    # formoole l'huilier

    def l_huilier_area(a, b, c):
        s = 0.5 * (a + b + c)
        t1 = math.tan(s / 2.0)
        t2 = math.tan((s - a) / 2.0)
        t3 = math.tan((s - b) / 2.0)
        t4 = math.tan((s - c) / 2.0)

        if t1 <= 0 or t2 <= 0 or t3 <= 0 or t4 <= 0:
            A_ang = Triangle.interior_angle(a, b, c)
            B_ang = Triangle.interior_angle(b, a, c)
            C_ang = Triangle.interior_angle(c, a, b)
            E = (A_ang + B_ang + C_ang) - math.pi
        else:
            tan_e4 = math.sqrt(t1 * t2 * t3 * t4)
            E = 4.0 * math.atan(tan_e4)

        area = (R ** 2) * E
        return area

# khoroojiha


def Output(lat1, lon1, lat2, lon2, lat3, lon3):
    p1 = Triangle(lat1, lon1)
    p2 = Triangle(lat2, lon2)
    p3 = Triangle(lat3, lon3)

    p1.coordinates()
    p2.coordinates()
    p3.coordinates()

    a = Triangle.dot_product(p2, p3)
    b = Triangle.dot_product(p1, p3)
    c = Triangle.dot_product(p1, p2)

    side_a_m = a * R
    side_b_m = b * R
    side_c_m = c * R

    perimeter = side_a_m + side_b_m + side_c_m

    A_angle = Triangle.interior_angle(a, b, c)
    B_angle = Triangle.interior_angle(b, a, c)
    C_angle = Triangle.interior_angle(c, a, b)

    area = Triangle.l_huilier_area(a, b, c)

    return {
        "sides_m": (side_a_m, side_b_m, side_c_m),
        "perimeter_m": perimeter,
        "angles_deg": tuple(map(math.degrees, (A_angle, B_angle, C_angle))),
        "area_m2": area
    }

# tkinter


def build_gui():
    root = tk.Tk()
    root.title("Triangle on WGS84 - Perimeter & Area")
    root.geometry("760x520")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    labels = ["Lat1", "Lon1", "Lat2", "Lon2", "Lat3", "Lon3"]
    entries = {}

    for i, lbl in enumerate(labels):
        tk.Label(frame, text=lbl + ":").grid(row=i,
                                             column=0, sticky="e", padx=6, pady=6)
        ent = tk.Entry(frame, width=18)
        ent.grid(row=i, column=1, sticky="w", padx=6, pady=6)
        entries[lbl] = ent

    result_text = tk.Text(frame, width=70, height=20, wrap="word")
    result_text.grid(row=0, column=2, rowspan=9, padx=10, pady=6)

    def Calculate():
        try:
            lat1 = float(entries["Lat1"].get())
            lon1 = float(entries["Lon1"].get())
            lat2 = float(entries["Lat2"].get())
            lon2 = float(entries["Lon2"].get())
            lat3 = float(entries["Lat3"].get())
            lon3 = float(entries["Lon3"].get())
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Please enter numeric values")
            return

        res = Output(lat1, lon1, lat2, lon2, lat3, lon3)

        s = []
        s.append("=== Results ===\n\n")
        s.append("Sides (meters):\n")
        s.append(f" a = {res['sides_m'][0]:,.3f} m\n")
        s.append(f" b = {res['sides_m'][1]:,.3f} m\n")
        s.append(f" c = {res['sides_m'][2]:,.3f} m\n\n")
        s.append(
            f"Perimeter = {res['perimeter_m']:,.3f} m  (~{res['perimeter_m']/1e3:,.3f} km)\n\n")
        s.append("Angles (degrees):\n")
        s.append(f" A = {res['angles_deg'][0]:.8f}°\n")
        s.append(f" B = {res['angles_deg'][1]:.8f}°\n")
        s.append(f" C = {res['angles_deg'][2]:.8f}°\n\n")
        s.append(
            f"Area = {res['area_m2']:,.3f} m²  (~{res['area_m2']/1e6:,.3f} km²)\n")

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "".join(s))

    btn = tk.Button(frame, text="Calculate", command=Calculate)
    btn.grid(row=9, column=1, pady=12)

    # default values
    entries["Lat1"].insert(0, "35.717875")
    entries["Lon1"].insert(0, "51.4180047")
    entries["Lat2"].insert(0, "35.739008")
    entries["Lon2"].insert(0, "51.447467")
    entries["Lat3"].insert(0, "35.700306")
    entries["Lon3"].insert(0, "51.499086")

    root.mainloop()


if __name__ == "__main__":
    build_gui()
