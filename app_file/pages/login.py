#importing nesesery librery 
import flet as ft
from app_file.base64image import icons
import requests
import json
import bcrypt
import time


password_login_student_drive_url ="https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/user.json"

def check_login(username,password):
    url = f"{password_login_student_drive_url}?nocache={int(time.time())}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print("⚠️ Could not fetch data from Drive")
            return False

        data = json.loads(response.text)

    except Exception as e:
        print("❌ Error fetching data:", e)
        return False

    # Make sure "students" is a list
    for s in data.get("students", []):
        if s.get("username", "").lower() == username.lower():
            hashed = s.get("mp", "").encode()

            # Check if password matches hash
            return bcrypt.checkpw(password.encode(), hashed)

    return False




def login(page: ft.Page):

    


    # importing font
    page.fonts = {"Koulen": r"font\koulen\Koulen-Regular.ttf",
                  "amiri" : r"font\amiri\Amiri-Regular.ttf"}


    # page config
    page.title = "Archemedia School"
    page.bgcolor = "#C0DA4A"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Function to build UI depending on screen size
    def build_ui():
        page.clean()

        # scale based on screen width (mobile or desktop)
        w = page.width
        h = page.height

        ellipse = ft.Container(
            width=w * 0.7,
            height=h * 1.2,
            bgcolor="#0C6D26",
            border_radius=w,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=-h * 0.15),
        )

        title = ft.Text(
            "ARCHEMEDE SCHOOL",
            weight="bold",
            color="white",
            size=w * 0.08 if w < 600 else 35,
            font_family="Koulen",
            text_align="center",
            width=w * 0.8,
        )

        line = ft.Container(
            width=w * 0.7,
            height=3,
            bgcolor="white",
        )
        def log_in(e):
            
            
            user = username_field.value
            pas = password_field.value
            loading.visible = True      # show circle
            page.update()

            # simulate checking process
            time.sleep(2)


            if not user or not pas:
                password_field.error_text = "Please enter both username and password"
                username_field.error_text = "Please enter both username and password"
                page.update()
                print('no user or password was put')
                loading.visible = False   # hide circle
                page.update()
                return
            elif check_login(user,pas):
                print("check_login")
                print('log in succes')
                loading.visible = False   # hide circle
                page.update()
                page.session.set("username", user)
                time.sleep(1)
                return page.go("/home")
            else:
                password_field.error_text = "Invalid username or password"
                username_field.error_text = "Invalid username or password"
                print("check_login")
                print('no')
                loading.visible = False   # hide circle
                page.update()
                return 
            

        username_field = ft.TextField(
            hint_text="username",
            width=w * 0.7,
            height=h * 0.08,
            bgcolor="white",
            border_radius=10,
            text_size=w * 0.05 if w < 500 else 20,
            color="black",
        )

        password_field = ft.TextField(
            hint_text="password",
            password=True,
            can_reveal_password=True,
            width=w * 0.7,
            height=h * 0.08,
            bgcolor="white",
            border_radius=10,
            text_size=w * 0.05 if w < 500 else 20,
            color="black",
        )

        

        login_button = ft.ElevatedButton(
            "Log in",
            width=w * 0.7,
            height=h * 0.08,
            bgcolor="#E1E645",
            color="black",
            on_click=log_in,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                shadow_color="black",
                elevation=6,
            ),
        )
        loading = ft.ProgressRing(visible=False, width=25, height=25, color="black")  # ⭕ small spinner


        logo = ft.Image(
            src_base64=icons[0],
            width=w * 0.3,
            height=h * 0.15,
            fit=ft.ImageFit.CONTAIN,
        )

        green_box = ft.Container(
            width=w * 0.8,
            height=h * 0.45,
            bgcolor="#27943E",
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=10, color=ft.Colors.BLACK26),
            border_radius=10,
            padding=20,
            content=ft.Column(
                [username_field,loading, password_field,loading, login_button],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # Main layout
        page.add(
            ft.Stack(
                [
                    ft.Container(content=ellipse, alignment=ft.alignment.center),
                    ft.Column(
                        [
                            ft.Container(content=logo, alignment=ft.alignment.center),
                            ft.Container(content=title, alignment=ft.alignment.center),
                            ft.Container(content=line, alignment=ft.alignment.center),
                            ft.Container(content=green_box, alignment=ft.alignment.center),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
        )

    # Run once and when resized
    def resize(e):
        build_ui()

    page.on_resize = resize
    build_ui()

