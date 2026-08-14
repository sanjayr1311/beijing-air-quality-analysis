import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib

# ================= COLOR PALETTE =================
COLOR_BG          = "#0F172A"   # deep navy background
COLOR_SIDEBAR     = "#111827"   # near-black sidebar
COLOR_CARD        = "#1E293B"   # card / panel background
COLOR_CARD_ALT    = "#243247"   # slightly lighter card
COLOR_ACCENT      = "#38BDF8"   # sky blue accent
COLOR_ACCENT_DARK = "#0EA5E9"
COLOR_SUCCESS     = "#22C55E"
COLOR_WARNING     = "#F59E0B"
COLOR_DANGER      = "#EF4444"
COLOR_TEXT        = "#F1F5F9"
COLOR_TEXT_DIM    = "#94A3B8"
COLOR_BORDER      = "#334155"

FONT_FAMILY = "Segoe UI"

# ================= Load Resources =================
try:
    df = pd.read_csv("Cleaned_Beijing_Air_Quality.csv")
except Exception:
    df = None

try:
    model = joblib.load("best_pm25_model.pkl")
    scaler = joblib.load("scaler.pkl")
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:")
    print(e)
    model = None
    scaler = None

# ================= Main Window =================
root = tk.Tk()
root.title("Beijing Air Quality Intelligence Dashboard")
root.geometry("1180x720")
root.minsize(1000, 640)
root.configure(bg=COLOR_BG)

style = ttk.Style()
style.theme_use("clam")

# ---- ttk styles ----
style.configure("Treeview",
                 background=COLOR_CARD,
                 fieldbackground=COLOR_CARD,
                 foreground=COLOR_TEXT,
                 rowheight=26,
                 borderwidth=0,
                 font=(FONT_FAMILY, 10))
style.configure("Treeview.Heading",
                 background=COLOR_ACCENT_DARK,
                 foreground="white",
                 font=(FONT_FAMILY, 10, "bold"),
                 relief="flat")
style.map("Treeview.Heading", background=[("active", COLOR_ACCENT)])
style.map("Treeview", background=[("selected", COLOR_ACCENT_DARK)],
                        foreground=[("selected", "white")])

style.configure("Vertical.TScrollbar", background=COLOR_CARD,
                 troughcolor=COLOR_BG, arrowcolor=COLOR_TEXT, borderwidth=0)
style.configure("Horizontal.TScrollbar", background=COLOR_CARD,
                 troughcolor=COLOR_BG, arrowcolor=COLOR_TEXT, borderwidth=0)

# ================= Root Layout =================
sidebar = tk.Frame(root, bg=COLOR_SIDEBAR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main_area = tk.Frame(root, bg=COLOR_BG)
main_area.pack(side="left", fill="both", expand=True)

topbar = tk.Frame(main_area, bg=COLOR_BG, height=70)
topbar.pack(fill="x", side="top")
topbar.pack_propagate(False)

content = tk.Frame(main_area, bg=COLOR_BG)
content.pack(fill="both", expand=True, padx=30, pady=(10, 20))

page_title_var = tk.StringVar(value="Overview")
page_sub_var = tk.StringVar(value="Beijing Air Quality Intelligence")

tk.Label(topbar, textvariable=page_title_var, bg=COLOR_BG, fg=COLOR_TEXT,
          font=(FONT_FAMILY, 20, "bold"), anchor="w").pack(side="left", padx=30, pady=(14, 0), anchor="s")
tk.Label(topbar, textvariable=page_sub_var, bg=COLOR_BG, fg=COLOR_TEXT_DIM,
          font=(FONT_FAMILY, 10), anchor="w").pack(side="left", padx=(0, 0), pady=(0, 14), anchor="s")

separator = tk.Frame(main_area, bg=COLOR_BORDER, height=1)
separator.pack(fill="x")

def clear():
    for w in content.winfo_children():
        w.destroy()

# ---------- helper: card factory ----------
def make_card(parent, **kw):
    card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground=COLOR_BORDER,
                     highlightthickness=1, bd=0, **kw)
    return card

