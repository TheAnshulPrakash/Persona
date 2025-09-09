import flet as ft
import asyncio
import json
import os
import random
import aiohttp
import base64
import threading
import eye_detection
from ollama_gpt import GPTInterview
from datetime import datetime

animation_running=True
current_theme=ft.Colors.INDIGO
current_text_theme=ft.Colors.WHITE
video_running=True
async def breath(page: ft.Page, circle: ft.Container, text: ft.Container):
    
    global animation_running
    
    
    
    while animation_running:
        
        val=random.randint(500,650)
        
        circle.width = val
        circle.height = val
        circle.gradient = ft.RadialGradient(
            colors=[current_theme, ft.Colors.BLACK],
            radius=0.5,
        )
        
        text.opacity=1.0        
        circle.update()
        await asyncio.sleep(4)

        val=random.randint(400,450)
        circle.width = val
        circle.height = val
        circle.gradient = ft.RadialGradient(
            colors=[current_theme, ft.Colors.BLACK],
            radius=0.5,
        )
        text.opacity = 0.5
        circle.update()
        await asyncio.sleep(4)


async def main(page: ft.Page):
    page.bgcolor = "black"
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.resizable = False
    page.title = "Persona"
    page.window.maximized = True
    page.padding=10
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    
    page.fonts={
        "Montserrat": "fonts/Montserrat-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Montserrat")
    
    
    def find_valid_json_files():
        valid_files = []
        for file_name in os.listdir("."):  # current directory
            if file_name.endswith(".json"):
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        json.load(f)  # check if valid JSON
                    valid_files.append(file_name)
                except Exception:
                    pass  # ignore invalid JSON files
        return valid_files

    files_history=find_valid_json_files()
    
    async def load_result(e):
        i=e.control.selected_index
        asyncio.create_task(resultboard(files_history[i]))
    
    end_drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("History", size=18, weight="bold", text_align=ft.TextAlign.CENTER)
        ] + [
            ft.NavigationDrawerDestination(
                icon=ft.Icons.DESCRIPTION,  # you can choose icons dynamically too
                label=file_name
            )
            for file_name in files_history
        ],
        bgcolor="#201D1D",
        selected_index=None,
        indicator_color=current_theme,
        position=ft.NavigationDrawerPosition.START,
        on_change=load_result
    )
    
    
    
    
    def open_end_drawer(e):
        e.control.page.end_drawer = end_drawer
        end_drawer.open = True
        e.control.page.update()


    
    initial_content=ft.Row([ft.Image("images/Persona_logo.png", height=40, width=40, ),
                ft.Text("Persona — Mock Interviews. Perfected.", size=30, weight="bold", color="white")])
    menu_button=ft.IconButton(icon=ft.Icons.MENU_SHARP, icon_color=current_text_theme,icon_size=40, on_click=open_end_drawer)
    
    
    persona_headline=ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(expand=True),  
                        initial_content,
                        ft.Container(expand=True, alignment=ft.alignment.center_right,
                                    content=menu_button),
                    ],
                    expand=True
                )
            ],
            expand=True
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=30),
        opacity=1.0,
        animate_opacity=4000,
        
    )
    
    
    
    
    all_skills=ft.Column([], wrap=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_EVENLY,)

    
    professions = {
    "⚙️ STEM & Engineering": [
        "Computer Engineer / Software Developer",
        "Data Scientist / AI-ML Engineer",
        "Cybersecurity Specialist",
        "Mechanical Engineer",
        "Electrical Engineer",
        "Civil Engineer",
        "Chemical Engineer",
        "Biotechnology Professional",
        
    ],
    "💼 Business & Management": [
        "Business & Management Professional",
        "Finance Professional",
        "Marketing Professional",
        
        "Consultant",
        "Product Manager",
    ],
    "🎨 Creative & Media": [
        "Designer / Creative Professional",
        "Artist / Performing Arts Professional",
        "Media & Journalism Professional",
        "Writer / Author",
        "Film & Entertainment Professional",
    ],
    "⚕️ Healthcare & Life Sciences": [
        "Healthcare Professional",
        "Pharmaceutical Professional",
        "Public Health Specialist",
        "Psychologist / Mental Health Professional",
    ],
    "📚 Education & Research": [
        "Education & Research Professional",
        "Scientist / Researcher",
        "Academic Faculty",
    ],
    "⚖️ Law & Public Service": [
        "Law / Legal Professional",
        "Civil Services / Government Administration",
        "Defence & Armed Forces Professional",
        "Police / Law Enforcement",
        "Politician / Policy Maker",
        "Social Work & NGO Professional",
    ],
    "🌍 Skilled Trades & Others": [
        "Skilled Trades Professional (e.g., Electrician, Plumber, Carpenter)",
        "Agriculture & Environmental Professional",
        "Transport & Logistics Professional",
        "Hospitality & Tourism Professional",
        "Sports Professional / Athlete",
    ],
    "🌐 Digital & Emerging Technologies": [
        "Cloud Computing Specialist",
        "Blockchain Developer",
        "AR/VR Developer",
        "Robotics Engineer",
        "Quantum Computing Researcher",
        ]
    }

    user_description_field=ft.TextField(multiline=True, hint_text="This could include your skills, work experience, etc.", width=450, border_radius=35, border_color=current_text_theme, max_lines=20, cursor_color=current_theme)
    employer_description_field=ft.TextField(multiline=True, hint_text="Describe what your employer expects from candidates", width=450, border_radius=35, border_color=current_text_theme, max_lines=20, cursor_color=current_theme)
    
    async def job_description(e):
        e.control.selected=True
        e.control.update()
        
        
       
        get_started.opacity=0 
        get_started.update()
        await asyncio.sleep(0.7)
        
        circle.height=650
        circle.width=650
        get_started.content=ft.Column([ft.Text("Describe about employer's details", size=35),ft.Divider(height=1, trailing_indent=600, leading_indent=600, color=current_text_theme),
                    employer_description_field,
                    ft.Row([ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT_SHARP, icon_color=current_text_theme, on_click=user_description),
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT_SHARP, icon_color=current_text_theme, on_click=dashboard),], alignment=ft.MainAxisAlignment.CENTER)],
                                      scroll="auto",spacing=20,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand_loose=True, )
        await asyncio.sleep(0.5)
        get_started.opacity=1
        get_started.update()
        
    live_image= ft.Image("Squares Loader.gif",expand=True
                   )
    
    
    
    def run_cv():
        
        eye_detection.run()
    async def image_update(live_image, page):
        global video_running
        threading.Thread(target=run_cv, daemon=True).start()
        
        
        async with aiohttp.ClientSession() as session:
            while video_running:
                try:
                    async with session.get("http://localhost:5000/frame.jpg") as resp:
                        if resp.status == 200:
                            data = await resp.read()
                            b64 = base64.b64encode(data).decode("utf-8")
                            live_image.src_base64 = b64
                            live_image.src = None
                            live_image.update()  
                except Exception as e:
                    print("Error fetching frame:", e)

                await asyncio.sleep(0.03)  
            
    
    mic_container=ft.Container(
                        content=ft.IconButton(icon=ft.Icons.MIC_SHARP,  icon_size=50,disabled=True),   
                        bgcolor="#000000",
                        expand=True,
                        border_radius=35,
                        padding=15,
                        shadow=ft.BoxShadow(
                            spread_radius=5,
                            blur_radius=15,
                            color=current_theme,
                            offset=ft.Offset(2, 2),
                        ),
                        alignment=ft.alignment.center
                    )
    
    text=ft.Text("Getting things ready",size=30, text_align=ft.TextAlign.CENTER)
    
    conv_container=ft.Container(
                    content=ft.Column([text,ft.Image("Square Rotator.gif")], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor='#000000',
                    expand=6,
                    border_radius=35,
                    padding=15,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=5,
                        blur_radius=15,
                        color=current_theme,
                        offset=ft.Offset(2, 2),
                    ),
                )
    
    
    image_stats={
        "good_count": 70,
        "bad_count": 38,
        "lost_count":1
    }
    async def dashboard(e):
        now = datetime.now()


        date_str = now.strftime("%d-%m")
        time_str = now.strftime("%H-%M")


        file_name = f"{date_str}, {time_str}.json"
        
        with open(file_name,'a') as f:
            f.write('[')
        global animation_running
        animation_running=False
        print("coming")
        get_started.opacity = 0
        get_started.update()
        await asyncio.sleep(0.7)

        get_started.content = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Container(
                        live_image,
                        expand=True,
                        bgcolor="#000000",
                        width=800,
                        border_radius=35,
                        shadow=ft.BoxShadow(
                            spread_radius=5,
                            blur_radius=15,
                            color=current_theme,
                            offset=ft.Offset(2, 2),
                        ),
                    ),
                    mic_container,
                ], expand=3, spacing=35),
                conv_container,
                
            ], expand=True, spacing=35)
        ], expand=True, spacing=35)
        
        user_info=user_description_field.value
        nonlocal job_role
        print(job_role)
        
        interview = GPTInterview(
                user_info=user_info,
                job_role=job_role,
                interview_type="friendly",
                no_of_questions=20,
                interview_req=employer_description_field.value,
                file_name=file_name
                
            )
        

        get_started.update()
        get_started.expand = True

        asyncio.create_task(image_update(live_image, page))
        
        

        await asyncio.sleep(0.7)

        get_started.opacity = 1
        get_started.update()
        page.update()

        t=threading.Thread(target=interview.chat_with_model, args=("start", conv_container, text, mic_container, current_theme, current_text_theme), daemon=True)
        t.start()
        
        async def monitor_thread():
            while t.is_alive():
                await asyncio.sleep(1)  
            print("Interview Done")
            with open(file_name, "r+", encoding="utf-8") as f:
                content = f.read().strip()

               
                if content.endswith(","):
                    content = content[:-1]
                    print("Removed trailing comma.")

                
                if not content.startswith("["):
                    content = "[" + content
                if not content.endswith("]"):
                    content = content + "]"

                
                f.seek(0)
                f.write(content)
                f.truncate()
                
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get("http://localhost:5000/stop") as resp:
                        if resp.status == 200:
                            nonlocal image_stats
                            image_stats = await resp.json()
                            print("image stats are:", image_stats)
                            print("Final CV Stats:", image_stats)  
                            global video_running
                            video_running=False
                except Exception as e:
                    print("Error calling stop:", e)
                await resultboard(file_name)
                
                
            

        # Run monitor in background
        asyncio.create_task(monitor_thread())
                
        
        
    async def resultboard(file_name):
        
        global animation_running
        animation_running=False
        persona_headline.opacity=1.0
        
        circle.content=ft.Row([])
        circle.width=0
        circle.height=0
        circle.update()
        
        get_started.opacity = 0
        get_started.update()
        await asyncio.sleep(0.7)
        
        with open(file_name, "r",) as f:
            data = json.load(f)
        
        questions = [d["question_number"] for d in data]
        english_scores = [d["evaluation"]["english_proficiency"] for d in data]
        confidence_scores = [d["evaluation"]["confidence"] for d in data]
        quality_scores = [d["evaluation"]["content_quality"] for d in data]
        
        notes = [(d["question_number"], d["evaluation"]["notes"]) for d in data][1:]

        note_rows = [
                    ft.Row(
                        controls=[
                            ft.Text(f"Q{q-1}:", weight="bold", size=25),
                            ft.Text(note if note else "(No notes)", size=25)
                            
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        wrap=True
                    )
                    for q, note in notes
                ]

        notes_column = ft.Column(controls=note_rows, spacing=8, expand=True, scroll="auto")
        
        print(english_scores,confidence_scores, quality_scores)
        nonlocal image_stats

        def build_line_chart(title, scores, color):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, weight="bold"),
                    ft.LineChart(
                        animate=1000,
                        expand=True,
                        min_y=0,
                        max_y=10,
                        min_x=min(questions),
                        max_x=max(questions),
                        border=ft.Border(
                            left=ft.BorderSide(2, ft.Colors.GREY),
                            bottom=ft.BorderSide(2, ft.Colors.GREY),
                        ),
                    
                        left_axis=ft.ChartAxis(labels_size=30, title=ft.Text("Score")),
                        bottom_axis=ft.ChartAxis(
                            labels_size=20,
                            title=ft.Text("Question"),
                            labels=[
                                ft.ChartAxisLabel(
                                    value=q,
                                    label=ft.Text(str(q), size=10)
                                )
                                for q in questions
                            ],
                        ),

                        data_series=[
                            ft.LineChartData(
                                data_points=[
                                    ft.LineChartDataPoint(q, s)
                                    for q, s in zip(questions, scores) if s is not None
                                ],
                                stroke_width=3,
                                color=color,
                                curved=True,
                                stroke_cap_round=True,
                                point=True,
                            )
                        ]
                    )
                ]),
                
                height=450,
                border_radius=15,
                bgcolor=ft.Colors.BLACK,
                shadow=ft.BoxShadow(
                        spread_radius=5,
                        blur_radius=15,
                        color=current_theme,
                        offset=ft.Offset(2, 2),
                    ),
                
                padding=10,
                expand=True
            )
        

        chart1 = build_line_chart("English Proficiency", english_scores, current_theme)
        chart2 = build_line_chart("Confidence", confidence_scores, current_theme)
        chart3 = build_line_chart("Content Quality", quality_scores, current_theme)
        
        s=(image_stats['good_count']+image_stats['bad_count']+image_stats['lost_count'])
        good=(image_stats['good_count']/s)*100
        bad=(image_stats['bad_count']/s)*100
        lost=(image_stats['lost_count']/s)*100
        
        chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=good,
                        width=40,
                        color="#269DA1",
                
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=bad,
                        width=40,
                        color="#DC4C28",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=lost,
                        width=40,
                        color="#747272",
                        border_radius=0,
                    ),
                ],
            ),
            
        ],
        border=ft.border.all(1, ft.Colors.GREY_400),
        left_axis=ft.ChartAxis(
            labels_size=40, title=ft.Text("Percentage"), title_size=40
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0, label=ft.Container(ft.Text("Good Posture"), padding=10)
                ),
                ft.ChartAxisLabel(
                    value=1, label=ft.Container(ft.Text("Bad Posture"), padding=10)
                ),
                ft.ChartAxisLabel(
                    value=2, label=ft.Container(ft.Text("Lost"), padding=10)
                ),
                
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
        max_y=110,
        interactive=True,
        expand=True,
    )
        
        get_started.content=ft.Column([ft.Row([
                chart1, chart2, chart3
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_EVENLY),ft.Row([chart, notes_column,],expand=True)], spacing=20)        
            
        await asyncio.sleep(0.7)
        get_started.opacity = 1
        get_started.update()
        page.update()
        
        
    
        
    
        
    def cv_uploaded(e):
        
        
        global animation_running
        animation_running=False
        persona_headline.opacity=1.0
        
        circle.content=ft.Row([])
        circle.width=0
        circle.height=0
        
        circle.update()
        
        print("Coming")
        
    job_role=None
    async def user_description(e):
        nonlocal job_role
        job_role=e.control.data
        
        e.control.selected=True
        e.control.update()
        
        
       
        get_started.opacity=0 
        get_started.update()
        await asyncio.sleep(0.7)
        
        circle.height=650
        circle.width=650
        get_started.content=ft.Column([ft.Text("Describe about yourself", size=35),ft.Divider(height=1, trailing_indent=600, leading_indent=600, color=current_text_theme),
                    user_description_field, 
                    ft.Row([ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT_SHARP, icon_color=current_text_theme, on_click=profession_selection),
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT_SHARP, icon_color=current_text_theme, on_click=job_description),], alignment=ft.MainAxisAlignment.CENTER)],
                                      scroll="auto",spacing=20,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand_loose=True, )
        await asyncio.sleep(0.5)
        get_started.opacity=1
        get_started.update()
        
    
    async def role_selection(e):
        
        e.control.selected=True
        e.control.update()
        data=e.control.data
        
       
        get_started.opacity=0 
        get_started.update()
        await asyncio.sleep(0.7)
        
        circle.height=650
        circle.width=650
        all_skills.controls.clear()
        
        
        
        
        for amenity in professions[data]:
            all_skills.controls.append(
                ft.Chip(
                    label=ft.Text(amenity),
                    show_checkmark=True,
                    selected=False,
                    data=amenity,
                    on_click=user_description,
                    check_color=current_text_theme
                )
            )
        print(professions[data])
        get_started.content=ft.Column([ft.Text("Role you're looking for", size=35),ft.Divider(height=1, trailing_indent=600,leading_indent=600, color=current_text_theme),
                                       ft.Container(all_skills, ), ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT_SHARP, icon_color=current_text_theme, on_click=profession_selection)], scroll="auto",spacing=20,
                                      alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand_loose=True, )
        await asyncio.sleep(0.5)
        get_started.opacity=1
        get_started.update()
    
    files=None
        
    async def profession_selection(e):
        
        
        persona_headline.opacity=1.0
        persona_headline.update()
        
        get_started.opacity=0
        get_started.update()
        all_skills.controls.clear()
        
        
        
        await asyncio.sleep(0.7)
        
        circle.height=650
        circle.width=650
        
        for amenity in professions:
            all_skills.controls.append(
                ft.Chip(
                    label=ft.Text(amenity),
                    show_checkmark=True,
                    selected=False,
                    data=amenity,
                    on_click=role_selection,
                    check_color=current_text_theme
                )
            )
        get_started.content=ft.Column([ft.Text("Choose your Profession", size=35),ft.Divider(height=1, trailing_indent=600,leading_indent=600, color=current_text_theme),
                                       ft.Container(all_skills, height=200,)], scroll="auto",spacing=20,
                                      alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        await asyncio.sleep(0.2)
        get_started.opacity=1
        get_started.update()
        circle.update()
        
        
        
        
    file_picker=ft.FilePicker()
    file_picker.on_result=cv_uploaded
    
    page.overlay.append(file_picker)
    #page.update()
    
        
    async def get_started_1(e):
        
        get_started.opacity=0
        get_started.update()
        
        await asyncio.sleep(1.1)
        
        get_started.content=ft.Column([ft.Text("Upload your CV", size=25, weight="bold",
                                               tooltip="Get Persona analyze your skills by uploading your cv to get a tailored experience",
                                               color=current_text_theme,),
            ft.Row([ft.CupertinoButton("Select file",on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["docx", "pdf"]
        ), color=current_text_theme),
                    ft.CupertinoButton("Skip", on_click=profession_selection, color=current_text_theme)], alignment=ft.MainAxisAlignment.CENTER), 
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,expand=True)
        get_started.opacity=1
        get_started.update()
        
        
    get_started=ft.Container(
        opacity=1.0,
        animate_opacity=700,
        content=ft.Column([ft.Text("Hey Contender, ready to shine?", size=25, weight="bold", color=current_text_theme),
            ft.CupertinoButton("Get started ➔",on_click=get_started_1, color=current_text_theme, bgcolor='transparent'), ], 
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
        
    
    
    
    circle = ft.Container(gradient=ft.RadialGradient(
            colors=[current_theme, ft.Colors.BLACK],
            radius=0.5,
        ),
        width=200,
        height=200,
        border_radius=200,
        animate=ft.Animation(4000, ft.AnimationCurve.EASE_IN_OUT),
        alignment=ft.alignment.center,
        expand=True
    )

    
    
   
    layout = ft.Column([
            persona_headline,
            ft.Stack([
                ft.Container(expand=True, alignment=ft.alignment.center, content=circle),
                ft.Container(expand=True, alignment=ft.alignment.center, content=ft.Column([get_started], 
                                                        alignment=ft.MainAxisAlignment.CENTER,  
                                                                            expand=True) )
            ], expand=True),
    ft.Container(content=ft.Text("Developed by Anshul Prakash ◉ Powered by GPT-oss", size=10),alignment=ft.alignment.bottom_center),],
    
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )


    page.add(layout)
    
    

    
    asyncio.create_task(breath(page, circle,persona_headline))
    
    


ft.app(target=main, assets_dir="assets",)


