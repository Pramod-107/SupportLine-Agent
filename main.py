import solara
import backend as state
import user
import manager
import about

# --- THEME VARIABLES ---
PRIMARY = state.TEXT_PRIMARY
SECONDARY = state.TEXT_SECONDARY
ACCENT = state.ACCENT_COLOR
EMERGENCY_RED = "#dc2626"


@solara.component
def Navbar():
    with solara.Row(
            style={"width": "100%", "justify-content": "center", "padding-top": "30px", "padding-bottom": "10px",
                   "z-index": "100"}):
        with solara.Row(gap="40px", style={"align-items": "center"}):
            solara.Button("HOME", text=True, on_click=lambda: state.current_page.set("home"),
                          style={"color": PRIMARY, "font-weight": "bold", "background": "transparent",
                                 "font-size": "14px", "letter-spacing": "1px"})
            solara.Button("ABOUT", text=True, on_click=lambda: state.current_page.set("about"),
                          style={"color": PRIMARY, "font-weight": "bold", "background": "transparent",
                                 "font-size": "14px", "letter-spacing": "1px"})

            if not state.show_emergency_menu.value:
                solara.Button("EMERGENCY", on_click=lambda: state.show_emergency_menu.set(True),
                              style={"background-color": EMERGENCY_RED, "color": "white", "border-radius": "30px",
                                     "padding": "10px 30px", "font-weight": "bold", "border": "none",
                                     "box-shadow": "0 4px 15px rgba(220, 38, 38, 0.4)", "font-size": "14px",
                                     "letter-spacing": "1px"})
            else:
                with solara.Row(gap="15px",
                                style={"background": "white", "padding": "5px 10px", "border-radius": "50px",
                                       "box-shadow": "0 10px 25px rgba(0,0,0,0.1)", "border": "1px solid #fca5a5",
                                       "align-items": "center"}):
                    # UPDATED: Fixed CSS syntax (removed extra quotes) and ensured border-radius is applied
                    solara.HTML(
                        unsafe_innerHTML=f'<a href="tel:100" target="_blank" style="text-decoration: none;"><div style="background-color: #fee2e2; color: #991b1b; padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 8px;"><span>👮</span> Police</div></a>')
                    solara.HTML(
                        unsafe_innerHTML=f'<a href="tel:108" target="_blank" style="text-decoration: none;"><div style="background-color: #fff7ed; color: #c2410c; padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 8px;"><span>🚑</span> Ambulance</div></a>')
                    
                    solara.Button("x", on_click=lambda: state.show_emergency_menu.set(False), text=True,
                                  style={"color": SECONDARY, "font-weight": "bold", "padding": "0 10px"})


@solara.component
def HomeView():
    with solara.Column(style={"width": "100%", "height": "85vh", "justify-content": "center", "align-items": "center"}):
        with solara.Column(style={"max-width": "900px", "text-align": "center", "align-items": "center"}):
            # TITLE
            solara.HTML(
                unsafe_innerHTML=f'<h1 style="font-family: \'Inter\', sans-serif; font-size: 100px; font-weight: 800; color: {PRIMARY}; margin: 0; letter-spacing: -2px; line-height: 1.1;">SupportLine Agent</h1>')

            # DESCRIPTION
            solara.Text("Connecting you to the nearest help instantly using intelligent agent-based modeling.",
                        style={"font-family": "'Inter', sans-serif", "font-size": "25px", "font-weight": "500",
                               "color": SECONDARY, "margin-top": "15px", "max-width": "600px", "line-height": "1.6",
                               "text-align": "center"})

            # WHO ARE YOU
            with solara.Column(style={"margin-top": "150px", "width": "100%", "align-items": "center", "gap": "25px"}):
                solara.Text("Who are you?",
                            style={"font-family": "'Inter', sans-serif", "font-size": "50px", "font-weight": "700",
                                   "margin-top": "50px", "color": PRIMARY, "opacity": "0.8"})
                with solara.Row(gap="30px"):
                    with solara.Button(on_click=lambda: [state.current_page.set("user"), state.user_view_step.set(1)],
                                       style={"background-color": "white", "color": PRIMARY, "height": "60px",
                                              "font-size": "20px", "width": "200px", "border-radius": "30px",
                                              "font-weight": "bold", "box-shadow": "0 10px 30px rgba(0,0,0,0.05)"},
                                       classes=["role-button"]):
                        solara.Text("USER")
                    with solara.Button(on_click=lambda: state.current_page.set("manager"),
                                       style={"background-color": ACCENT, "color": "white", "height": "60px",
                                              "font-size": "15px", "width": "200px", "border-radius": "30px",
                                              "font-weight": "bold", "border": "none",
                                              "box-shadow": f"0 10px 30px {ACCENT}60"}, classes=["role-button"]):
                        solara.Text("CENTER MANAGER")

        with solara.Column(style={"position": "absolute", "bottom": "20px", "width": "100%", "align-items": "center"}):
            solara.HTML(
                unsafe_innerHTML=f'<p style="color: {SECONDARY}; opacity: 0.6; font-size: 15px;">&copy; SupportLine Agent.</p>')


@solara.component
def Page():
    # --- 100% HEIGHT FIX (Applying Direct URL to Body) ---
    bg_url = state.HOME_BG_URL if state.current_page.value == 'home' else state.OTHER_BG_URL

    solara.Style(f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        /* 1. FORCE BACKGROUND ON BODY (Root Level) */
        body {{
            background-image: url("{bg_url}") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
            margin: 0;
            padding: 0;
            width: 100vw;
            min-height: 100vh;
        }}

        /* 2. MAKE CONTAINERS TRANSPARENT */
        #app, .v-application, .v-application--wrap, .v-main {{
            background: transparent !important;
            background-color: transparent !important;
            min-height: 100vh !important;
            box-shadow: none !important;
        }}

        /* 3. UTILITIES */
        ::-webkit-scrollbar {{ width: 0px; background: transparent; }}
        .role-button:hover {{ transform: translateY(-5px) !important; }}
        * {{ font-family: 'Inter', sans-serif !important; }}
    """)

    if state.current_page.value == "home":
        Navbar()
        HomeView()
    elif state.current_page.value == "user":
        Navbar()
        user.UserFlow()
    elif state.current_page.value == "manager":
        Navbar()
        manager.ManagerView()
    elif state.current_page.value == "about":
        Navbar()
        about.AboutView()