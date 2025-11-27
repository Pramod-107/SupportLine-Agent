import solara
import backend as state
from ipyleaflet import Map, Marker, AwesomeIcon, Polyline, basemaps
from ipywidgets import HTML, Layout

# --- THEME COLORS ---
PRIMARY = state.TEXT_PRIMARY
SECONDARY = state.TEXT_SECONDARY
ACCENT = state.ACCENT_COLOR
ICON_MAPPING = state.ICON_MAPPING


@solara.component
def RealMap():
    u_lat, u_lon = state.user_current_coords.value

    centers = solara.use_memo(
        lambda: state.model_instance.get_centers(state.selected_category.value),
        [state.selected_category.value]
    )

    m = Map(center=(u_lat, u_lon), zoom=13, scroll_wheel_zoom=True,
            basemap=basemaps.OpenStreetMap.Mapnik,
            layout=Layout(width='100%', height='70vh'))

    m.add_layer(Marker(location=(u_lat, u_lon), icon=AwesomeIcon(name='user', marker_color='blue', icon_color='white'),
                       title="You"))

    icon_dict = {"Police": "shield", "Hospital": "plus", "Cyber Crime": "lock", "Consultation": "info",
                 "Pharmacy": "medkit", "Fire/Emergency": "fire"}

    for c in centers:
        is_target = (state.target_center.value and state.target_center.value.unique_id == c.unique_id)
        color = 'red' if is_target else 'cadetblue'
        m.add_layer(Marker(location=(c.lat, c.lon),
                           icon=AwesomeIcon(name=icon_dict.get(c.p_type, "building"), marker_color=color,
                                            icon_color='white'), title=f"{c.name}"))

    if state.show_route.value and state.target_center.value:
        target = state.target_center.value
        m.add_layer(
            Polyline(locations=[(u_lat, u_lon), (target.lat, target.lon)], color="#2563EB", fill=False, weight=4))

    solara.display(m)


@solara.component
def CleanTable():
    u_lat, u_lon = state.user_current_coords.value

    centers = solara.use_memo(
        lambda: state.model_instance.calculate_metrics(u_lat, u_lon, state.selected_category.value),
        [u_lat, u_lon, state.selected_category.value]
    )

    with solara.Column(style={"height": "100%", "overflow-y": "auto", "background": "white", "border-radius": "15px",
                              "box-shadow": "0 4px 20px rgba(0,0,0,0.05)"}):
        # HEADER
        with solara.Row(style={"background": "#f8fafc", "padding": "15px", "color": PRIMARY, "font-weight": "bold"}):
            solara.Text("Name", style={"width": "40%"})
            solara.Text("Phone", style={"width": "30%"})
            solara.Text("Dist.", style={"width": "15%"})
            solara.Text("Call", style={"width": "15%", "text-align": "right"})

        # DATA ROWS
        for c in centers:
            is_target = (state.target_center.value and state.target_center.value.unique_id == c.unique_id)
            bg = "#e0f2fe" if is_target else "transparent"

            def on_row_click(center=c):
                state.target_center.set(center)
                state.show_route.set(True)

                # MAIN ROW CONTAINER

            with solara.Row(style={"background": bg, "border-bottom": "1px solid #f1f5f9", "padding": "0",
                                   "align-items": "center"}):
                # LEFT SIDE: Button acting as a clickable row (85% width)
                # We style it to look like plain text (transparent bg, no shadow)
                with solara.Button(
                        on_click=on_row_click,
                        style={
                            "width": "85%",
                            "background-color": "transparent",
                            "border": "none",
                            "box-shadow": "none",
                            "text-transform": "none",  # Prevents uppercase text
                            "padding": "12px",
                            "display": "block"  # Ensures internal Row takes full width
                        }
                ):
                    # Use a Row inside the button to align columns
                    with solara.Row(style={"width": "100%", "background": "transparent", "gap": "0"}):
                        solara.Text(c.name, style={"width": "47%", "text-align": "left", "color": SECONDARY,
                                                   "font-weight": "500"})
                        solara.Text(c.phone, style={"width": "35%", "text-align": "left", "color": SECONDARY})
                        solara.Text(f"{c.distance_to_user}km",
                                    style={"width": "18%", "text-align": "left", "color": PRIMARY,
                                           "font-weight": "bold"})

                # RIGHT SIDE: Call Button (15% width) - Outside the main button
                with solara.Row(style={"width": "15%", "padding": "12px", "justify-content": "flex-end"}):
                    solara.HTML(
                        unsafe_innerHTML=f'<a href="tel:{c.phone}" target="_blank" style="text-decoration:none; font-size:18px; color: {ACCENT};">📞</a>'
                    )