def stat_card(parent, title, value, color=COLOR_ACCENT, icon="●"):
    card = make_card(parent)
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(fill="both", expand=True, padx=18, pady=16)
    tk.Label(inner, text=icon, bg=COLOR_CARD, fg=color,
              font=(FONT_FAMILY, 16)).pack(anchor="w")
    tk.Label(inner, text=str(value), bg=COLOR_CARD, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 22, "bold")).pack(anchor="w", pady=(6, 0))
    tk.Label(inner, text=title, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
              font=(FONT_FAMILY, 10)).pack(anchor="w")
    return card

def section_label(parent, text):
    tk.Label(parent, text=text, bg=COLOR_BG, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 13, "bold")).pack(anchor="w", pady=(20, 10))

# ---------------- Home ----------------
def home():
    page_title_var.set("Overview")
    page_sub_var.set("Live snapshot of the Beijing air-quality dataset")
    clear()

    hero = make_card(content)
    hero.pack(fill="x", pady=(0, 10))
    hero_inner = tk.Frame(hero, bg=COLOR_CARD)
    hero_inner.pack(fill="x", padx=24, pady=20)
    tk.Label(hero_inner, text="Beijing Air Quality Analysis", bg=COLOR_CARD,
              fg=COLOR_TEXT, font=(FONT_FAMILY, 18, "bold")).pack(anchor="w")
    tk.Label(hero_inner,
              text="Explore historical pollutant readings and predict PM2.5 concentration "
                   "using a trained machine-learning model.",
              bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 10),
              wraplength=800, justify="left").pack(anchor="w", pady=(6, 0))

    section_label(content, "Dataset Snapshot")
    stats_row = tk.Frame(content, bg=COLOR_BG)
    stats_row.pack(fill="x")

    if df is not None:
        rows = f"{len(df):,}"
        cols = f"{len(df.columns)}"
        stations = f"{df['station'].nunique()}"
        model_status = "Loaded" if model is not None else "Missing"
        model_color = COLOR_SUCCESS if model is not None else COLOR_DANGER

        cards = [
            ("Total Records", rows, COLOR_ACCENT, "▤"),
            ("Columns Tracked", cols, COLOR_WARNING, "▥"),
            ("Monitoring Stations", stations, "#A78BFA", "◎"),
            ("Model Status", model_status, model_color, "✓" if model is not None else "!"),
        ]
        for i, (title, val, color, icon) in enumerate(cards):
            c = stat_card(stats_row, title, val, color, icon)
            c.grid(row=0, column=i, sticky="nsew", padx=(0, 12) if i < 3 else (0, 0))
            stats_row.grid_columnconfigure(i, weight=1)
    else:
        warn = make_card(stats_row)
        warn.pack(fill="x")
        tk.Label(warn, text="⚠  Dataset file not found. Place "
                              "'Cleaned_Beijing_Air_Quality.csv' in the app folder.",
                  bg=COLOR_CARD, fg=COLOR_WARNING, font=(FONT_FAMILY, 11),
                  padx=18, pady=16).pack(anchor="w")

    if df is not None:
        section_label(content, "Average Pollutant Levels")
        pollutant_row = tk.Frame(content, bg=COLOR_BG)
        pollutant_row.pack(fill="x")
        pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        colors = [COLOR_DANGER, COLOR_WARNING, "#A78BFA", COLOR_ACCENT, "#F472B6", COLOR_SUCCESS]
        for i, p in enumerate(pollutants):
            try:
                avg = round(df[p].mean(), 1)
            except Exception:
                avg = "N/A"
            c = stat_card(pollutant_row, p, avg, colors[i % len(colors)], "◆")
            c.grid(row=i // 6, column=i % 6, sticky="nsew", padx=(0, 12), pady=(0, 12))
            pollutant_row.grid_columnconfigure(i % 6, weight=1)

# ---------------- Dataset ----------------
def dataset():
    page_title_var.set("Dataset")
    page_sub_var.set("First 50 rows of the cleaned dataset")
    clear()

    if df is None:
        empty_state(content, "Dataset not found",
                     "Place 'Cleaned_Beijing_Air_Quality.csv' next to this script and restart.")
        return

    card = make_card(content)
    card.pack(fill="both", expand=True)
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(fill="both", expand=True, padx=14, pady=14)

    tree_wrap = tk.Frame(inner, bg=COLOR_CARD)
    tree_wrap.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(tree_wrap, orient="vertical")
    hsb = ttk.Scrollbar(tree_wrap, orient="horizontal")

    tree = ttk.Treeview(tree_wrap, show="headings", height=20,
                          yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    tree["columns"] = list(df.columns)
    for c in df.columns:
        tree.heading(c, text=c)
        tree.column(c, width=90, anchor="center")

    for idx, (_, r) in enumerate(df.head(50).iterrows()):
        tag = "even" if idx % 2 == 0 else "odd"
        tree.insert("", tk.END, values=list(r), tags=(tag,))

    tree.tag_configure("even", background=COLOR_CARD)
    tree.tag_configure("odd", background=COLOR_CARD_ALT)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tree_wrap.grid_rowconfigure(0, weight=1)
    tree_wrap.grid_columnconfigure(0, weight=1)

    tk.Label(inner, text=f"Showing 50 of {len(df):,} rows", bg=COLOR_CARD,
              fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 9)).pack(anchor="w", pady=(8, 0))

# ---------------- Visualizations ----------------
def visual():
    page_title_var.set("Summary")
    page_sub_var.set("Average pollutant concentration across all records")
    clear()

    if df is None:
        empty_state(content, "No data to summarize",
                     "Load the dataset to see pollutant averages.")
        return

    stats = df[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].mean().round(2)
    colors = {"PM2.5": COLOR_DANGER, "PM10": COLOR_WARNING, "SO2": "#A78BFA",
              "NO2": COLOR_ACCENT, "CO": "#F472B6", "O3": COLOR_SUCCESS}
    max_val = max(stats.values) if len(stats) else 1

    card = make_card(content)
    card.pack(fill="both", expand=True)
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(fill="both", expand=True, padx=26, pady=24)

    tk.Label(inner, text="Average Pollutant Levels (µg/m³ or mg/m³)", bg=COLOR_CARD,
              fg=COLOR_TEXT, font=(FONT_FAMILY, 13, "bold")).pack(anchor="w", pady=(0, 18))

    for name, val in stats.items():
        row = tk.Frame(inner, bg=COLOR_CARD)
        row.pack(fill="x", pady=8)

        tk.Label(row, text=name, bg=COLOR_CARD, fg=COLOR_TEXT, width=8,
                  anchor="w", font=(FONT_FAMILY, 10, "bold")).pack(side="left")

        bar_bg = tk.Frame(row, bg=COLOR_CARD_ALT, height=16)
        bar_bg.pack(side="left", fill="x", expand=True, padx=10)
        bar_bg.pack_propagate(False)

        frac = max(val / max_val, 0.02) if max_val else 0.02
        bar_container = tk.Frame(bar_bg, bg=COLOR_CARD_ALT)
        bar_container.place(relx=0, rely=0, relheight=1, relwidth=1)
        bar_fill = tk.Frame(bar_container, bg=colors.get(name, COLOR_ACCENT))
        bar_fill.place(relx=0, rely=0, relheight=1, relwidth=frac)

        tk.Label(row, text=str(val), bg=COLOR_CARD, fg=COLOR_TEXT_DIM, width=8,
                  anchor="e", font=(FONT_FAMILY, 10)).pack(side="left")

# ---------------- Prediction ----------------
def prediction():
    page_title_var.set("Predict")
    page_sub_var.set("Estimate PM2.5 concentration from live inputs")
    clear()

    wrapper = tk.Frame(content, bg=COLOR_BG)
    wrapper.pack(fill="both", expand=True)
    wrapper.grid_columnconfigure(0, weight=3)
    wrapper.grid_columnconfigure(1, weight=2)
    wrapper.grid_rowconfigure(0, weight=1)

    form_card = make_card(wrapper)
    form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
    form_inner = tk.Frame(form_card, bg=COLOR_CARD)
    form_inner.pack(fill="both", expand=True, padx=24, pady=22)

    tk.Label(form_inner, text="Input Parameters", bg=COLOR_CARD, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 13, "bold")).grid(row=0, column=0, columnspan=2,
                                                      sticky="w", pady=(0, 14))

    labels = ["PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES",
              "DEWP", "RAIN", "WSPM", "Station Encoded",
              "Season Encoded", "Weekday", "Hour"]

    entries = []
    for i, l in enumerate(labels):
        r = i + 1
        tk.Label(form_inner, text=l, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                  font=(FONT_FAMILY, 10), width=16, anchor="w").grid(
                      row=r, column=0, sticky="w", pady=5)
        e = tk.Entry(form_inner, width=18, bg=COLOR_CARD_ALT, fg=COLOR_TEXT,
                      insertbackground=COLOR_TEXT, relief="flat",
                      highlightthickness=1, highlightbackground=COLOR_BORDER,
                      highlightcolor=COLOR_ACCENT, font=(FONT_FAMILY, 10))
        e.grid(row=r, column=1, sticky="w", pady=5, padx=(10, 0), ipady=4)
        entries.append(e)

    predict_btn = tk.Button(form_inner, text="Predict PM2.5", command=lambda: predict_pm25(),
                              bg=COLOR_ACCENT, fg="#0F172A", activebackground=COLOR_ACCENT_DARK,
                              activeforeground="white", font=(FONT_FAMILY, 11, "bold"),
                              relief="flat", bd=0, cursor="hand2", padx=16, pady=10)
    predict_btn.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="ew", pady=(16, 0))

    # ----- result panel -----
    result_card = make_card(wrapper)
    result_card.grid(row=0, column=1, sticky="nsew")
    result_inner = tk.Frame(result_card, bg=COLOR_CARD)
    result_inner.pack(fill="both", expand=True, padx=24, pady=22)

    tk.Label(result_inner, text="Prediction Result", bg=COLOR_CARD, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 13, "bold")).pack(anchor="w", pady=(0, 16))

    result_value = tk.Label(result_inner, text="—", bg=COLOR_CARD, fg=COLOR_ACCENT,
                              font=(FONT_FAMILY, 32, "bold"))
    result_value.pack(anchor="w")

    result_unit = tk.Label(result_inner, text="µg/m³ · PM2.5", bg=COLOR_CARD,
                             fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 10))
    result_unit.pack(anchor="w", pady=(0, 16))

    badge = tk.Label(result_inner, text="Awaiting input", bg=COLOR_CARD_ALT,
                       fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 10, "bold"),
                       padx=12, pady=6)
    badge.pack(anchor="w")

    tk.Label(result_inner,
              text="Fill in the pollutant and weather readings, then click "
                   "Predict PM2.5 to see the estimated concentration and its "
                   "AQI category.",
              bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 9),
              wraplength=260, justify="left").pack(anchor="w", pady=(20, 0))

    aqi_scale = [
        ("Good", "0–12", COLOR_SUCCESS),
        ("Moderate", "12–35.4", COLOR_WARNING),
        ("USG", "35.4–55.4", "#F97316"),
        ("Unhealthy", "55.4–150.4", COLOR_DANGER),
        ("Very Unhealthy", "150.4–250.4", "#B91C1C"),
        ("Hazardous", "250.4+", "#7F1D1D"),
    ]
    scale_frame = tk.Frame(result_inner, bg=COLOR_CARD)
    scale_frame.pack(anchor="w", pady=(18, 0), fill="x")
    for name, rng, color in aqi_scale:
        row = tk.Frame(scale_frame, bg=COLOR_CARD)
        row.pack(fill="x", pady=2)
        tk.Label(row, text="●", bg=COLOR_CARD, fg=color, font=(FONT_FAMILY, 9)).pack(side="left")
        tk.Label(row, text=f" {name}", bg=COLOR_CARD, fg=COLOR_TEXT, width=14,
                  anchor="w", font=(FONT_FAMILY, 9)).pack(side="left")
        tk.Label(row, text=rng, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                  font=(FONT_FAMILY, 9)).pack(side="left")

    def predict_pm25():
        if model is None:
            messagebox.showerror("Error", "Model file not found.")
            return
        try:
            values = [float(e.get()) for e in entries]
            scaled = scaler.transform([values])

            try:
                pred = model.predict([values])[0]
            except Exception:
                pred = model.predict(scaled)[0]

            if pred <= 12:
                aqi, color = "Good", COLOR_SUCCESS
            elif pred <= 35.4:
                aqi, color = "Moderate", COLOR_WARNING
            elif pred <= 55.4:
                aqi, color = "USG", "#F97316"
            elif pred <= 150.4:
                aqi, color = "Unhealthy", COLOR_DANGER
            elif pred <= 250.4:
                aqi, color = "Very Unhealthy", "#B91C1C"
            else:
                aqi, color = "Hazardous", "#7F1D1D"

            result_value.config(text=f"{pred:.1f}")
            badge.config(text=aqi, fg=color)

        except Exception as ex:
            messagebox.showerror("Input Error", str(ex))

