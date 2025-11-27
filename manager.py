import solara
import backend as state
# import asyncio # Removed: No longer needed for auto-dismissal

# --- THEME COLORS ---
PRIMARY = state.TEXT_PRIMARY
ACCENT = state.ACCENT_COLOR
SECONDARY = state.TEXT_SECONDARY
CATEGORIES = ["Police", "Hospital", "Cyber Crime", "Consultation", "Pharmacy", "Fire/Emergency"]


@solara.component
def SuccessOverlay():
    
    def start_new_registration():
        """Resets only the form fields and closes the popup."""
        state.mgr_name.set("New Center")
        state.mgr_type.set("Police")
        state.mgr_phone.set("8121203705")
        state.mgr_area.set("Indiranagar")
        state.show_registration_success.set(False)

    def go_to_home():
        """Resets the form fields and navigates to the home page."""
        start_new_registration() # Reset form fields
        state.current_page.set("home")
    
    # Custom Overlay structure to accommodate buttons
    with solara.Column(style={
        "position": "fixed", "top": 0, "left": 0, "width": "100%", "height": "100%",
        "background-color": "rgba(0, 0, 0, 0.7)", "z-index": 9999, 
        "justify-content": "center", "align-items": "center"
    }):
        with solara.Column(style={
            "background": "white", "padding": "40px", "border-radius": "15px", "width": "400px",
            "align-items": "center", "box-shadow": "0 10px 40px rgba(0,0,0,0.5)"
        }):
            # Success Icon/Text
            solara.HTML(unsafe_innerHTML=f"""
                <div style='color: #065f46; font-size: 50px;'>✅</div>
                <h3 style='color: {PRIMARY}; font-weight: bold; margin-bottom: 5px;'>Registration Completed Successfully!</h3>
                <p style='color: {SECONDARY}; font-size: 14px; margin-bottom: 25px;'>The new center is now active in the simulation.</p>
            """)
            
            # Action Buttons
            with solara.Column(gap="10px", style={"width": "100%"}):
                solara.Button("New Registration", on_click=start_new_registration,
                                style={"background-color": ACCENT, "color": "white", "width": "100%", "font-weight": "bold"})
                solara.Button("← Back to Home", on_click=go_to_home,
                                style={"background-color": SECONDARY, "color": "white", "width": "100%", "font-weight": "bold"})


@solara.component
def ManagerView():
    def register():
        state.model_instance.add_agent(category=state.mgr_type.value, name=state.mgr_name.value, address="Bangalore",
                                       phone=state.mgr_phone.value, location_name=state.mgr_area.value)
        
        # FIX FOR TABLE UPDATE: Mutate a user-facing reactive state.
        # This ensures that when the user switches to the UserDashboard, Solara sees a state change
        # and correctly re-runs functions that rely on model data (like get_centers).
        current_cat = state.selected_category.value
        state.selected_category.set("TEMPORARY")
        state.selected_category.set(current_cat)
        
        state.show_registration_success.set(True)

    with solara.Column(style={"height": "100vh", "width": "100%", "align-items": "center", "padding": "40px",
                              "justify-content": "center"}):
        # --- Top Left Back Button (Matches About Page) ---
        with solara.Row(style={"position": "absolute", "top": "30px", "left": "40px", "z-index": "10"}):
            solara.Button("← Back", on_click=lambda: state.current_page.set("home"), text=True,
                          style={"color": PRIMARY, "font-size": "18px", "padding": "10px 25px", "border-radius": "50px",
                                 "background-color": "rgba(255,255,255,0.7)", "font-family": "Inter",
                                 "font-weight": "bold", "box-shadow": "0 5px 15px rgba(0,0,0,0.05)"})

        # --- Main Heading ---
        solara.HTML(
            unsafe_innerHTML=f"<h1 style='font-family: Inter; font-size: 50px; color: {PRIMARY}; margin-bottom: 20px; font-weight: 700; text-shadow: 0 2px 10px rgba(255,255,255,0.5);'>Register your center here!</h1>")

        # --- Subtitle ---
        solara.Text("Join our network to provide real-time emergency assistance.",
                    style={"color": SECONDARY, "font-size": "18px", "margin-bottom": "40px"})

        # --- Registration Form (Glass Style) ---
        with solara.Column(style={
            "width": "500px",
            "background-color": "rgba(255,255,255,0.6)",
            "backdrop-filter": "blur(15px)",
            "padding": "40px", "border-radius": "30px",
            "box-shadow": "0 20px 50px rgba(0,0,0,0.05)",
            "border": "1px solid rgba(255,255,255,0.4)",
            "gap": "25px"
        }):
            solara.InputText("Center Name", value=state.mgr_name)
            solara.Select("Location", values=list(state.BANGALORE_LOCATIONS.keys()), value=state.mgr_area)
            solara.Select("Type", values=CATEGORIES, value=state.mgr_type)
            solara.InputText("Phone", value=state.mgr_phone)

            solara.Button("Submit Registration", on_click=register, style={
                "width": "100%", "height": "55px", "margin-top": "15px", "border-radius": "15px",
                "background-color": ACCENT, "color": "white", "font-family": "Inter",
                "font-weight": "bold", "border": "none", "font-size": "16px", "box-shadow": f"0 10px 20px {ACCENT}40"
            })

        if state.show_registration_success.value:
            SuccessOverlay()