@solara.component
def UserDashboard():
    def update_location(value):
        new_coords = state.get_coordinates(value)
        state.user_current_coords.set(new_coords)
        state.target_center.set(None)
        state.nearest_found.set(False)

    def find_nearest_click():
        best = state.model_instance.find_nearest_using_heuristic(*state.user_current_coords.value,
                                                                 state.selected_category.value)
        if best:
            state.target_center.set(best)
            state.nearest_found.set(True)

    with solara.Column(style={"padding": "0 40px", "width": "100%", "height": "100%"}):

        # Back Button
        with solara.Row(style={"margin-bottom": "10px"}):
            solara.Button("← Back", on_click=lambda: state.user_view_step.set(1), text=True,
                          style={"font-weight": "bold", "color": SECONDARY, "padding": "0", "font-size": "16px"})

        with solara.Row(style={"margin-bottom": "20px", "align-items": "center", "justify-content": "space-between"}):
            solara.HTML(
                unsafe_innerHTML=f"<h2 style='color:{PRIMARY}; font-family: Inter; font-weight: 700; font-size: 30px; margin: 0;'>{state.selected_category.value}</h2>")

        with solara.Row(style={"height": "calc(100vh - 220px)", "gap": "30px"}):

            # Left Panel
            with solara.Column(style={"width": "35%", "height": "100%", "gap": "20px"}):
                with solara.Column(style={"background": "white", "padding": "25px", "border-radius": "20px",
                                          "box-shadow": "0 10px 30px rgba(0,0,0,0.05)"}):

                    solara.InputText(label="Current Location",
                                     value=state.user_location_input,
                                     on_value=update_location,
                                     continuous_update=False)

                    if not state.nearest_found.value:
                        solara.Button("Find Nearest", on_click=find_nearest_click,
                                      style={"background-color": ACCENT, "color": "white", "width": "100%",
                                             "margin-top": "15px", "border-radius": "10px", "height": "45px"})
                    else:
                        name = state.target_center.value.name if state.target_center.value else ""
                        solara.Text(f"Nearest: {name}",
                                    style={"color": PRIMARY, "font-weight": "bold", "margin-top": "10px"})
                        if not state.show_route.value:
                            solara.Button("Show Route", on_click=lambda: state.show_route.set(True),
                                          style={"background-color": PRIMARY, "color": "white", "width": "100%",
                                                 "border-radius": "10px"})
                CleanTable()

            # Right Panel (Map)
            with solara.Column(style={"width": "65%", "height": "100%", "border-radius": "20px", "overflow": "hidden",
                                      "box-shadow": "0 10px 30px rgba(0,0,0,0.05)"}):
                RealMap()


@solara.component
def UserSelectionView():
    with solara.Column(align="center", style={"width": "100%", "height": "calc(100vh - 100px)", "overflow": "hidden"}):
        solara.HTML(unsafe_innerHTML=f"""
            <h2 style='color: {PRIMARY}; text-align: center; margin-top: 40px; font-size: 40px; font-family: "Inter", sans-serif; font-weight: 700;'>
                Select Assistance Type
            </h2>
        """)

        def select(p):
            state.selected_category.set(p)
            state.user_view_step.set(2)

        with solara.Column(style={"width": "100%", "max-width": "1200px", "padding": "20px", "margin-top": "20px"}):
            with solara.GridFixed(columns=3):
                for p in ["Police", "Hospital", "Cyber Crime", "Consultation", "Pharmacy", "Fire/Emergency"]:
                    with solara.Button(on_click=lambda v=p: select(v),
                                       style={
                                           "height": "180px", "width": "90%", "margin": "15px auto",
                                           "background-color": "white",
                                           "border": "none", "border-radius": "20px",
                                           "box-shadow": "0 10px 30px rgba(0,0,0,0.05)",
                                           "display": "flex", "flex-direction": "column", "align-items": "center",
                                           "justify-content": "center", "gap": "20px",
                                           "position": "relative",
                                           "transition": "transform 0.2s ease"
                                       },
                                       classes=["role-button"]
                                       ):
                        with solara.Column(style={"position": "absolute", "top": "20px", "left": "25px",
                                                  "background-color": ACCENT, "padding": "8px",
                                                  "border-radius": "4px"}):
                            icon_url = ICON_MAPPING.get(p, ICON_MAPPING["Consultation"])
                            solara.Image(icon_url, width="25px")

                        solara.Text(p.upper(), style={"color": PRIMARY, "font-weight": "bold", "font-size": "16px",
                                                      "letter-spacing": "1px"})


@solara.component
def UserFlow():
    if state.user_view_step.value == 1:
        UserSelectionView()
    else:
        UserDashboard()