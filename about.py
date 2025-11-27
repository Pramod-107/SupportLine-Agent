import solara
import backend as state # Assuming 'backend.py' is a separate file defining state variables

PRIMARY = state.TEXT_PRIMARY
SECONDARY = state.TEXT_SECONDARY
ACCENT = state.ACCENT_COLOR

# MODIFIED: All image URLs replaced with local filenames.
# IMPORTANT: Ensure 'avatar1.png', 'san.jpeg', and 'avatar3.png' are in the same folder as this script.
IMAGE_URLS = [
    "surya.jpeg", 
    "san.jpeg", 
    "var.jpeg"
]


@solara.component
def TeamCard(name, desc, img_url, linkedin_url):
    with solara.Column(style={
        "background": "rgba(255,255,255,0.6)", "backdrop-filter": "blur(10px)",
        "border-radius": "25px", "padding": "30px",
        "align-items": "center", "width": "350px", "height": "450px",
        "margin": "0 20px", "box-shadow": "0 15px 40px rgba(0,0,0,0.05)",
        "border": "1px solid rgba(255,255,255,0.4)",
        "transition": "transform 0.3s"
    }):
        with solara.Column(style={"width": "100px", "height": "100px", "border-radius": "50%", "overflow": "hidden",
                                    "margin-bottom": "20px", "background": "rgba(255,255,255,0.5)"}):
            # solara.Image handles both external URLs and local filenames
            solara.Image(img_url, width="100%")

        solara.Text(name, style={"color": PRIMARY, "font-size": "22px", "font-weight": "bold", "margin-bottom": "10px",
                                    "font-family": "Inter"})

        with solara.Column(style={"flex-grow": "1", "justify-content": "center"}):
            solara.Text(desc,
                        style={"color": SECONDARY, "font-size": "14px", "text-align": "center", "line-height": "1.6"})

        solara.HTML(unsafe_innerHTML=f"""
            <a href="{linkedin_url}" target="_blank" style="
                color: white; background-color: {ACCENT}; font-weight: 600; font-size: 14px;
                text-decoration: none; padding: 10px 25px; border-radius: 20px; margin-top: 20px;
                display: inline-block; font-family: 'Inter', sans-serif; box-shadow: 0 5px 15px {ACCENT}50;">
                Connect on LinkedIn
            </a>
        """)


@solara.component
def AboutView():
    with solara.Column(style={"height": "100vh", "width": "100%", "align-items": "center", "padding": "40px",
                                    "justify-content": "center"}):
        with solara.Row(style={"position": "absolute", "top": "30px", "left": "40px", "z-index": "10"}):
            solara.Button("← Back", on_click=lambda: state.current_page.set("home"), text=True,
                            style={"color": PRIMARY, "font-size": "18px", "padding": "10px 25px", "border-radius": "50px",
                                    "background-color": "rgba(255,255,255,0.7)", "font-family": "Inter",
                                    "font-weight": "bold", "box-shadow": "0 5px 15px rgba(0,0,0,0.05)"})

        solara.HTML(
            unsafe_innerHTML=f"<h1 style='font-family: Inter; font-size: 50px; color: {PRIMARY}; margin-bottom: 20px; font-weight: 700; text-shadow: 0 2px 10px rgba(255,255,255,0.5);'>Our Team</h1>")

        solara.Text("Students from Amrita Vishwa Vidyapeetham blending design and AI.",
                        style={"color": SECONDARY, "font-size": "18px", "margin-bottom": "50px"})

        with solara.Row(style={"justify-content": "center"}):
            TeamCard("Surya Pramod .J",
                        "AI Engineering Freshman. Committed to building strong foundations in AI systems.", IMAGE_URLS[0],
                        "https://www.linkedin.com/in/surya-pramod-josyula")
            TeamCard("Sanka Santosh", "Passionate about innovation and problem-solving in dynamic tech environments.",
                        IMAGE_URLS[1], "https://www.linkedin.com/in/santhosh-sanka-995b25205/")
            TeamCard("K.C.S Varshith", "Aspiring engineer with analytical thinking and dedication to excellence.",
                        IMAGE_URLS[2], "https://www.linkedin.com/in/varshith-kcs-24509b207/")