# ---------------- About ----------------
def about():
    page_title_var.set("About")
    page_sub_var.set("Project details")
    clear()

    card = make_card(content)
    card.pack(fill="both", expand=True)
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(fill="both", expand=True, padx=30, pady=26)

    tk.Label(inner, text="Beijing Air Quality Analysis", bg=COLOR_CARD, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 16, "bold")).pack(anchor="w")
    tk.Label(inner, text="Dataset: Beijing Air Quality  ·  Model: Random Forest Regressor",
              bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(4, 20))

    features = [
        ("▤", "Dataset Preview", "Browse the first 50 rows of cleaned data."),
        ("▥", "Dataset Summary", "Average pollutant concentrations at a glance."),
        ("◎", "PM2.5 Prediction", "Estimate PM2.5 from live parameter inputs."),
        ("ⓘ", "About Page", "Project and model information."),
    ]
    for icon, title, desc in features:
        row = tk.Frame(inner, bg=COLOR_CARD)
        row.pack(fill="x", pady=8, anchor="w")
        tk.Label(row, text=icon, bg=COLOR_CARD, fg=COLOR_ACCENT,
                  font=(FONT_FAMILY, 13)).pack(side="left", padx=(0, 12))
        text_col = tk.Frame(row, bg=COLOR_CARD)
        text_col.pack(side="left")
        tk.Label(text_col, text=title, bg=COLOR_CARD, fg=COLOR_TEXT,
                  font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(anchor="w")
        tk.Label(text_col, text=desc, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                  font=(FONT_FAMILY, 9), anchor="w").pack(anchor="w")

# ---------------- Empty state helper ----------------
def empty_state(parent, title, subtitle):
    card = make_card(parent)
    card.pack(fill="both", expand=True)
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(expand=True)
    tk.Label(inner, text="⚠", bg=COLOR_CARD, fg=COLOR_WARNING,
              font=(FONT_FAMILY, 28)).pack(pady=(60, 10))
    tk.Label(inner, text=title, bg=COLOR_CARD, fg=COLOR_TEXT,
              font=(FONT_FAMILY, 13, "bold")).pack()
    tk.Label(inner, text=subtitle, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
              font=(FONT_FAMILY, 10)).pack(pady=(4, 60))

# ================= Sidebar =================
tk.Label(sidebar, text="🌫", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT,
          font=(FONT_FAMILY, 26)).pack(pady=(28, 0))
tk.Label(sidebar, text="Beijing AQ", bg=COLOR_SIDEBAR, fg=COLOR_TEXT,
          font=(FONT_FAMILY, 14, "bold")).pack(pady=(6, 0))
tk.Label(sidebar, text="Intelligence Dashboard", bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM,
          font=(FONT_FAMILY, 8)).pack(pady=(0, 26))

nav_buttons = {}
nav_items = [
    ("Home", "⌂", home),
    ("Dataset", "▤", dataset),
    ("Summary", "▥", visual),
    ("Prediction", "◎", prediction),
    ("About", "ⓘ", about),
]

def set_active(name):
    for n, btn in nav_buttons.items():
        if n == name:
            btn.configure(bg=COLOR_ACCENT_DARK, fg="white")
        else:
            btn.configure(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM)

def make_nav_click(name, fn):
    def _click():
        set_active(name)
        fn()
    return _click

for name, icon, fn in nav_items:
    btn = tk.Button(sidebar, text=f"  {icon}   {name}", anchor="w",
                      bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM, activebackground=COLOR_ACCENT_DARK,
                      activeforeground="white", relief="flat", bd=0, cursor="hand2",
                      font=(FONT_FAMILY, 11), padx=16, pady=10)
    btn.configure(command=make_nav_click(name, fn))
    btn.pack(fill="x", padx=12, pady=3)
    nav_buttons[name] = btn

footer = tk.Label(sidebar, text="v2.0 · ML Powered", bg=COLOR_SIDEBAR,
                    fg=COLOR_TEXT_DIM, font=(FONT_FAMILY, 8))
footer.pack(side="bottom", pady=16)

set_active("Home")
home()
root.mainloop()