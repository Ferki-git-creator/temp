"""
Мобильное погодное приложение с Open-Meteo API
Для установки зависимостей:
pip install kivy kivymd requests geocoder
"""
import requests
from datetime import datetime, timedelta
import json
import geocoder
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import ListProperty
from kivy.animation import Animation
import webbrowser

# Локализация с текстовыми описаниями погоды
TRANSLATIONS = {
    'en': {
        'app_title': 'Weather App',
        'current_weather': 'Current Weather',
        'detecting_location': 'Detecting location...',
        'hourly_forecast': 'Hourly Forecast',
        'details': 'Details',
        'weekly_forecast': '7-Day Forecast',
        'forecast': 'Forecast',
        'select_city': 'Select City',
        'enter_city': 'Enter city name',
        'search': 'Search',
        'use_my_location': 'Use My Location',
        'found': 'Found:',
        'city_not_found': 'City not found',
        'pressure': 'Pressure',
        'feels_like': 'Feels Like',
        'cloudiness': 'Cloudiness',
        'sunrise': 'Sunrise',
        'sunset': 'Sunset',
        'visibility': 'Visibility',
        'wind': 'Wind',
        'humidity': 'Humidity',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'settings': 'Settings',
        'about': 'About App',
        'main': 'Main',
        'language': 'Language',
        'theme': 'Theme',
        'dark_theme': 'Dark Theme',
        'units': 'Units',
        'metric': '°C, m/s',
        'imperial': '°F, mph',
        'support_developer': 'Support Developer',
        'open_weather_map': 'Open Weather Map',
        'refresh': 'Refresh',
        'rain_map': 'Rain Map',
        'coordinates': 'Coordinates',
        'open_in_browser': 'Open in browser',
        'close': 'Close',
        'error': 'Error',
        'location_error': 'Failed to get location',
        'data_error': 'Failed to get data',
        'search_error': 'Search error',
        'uv_index': 'UV Index',
        'precipitation': 'Precipitation',
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'full_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'weather_conditions': {
            0: "Clear",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Cloudy",
            45: "Fog",
            48: "Fog with frost",
            51: "Drizzle",
            53: "Drizzle",
            55: "Heavy drizzle",
            56: "Freezing drizzle",
            57: "Heavy freezing drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Freezing rain",
            67: "Heavy freezing rain",
            71: "Light snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Light showers",
            81: "Moderate showers",
            82: "Heavy showers",
            85: "Light snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Heavy thunderstorm with hail"
        }
    },
    'uk': {
        'app_title': 'Погодний додаток',
        'current_weather': 'Поточна погода',
        'detecting_location': 'Визначення місця...',
        'hourly_forecast': 'Погодинний прогноз',
        'details': 'Деталі',
        'weekly_forecast': 'Прогноз на 7 днів',
        'forecast': 'Прогноз',
        'select_city': 'Вибір міста',
        'enter_city': 'Введіть назву міста',
        'search': 'Пошук',
        'use_my_location': 'Використати моє місце',
        'found': 'Знайдено:',
        'city_not_found': 'Місто не знайдено',
        'pressure': 'Тиск',
        'feels_like': 'Відчувається',
        'cloudiness': 'Хмарність',
        'sunrise': 'Схід сонця',
        'sunset': 'Захід сонця',
        'visibility': 'Видимість',
        'wind': 'Вітер',
        'humidity': 'Вологість',
        'today': 'Сьогодні',
        'tomorrow': 'Завтра',
        'settings': 'Налаштування',
        'about': 'Про додаток',
        'main': 'Головна',
        'language': 'Мова',
        'theme': 'Тема',
        'dark_theme': 'Темна тема',
        'units': 'Одиниці виміру',
        'metric': '°C, м/с',
        'imperial': '°F, миль/год',
        'support_developer': 'Підтримати розробника',
        'open_weather_map': 'Відкрити карту погоди',
        'refresh': 'Оновити',
        'rain_map': 'Карта опадів',
        'coordinates': 'Координати',
        'open_in_browser': 'Відкрити в браузері',
        'close': 'Закрити',
        'error': 'Помилка',
        'location_error': 'Не вдалося визначити місце',
        'data_error': 'Не вдалося отримати дані',
        'search_error': 'Помилка пошуку',
        'uv_index': 'УФ індекс',
        'precipitation': 'Опади',
        'days': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
        'full_days': ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя'],
        'weather_conditions': {
            0: "Ясно",
            1: "Переважно ясно",
            2: "Змінна хмарність",
            3: "Хмарно",
            45: "Туман",
            48: "Туман з інеєм",
            51: "Мряка",
            53: "Мряка",
            55: "Сильна мряка",
            56: "Крижана мряка",
            57: "Сильна крижана мряка",
            61: "Невеликий дощ",
            63: "Помірний дощ",
            65: "Сильний дощ",
            66: "Крижаний дощ",
            67: "Сильний крижаний дощ",
            71: "Невеликий сніг",
            73: "Помірний сніг",
            75: "Сильний сніг",
            77: "Снігові зерна",
            80: "Невеликі зливи",
            81: "Помірні зливи",
            82: "Сильні зливи",
            85: "Невеликі снігопади",
            86: "Сильні снігопади",
            95: "Гроза",
            96: "Гроза з градом",
            99: "Сильна гроза з градом"
        }
    },
    'ru': {
        'app_title': 'Погодное приложение',
        'current_weather': 'Текущая погода',
        'detecting_location': 'Определение местоположения...',
        'hourly_forecast': 'Погодинный прогноз',
        'details': 'Детали',
        'weekly_forecast': 'Прогноз на 7 дней',
        'forecast': 'Прогноз',
        'select_city': 'Выбор города',
        'enter_city': 'Введите название города',
        'search': 'Поиск',
        'use_my_location': 'Использовать моё местоположение',
        'found': 'Найдено:',
        'city_not_found': 'Город не найден',
        'pressure': 'Давление',
        'feels_like': 'Ощущается',
        'cloudiness': 'Облачность',
        'sunrise': 'Восход',
        'sunset': 'Закат',
        'visibility': 'Видимость',
        'wind': 'Ветер',
        'humidity': 'Влажность',
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'settings': 'Настройки',
        'about': 'О приложении',
        'main': 'Главная',
        'language': 'Язык',
        'theme': 'Тема',
        'dark_theme': 'Темная тема',
        'units': 'Единицы измерения',
        'metric': '°C, м/с',
        'imperial': '°F, миль/ч',
        'support_developer': 'Поддержать разработчика',
        'open_weather_map': 'Открыть карту погоды',
        'refresh': 'Обновить',
        'rain_map': 'Карта осадков',
        'coordinates': 'Координаты',
        'open_in_browser': 'Открыть в браузере',
        'close': 'Закрыть',
        'error': 'Ошибка',
        'location_error': 'Не удалось определить местоположение',
        'data_error': 'Не удалось получить данные',
        'search_error': 'Ошибка поиска',
        'uv_index': 'УФ индекс',
        'precipitation': 'Осадки',
        'days': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        'full_days': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'weather_conditions': {
            0: "Ясно",
            1: "Преимущественно ясно",
            2: "Переменная облачность",
            3: "Пасмурно",
            45: "Туман",
            48: "Туман с инеем",
            51: "Морось",
            53: "Морось",
            55: "Сильная морось",
            56: "Ледяной дождь",
            57: "Сильный ледяной дождь",
            61: "Небольшой дождь",
            63: "Умеренный дождь",
            65: "Сильный дождь",
            66: "Ледяной дождь",
            67: "Сильный ледяной дождь",
            71: "Небольшой снег",
            73: "Умеренный снег",
            75: "Сильный снег",
            77: "Снежные зерна",
            80: "Небольшие ливни",
            81: "Умеренные ливни",
            82: "Сильные ливни",
            85: "Небольшие снегопады",
            86: "Сильные снегопады",
            95: "Гроза",
            96: "Гроза с градом",
            99: "Сильная гроза с градом"
        }
    }
}

# KV language строка для интерфейса
KV = '''
<WeatherCard>:
    orientation: 'vertical'
    size_hint: None, None
    size: "320dp", "140dp"
    padding: "15dp"
    spacing: "8dp"
    pos_hint: {"center_x": 0.5}
    elevation: 4
    
    MDLabel:
        id: date_label
        text: "Сьогодні"
        halign: "center"
        font_style: "H6"
        theme_text_color: "Primary"
        
    MDBoxLayout:
        spacing: "15dp"
        size_hint_y: None
        height: "70dp"
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: "5dp"
            size_hint_x: 0.4
            
            MDLabel:
                id: temp_label
                text: "25°C"
                halign: "center"
                font_style: "H4"
                theme_text_color: "Primary"
                
            MDLabel:
                id: condition_label
                text: "Сонячно"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Secondary"
                
        MDBoxLayout:
            orientation: 'vertical'
            spacing: "5dp"
            size_hint_x: 0.6
            
            MDLabel:
                id: wind_label
                text: "Вітер: 5 м/с"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Secondary"
                
            MDLabel:
                id: humidity_label
                text: "Вологість: 60%"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Secondary"

<HourlyForecastItem>:
    orientation: 'vertical'
    size_hint: None, None
    size: "65dp", "100dp"
    padding: "5dp"
    spacing: "5dp"
    elevation: 2
    
    MDLabel:
        id: time_label
        text: "12:00"
        halign: "center"
        font_style: "Caption"
        theme_text_color: "Primary"
        
    MDLabel:
        id: hour_temp_label
        text: "24°C"
        halign: "center"
        font_style: "H6"
        theme_text_color: "Primary"
        
    MDLabel:
        id: hour_condition
        text: "Ясно"
        halign: "center"
        font_style: "Caption"
        theme_text_color: "Secondary"
        text_size: self.width, None

<DayForecastItem>:
    orientation: 'vertical'
    size_hint: None, None
    size: "300dp", "100dp"
    padding: "10dp"
    spacing: "5dp"
    elevation: 2
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: "10dp"
        
        MDLabel:
            id: day_name
            text: "Понеділок"
            font_style: "Body1"
            theme_text_color: "Primary"
            size_hint_x: 0.4
            
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: "5dp"
            size_hint_x: 0.3
            
            MDLabel:
                id: min_temp
                text: "15°"
                font_style: "Body2"
                theme_text_color: "Secondary"
                
            MDLabel:
                text: "/"
                font_style: "Body2"
                theme_text_color: "Secondary"
                
            MDLabel:
                id: max_temp
                text: "25°"
                font_style: "Body1"
                theme_text_color: "Primary"
                
        MDLabel:
            id: day_condition
            text: "Ясно"
            font_style: "Body2"
            size_hint_x: 0.3
            halign: "center"
            text_size: self.width, None

<DetailInfoItem>:
    orientation: 'vertical'
    size_hint: None, None
    size: "110dp", "100dp"
    padding: "10dp"
    spacing: "5dp"
    elevation: 2
    
    MDLabel:
        id: detail_title
        text: "Тиск"
        halign: "center"
        font_style: "Body2"
        theme_text_color: "Secondary"
        
    MDLabel:
        id: detail_value
        text: "1013 hPa"
        halign: "center"
        font_style: "H6"
        theme_text_color: "Primary"

<MenuItem>:
    IconLeftWidget:
        icon: root.icon

<MainScreen>:
    canvas.before:
        Color:
            rgba: app.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            title: "Погодний додаток"
            elevation: 4
            left_action_items: [["menu", lambda x: app.nav_drawer_open()]]
            right_action_items: [["refresh", lambda x: app.refresh_weather()], ["map-marker", lambda x: app.open_location_screen()]]
            md_bg_color: app.primary_color
        
        MDScrollView:
            id: scroll_view
            
            MDBoxLayout:
                id: main_box
                orientation: 'vertical'
                spacing: "20dp"  # Увеличили spacing между секциями
                padding: "20dp"  # Увеличили padding
                size_hint_y: None
                height: self.minimum_height
                
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        id: location_label
                        text: "Визначення місця..."
                        halign: "center"
                        font_style: "H5"
                        size_hint_y: None
                        height: "40dp"
                        theme_text_color: "Primary"
                        color: app.text_color
                        
                    WeatherCard:
                        id: current_weather
                        
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"  # Увеличили spacing под заголовком
                    size_hint_y: None
                    height: "180dp"  # Увеличили высоту контейнера
                    
                    MDLabel:
                        id: hourly_title
                        text: "Погодинний прогноз"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Primary"
                        color: app.text_color
                        size_hint_y: None
                        height: "30dp"
                        
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: "135dp"
                        
                        MDScrollView:
                            do_scroll_x: True
                            do_scroll_y: False
                            bar_width: "4dp"
                            
                            MDBoxLayout:
                                id: hourly_forecast
                                spacing: "10dp"
                                size_hint_x: None
                                width: self.minimum_width
                                size_hint_y: None
                                height: "125dp"
                                padding: "5dp"  # Добавили padding внутри контейнера
                            
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"  # Увеличили spacing под заголовком
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        id: details_title
                        text: "Деталі"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Primary"
                        color: app.text_color
                        size_hint_y: None
                        height: "30dp"
                        
                    MDGridLayout:
                        id: daily_details
                        cols: 3
                        spacing: "10dp"
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "10dp"
                        
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"  # Увеличили spacing под заголовком
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        id: forecast_title
                        text: "Прогноз на 7 днів"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Primary"
                        color: app.text_color
                        size_hint_y: None
                        height: "30dp"
                        
                    MDBoxLayout:
                        id: weekly_forecast
                        orientation: 'vertical'
                        spacing: "10dp"
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "10dp"  # Добавили padding для лучшего отображения

<LocationScreen>:
    canvas.before:
        Color:
            rgba: app.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: location_toolbar
            title: "Вибір міста"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.open_main_screen()]]
            md_bg_color: app.primary_color
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: "15dp"
            padding: "15dp"
            
            MDTextField:
                id: city_input
                hint_text: "Введіть назву міста"
                mode: "fill"
                size_hint_y: None
                height: "50dp"
                on_text_validate: app.search_city()
                hint_text_color: app.hint_color
                text_color: app.text_color
                
            MDRaisedButton:
                id: search_button
                text: "Пошук"
                on_press: app.animate_button_and_search()
                size_hint_x: 0.8
                height: "50dp"
                pos_hint: {"center_x": 0.5}
                
            MDRaisedButton:
                id: location_button
                text: "Використати моє місце"
                on_press: app.animate_button_and_location()
                size_hint_x: 0.8
                height: "50dp"
                pos_hint: {"center_x": 0.5}
                
            MDLabel:
                id: search_results
                text: ""
                halign: "center"
                font_style: "Body1"
                theme_text_color: "Secondary"
                color: app.text_color
'''

Builder.load_string(KV)

class WeatherCard(MDCard):
    pass

class HourlyForecastItem(MDCard):
    pass

class DayForecastItem(MDCard):
    pass

class DetailInfoItem(MDCard):
    pass

class MenuItem(OneLineIconListItem):
    def __init__(self, icon="", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon

class MainScreen(MDScreen):
    pass

class LocationScreen(MDScreen):
    pass

class WeatherApp(MDApp):
    background_color = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0, 0, 0, 1])
    hint_color = ListProperty([0.5, 0.5, 0.5, 1])
    primary_color = ListProperty([0.13, 0.59, 0.95, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.current_location = None
        self.current_data = None
        self.geocoded_locations = []
        self.nav_drawer = None
        self.language = 'uk'
        self.dark_theme = False
        self.units_metric = True
        
    def t(self, key):
        """Функция перевода"""
        if key in TRANSLATIONS[self.language]:
            return TRANSLATIONS[self.language][key]
        elif self.language != 'en' and key in TRANSLATIONS['en']:
            return TRANSLATIONS['en'][key]
        return key
    
    def get_weather_condition(self, code):
        """Получить описание погоды с учетом языка"""
        conditions = TRANSLATIONS[self.language]['weather_conditions']
        return conditions.get(code, self.t('weather_conditions').get(code, "Unknown"))
    
    def update_theme_colors(self):
        """Обновить цвета темы"""
        if self.dark_theme:
            self.background_color = [0.1, 0.1, 0.1, 1]
            self.text_color = [1, 1, 1, 1]
            self.hint_color = [0.7, 0.7, 0.7, 1]
            self.theme_cls.theme_style = "Dark"
        else:
            self.background_color = [1, 1, 1, 1]
            self.text_color = [0, 0, 0, 1]
            self.hint_color = [0.5, 0.5, 0.5, 1]
            self.theme_cls.theme_style = "Light"
    
    def animate_button(self, button=None):
        """Анимация нажатия кнопки"""
        if button:
            anim = Animation(opacity=0.7, duration=0.1) + Animation(opacity=1, duration=0.1)
            anim.start(button)
    
    def animate_button_and_search(self):
        """Анимация и поиск"""
        location_screen = self.screen_manager.get_screen('location')
        self.animate_button(location_screen.ids.search_button)
        Clock.schedule_once(lambda dt: self.search_city(), 0.1)
    
    def animate_button_and_location(self):
        """Анимация и использование местоположения"""
        location_screen = self.screen_manager.get_screen('location')
        self.animate_button(location_screen.ids.location_button)
        Clock.schedule_once(lambda dt: self.use_my_location(), 0.1)
    
    def update_ui_language(self):
        """Обновить все тексты на UI"""
        screen = self.screen_manager.get_screen('main')
        screen.ids.toolbar.title = self.t('app_title')
        screen.ids.hourly_title.text = self.t('hourly_forecast')
        screen.ids.details_title.text = self.t('details')
        screen.ids.forecast_title.text = self.t('weekly_forecast')
        
        location_screen = self.screen_manager.get_screen('location')
        location_screen.ids.location_toolbar.title = self.t('select_city')
        location_screen.ids.city_input.hint_text = self.t('enter_city')
        location_screen.ids.search_button.text = self.t('search')
        location_screen.ids.location_button.text = self.t('use_my_location')
        
        if self.current_data:
            self.update_current_weather()
            self.update_hourly_forecast()
            self.update_daily_details()
            self.update_weekly_forecast()
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "500"
        
        self.update_theme_colors()
        
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(LocationScreen(name='location'))
        
        self.create_navigation_drawer()
        
        Clock.schedule_once(lambda dt: self.get_current_location(), 1)
        
        return self.screen_manager
    
    def create_navigation_drawer(self):
        self.nav_drawer = MDNavigationDrawer()
        
        content = MDBoxLayout(orientation="vertical", spacing="8dp", padding="8dp")
        
        content.add_widget(MDLabel(
            text="Меню",
            font_style="H5",
            size_hint_y=None,
            height="40dp",
            theme_text_color="Primary"
        ))
        
        menu_list = MDList()
        
        menu_items = [
            (self.t('main'), "home", self.open_main_screen),
            (self.t('select_city'), "map-marker", self.open_location_screen),
            (self.t('settings'), "cog", self.open_settings),
            (self.t('support_developer'), "heart", self.support_developer),
            (self.t('about'), "information", self.open_about),
        ]
        
        for text, icon, callback in menu_items:
            item = OneLineIconListItem(text=text)
            item.add_widget(IconLeftWidget(icon=icon))
            item.bind(on_release=lambda x, cb=callback: (self.animate_button(x), cb(), Clock.schedule_once(lambda dt: self.nav_drawer.set_state("close"), 0.1)))
            menu_list.add_widget(item)
        
        content.add_widget(menu_list)
        
        self.nav_drawer.add_widget(content)
        self.screen_manager.get_screen('main').add_widget(self.nav_drawer)
    
    def nav_drawer_open(self):
        self.nav_drawer.set_state("open")
    
    def get_current_location(self):
        try:
            g = geocoder.ip('me')
            if g.ok:
                self.current_location = {
                    'city': g.city,
                    'country': g.country,
                    'lat': g.lat,
                    'lng': g.lng
                }
                self.update_location_label()
                self.fetch_weather_data()
            else:
                self.show_error(self.t('location_error'))
        except Exception as e:
            print(f"Ошибка получения локации: {e}")
            self.current_location = {
                'city': 'Київ' if self.language == 'uk' else 'Киев' if self.language == 'ru' else 'Kyiv',
                'country': 'Україна' if self.language == 'uk' else 'Украина' if self.language == 'ru' else 'Ukraine',
                'lat': 50.4501,
                'lng': 30.5234
            }
            self.update_location_label()
            self.fetch_weather_data()
    
    def update_location_label(self):
        if self.current_location:
            screen = self.screen_manager.get_screen('main')
            screen.ids.location_label.text = f"{self.current_location['city']}, {self.current_location['country']}"
    
    def fetch_weather_data(self):
        if not self.current_location:
            return
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': self.current_location['lat'],
                'longitude': self.current_location['lng'],
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                'hourly': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,weather_code,visibility,wind_speed_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,daylight_duration,sunshine_duration,precipitation_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max',
                'timezone': 'auto',
                'forecast_days': 7
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            self.current_data = response.json()
            
            self.update_current_weather()
            self.update_hourly_forecast()
            self.update_daily_details()
            self.update_weekly_forecast()
            
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            self.show_error(f"{self.t('data_error')}: {e}")
    
    def update_current_weather(self):
        if not self.current_data:
            return
        
        current = self.current_data.get('current', {})
        screen = self.screen_manager.get_screen('main')
        card = screen.ids.current_weather
        
        temp = current.get('temperature_2m', 0)
        if not self.units_metric:
            temp = temp * 9/5 + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        card.ids.temp_label.text = f"{int(temp)}{temp_unit}"
        
        weather_code = current.get('weather_code', 0)
        condition = self.get_weather_condition(weather_code)
        card.ids.condition_label.text = condition
        
        wind_speed = current.get('wind_speed_10m', 0)
        if not self.units_metric:
            wind_speed = wind_speed * 2.23694
            wind_unit = " mph"
        else:
            wind_unit = " м/с"
        card.ids.wind_label.text = f"{self.t('wind')}: {wind_speed:.1f}{wind_unit}"
        
        humidity = current.get('relative_humidity_2m', 0)
        card.ids.humidity_label.text = f"{self.t('humidity')}: {humidity}%"
        
        now = datetime.now()
        if self.language == 'en':
            date_format = f"{self.t('today')}, {now.strftime('%d %B %H:%M')}"
        elif self.language == 'uk':
            months_uk = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 
                        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']
            date_format = f"{self.t('today')}, {now.day} {months_uk[now.month-1]} {now.strftime('%H:%M')}"
        else:
            months_ru = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
            date_format = f"{self.t('today')}, {now.day} {months_ru[now.month-1]} {now.strftime('%H:%M')}"
        
        card.ids.date_label.text = date_format
    
    def update_hourly_forecast(self):
        if not self.current_data:
            return
        
        screen = self.screen_manager.get_screen('main')
        hourly_box = screen.ids.hourly_forecast
        hourly_box.clear_widgets()
        
        hourly_data = self.current_data.get('hourly', {})
        times = hourly_data.get('time', [])
        temps = hourly_data.get('temperature_2m', [])
        weather_codes = hourly_data.get('weather_code', [])
        
        # Получаем текущий час
        now = datetime.now()
        current_hour = now.hour
        
        # Определяем, с какого часа начинать показ (ближайшие 24 часа)
        start_index = 0
        for i, time_str in enumerate(times):
            try:
                dt = datetime.fromisoformat(time_str)
                if dt.hour >= current_hour:
                    start_index = i
                    break
            except:
                pass
        
        # Показываем прогноз на следующие 24 часа
        for i in range(start_index, min(start_index + 24, len(times))):
            time_str = times[i]
            try:
                dt = datetime.fromisoformat(time_str)
                # Форматируем время четко: ЧЧ:00
                time_display = dt.strftime("%H:00")
            except:
                time_display = time_str
            
            temp = temps[i] if i < len(temps) else 0
            if not self.units_metric:
                temp = temp * 9/5 + 32
                temp_unit = "°F"
            else:
                temp_unit = "°C"
            
            code = weather_codes[i] if i < len(weather_codes) else 0
            condition = self.get_weather_condition(code)
            
            item = HourlyForecastItem()
            item.ids.time_label.text = time_display
            item.ids.hour_temp_label.text = f"{int(temp)}{temp_unit}"
            item.ids.hour_condition.text = condition
            
            hourly_box.add_widget(item)
    
    def update_daily_details(self):
        if not self.current_data:
            return
        
        screen = self.screen_manager.get_screen('main')
        details_grid = screen.ids.daily_details
        details_grid.clear_widgets()
        
        current = self.current_data.get('current', {})
        daily_data = self.current_data.get('daily', {})
        
        sunrise = ""
        sunset = ""
        if daily_data.get('sunrise'):
            try:
                sunrise_time = datetime.fromisoformat(daily_data['sunrise'][0])
                sunrise = sunrise_time.strftime("%H:%M")
                sunset_time = datetime.fromisoformat(daily_data['sunset'][0])
                sunset = sunset_time.strftime("%H:%M")
            except:
                sunrise = "06:30"
                sunset = "20:45"
        
        uv_index = "3"
        
        pressure = current.get('pressure_msl', 0)
        feels_like = current.get('apparent_temperature', 0)
        if not self.units_metric:
            feels_like = feels_like * 9/5 + 32
            feels_unit = "°F"
        else:
            feels_unit = "°C"
        
        details = [
            (self.t('pressure'), f"{pressure:.0f} hPa"),
            (self.t('feels_like'), f"{feels_like:.0f}{feels_unit}"),
            (self.t('cloudiness'), f"{current.get('cloud_cover', 0)}%"),
            (self.t('sunrise'), sunrise),
            (self.t('sunset'), sunset),
            (self.t('visibility'), "10 km"),
            (self.t('precipitation'), "0 mm"),
            (self.t('uv_index'), uv_index),
            (self.t('wind'), f"{current.get('wind_speed_10m', 0):.1f} м/с")
        ]
        
        for title, value in details:
            item = DetailInfoItem()
            item.ids.detail_title.text = title
            item.ids.detail_value.text = value
            details_grid.add_widget(item)
    
    def update_weekly_forecast(self):
        if not self.current_data:
            return
        
        screen = self.screen_manager.get_screen('main')
        weekly_box = screen.ids.weekly_forecast
        weekly_box.clear_widgets()
        
        daily_data = self.current_data.get('daily', {})
        times = daily_data.get('time', [])
        max_temps = daily_data.get('temperature_2m_max', [])
        min_temps = daily_data.get('temperature_2m_min', [])
        weather_codes = daily_data.get('weather_code', [])
        
        full_days = self.t('full_days')
        
        for i in range(min(7, len(times))):
            date_str = times[i]
            try:
                dt = datetime.fromisoformat(date_str)
                day_num = dt.weekday()
                
                if i == 0:
                    day_name = self.t('today')
                elif i == 1:
                    day_name = self.t('tomorrow')
                else:
                    day_name = full_days[day_num]
                
            except:
                day_name = date_str
            
            max_temp = max_temps[i] if i < len(max_temps) else 0
            min_temp = min_temps[i] if i < len(min_temps) else 0
            if not self.units_metric:
                max_temp = max_temp * 9/5 + 32
                min_temp = min_temp * 9/5 + 32
                temp_unit = "°F"
            else:
                temp_unit = "°C"
            
            code = weather_codes[i] if i < len(weather_codes) else 0
            condition = self.get_weather_condition(code)
            
            item = DayForecastItem()
            item.ids.day_name.text = day_name
            item.ids.min_temp.text = f"{int(min_temp)}{temp_unit}"
            item.ids.max_temp.text = f"{int(max_temp)}{temp_unit}"
            item.ids.day_condition.text = condition
            
            weekly_box.add_widget(item)
    
    def search_city(self):
        city = self.screen_manager.get_screen('location').ids.city_input.text
        if not city:
            return
        
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': city,
                'format': 'json',
                'limit': 5
            }
            headers = {
                'User-Agent': 'WeatherApp/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers)
            results = response.json()
            
            if results:
                self.geocoded_locations = results
                locations_text = "\n".join([f"{r.get('display_name', '')}" for r in results[:3]])
                self.screen_manager.get_screen('location').ids.search_results.text = \
                    f"{self.t('found')}:\n{locations_text}"
                
                self.current_location = {
                    'city': results[0].get('name', city),
                    'country': results[0].get('display_name', '').split(',')[-1].strip(),
                    'lat': float(results[0]['lat']),
                    'lng': float(results[0]['lon'])
                }
                
                self.update_location_label()
                self.fetch_weather_data()
                self.open_main_screen()
            else:
                self.screen_manager.get_screen('location').ids.search_results.text = \
                    self.t('city_not_found')
                
        except Exception as e:
            print(f"Ошибка поиска города: {e}")
            self.show_error(f"{self.t('search_error')}: {e}")
    
    def use_my_location(self):
        self.get_current_location()
        self.open_main_screen()
    
    def refresh_weather(self):
        if self.current_location:
            self.fetch_weather_data()
    
    def open_main_screen(self):
        self.screen_manager.current = 'main'
    
    def open_location_screen(self):
        self.screen_manager.current = 'location'
    
    def open_settings(self):
        content = MDBoxLayout(orientation='vertical', spacing='15dp', padding='10dp', size_hint_y=None)
        content.height = '400dp'
        
        content.add_widget(MDLabel(
            text=self.t('language'),
            font_style='H6',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Primary'
        ))
        
        lang_box = MDBoxLayout(orientation='horizontal', spacing='10dp', size_hint_y=None, height='40dp')
        
        def set_language(lang):
            self.language = lang
            self.update_ui_language()
            self.create_navigation_drawer()
            settings_dialog.dismiss()
        
        def lang_button_press(btn, lang):
            self.animate_button(btn)
            Clock.schedule_once(lambda dt: set_language(lang), 0.1)
        
        en_btn = MDRaisedButton(
            text='English',
            on_press=lambda x: lang_button_press(x, 'en'),
            size_hint=(None, None),
            height='40dp',
            width='100dp'
        )
        
        uk_btn = MDRaisedButton(
            text='Українська',
            on_press=lambda x: lang_button_press(x, 'uk'),
            size_hint=(None, None),
            height='40dp',
            width='120dp'
        )
        
        ru_btn = MDRaisedButton(
            text='Русский',
            on_press=lambda x: lang_button_press(x, 'ru'),
            size_hint=(None, None),
            height='40dp',
            width='100dp'
        )
        
        lang_box.add_widget(en_btn)
        lang_box.add_widget(uk_btn)
        lang_box.add_widget(ru_btn)
        content.add_widget(lang_box)
        
        content.add_widget(MDLabel(
            text=self.t('theme'),
            font_style='H6',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Primary'
        ))
        
        theme_box = MDBoxLayout(orientation='horizontal', spacing='10dp', size_hint_y=None, height='40dp')
        
        def toggle_theme(checkbox, value):
            self.dark_theme = value
            self.update_theme_colors()
        
        theme_check = MDCheckbox(active=self.dark_theme)
        theme_check.bind(active=toggle_theme)
        theme_box.add_widget(theme_check)
        theme_box.add_widget(MDLabel(
            text=self.t('dark_theme'),
            font_style='Body1',
            theme_text_color='Primary'
        ))
        content.add_widget(theme_box)
        
        content.add_widget(MDLabel(
            text=self.t('units'),
            font_style='H6',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Primary'
        ))
        
        units_box = MDBoxLayout(orientation='horizontal', spacing='10dp', size_hint_y=None, height='40dp')
        
        def set_units(metric):
            self.units_metric = metric
            if self.current_data:
                self.update_current_weather()
                self.update_hourly_forecast()
                self.update_weekly_forecast()
        
        def units_button_press(btn, metric):
            self.animate_button(btn)
            Clock.schedule_once(lambda dt: set_units(metric), 0.1)
        
        metric_btn = MDRaisedButton(
            text=self.t('metric'),
            on_press=lambda x: units_button_press(x, True),
            size_hint=(None, None),
            height='40dp',
            width='140dp'
        )
        
        imperial_btn = MDRaisedButton(
            text=self.t('imperial'),
            on_press=lambda x: units_button_press(x, False),
            size_hint=(None, None),
            height='40dp',
            width='140dp'
        )
        
        units_box.add_widget(metric_btn)
        units_box.add_widget(imperial_btn)
        content.add_widget(units_box)
        
        support_btn = MDRaisedButton(
            text=self.t('support_developer'),
            on_press=lambda x: (self.animate_button(x), self.support_developer()),
            size_hint=(None, None),
            height='50dp',
            width='200dp'
        )
        
        content.add_widget(support_btn)
        
        settings_dialog = MDDialog(
            title=self.t('settings'),
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(
                    text=self.t('close'),
                    on_press=lambda x: settings_dialog.dismiss()
                )
            ]
        )
        settings_dialog.open()
    
    def support_developer(self):
        try:
            webbrowser.open('https://ko-fi.com/ferki')
        except:
            dialog = MDDialog(
                title=self.t('support_developer'),
                text="https://ko-fi.com/ferki",
                size_hint=(0.8, 0.4),
                buttons=[
                    MDFlatButton(
                        text=self.t('close'),
                        on_press=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
    
    def open_about(self):
        dialog = MDDialog(
            title=self.t('about'),
            text=f"{self.t('app_title')} v1.0\n\n{self.t('language')}: {self.language.upper()}\n\nИспользует:\n• Open-Meteo API\n• Nominatim для геокодирования\n\n© 2024",
            size_hint=(0.8, 0.4),
            buttons=[
                MDFlatButton(
                    text=self.t('close'),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_error(self, message):
        dialog = MDDialog(
            title=self.t('error'),
            text=message,
            size_hint=(0.8, 0.4),
            buttons=[
                MDFlatButton(
                    text=self.t('close'),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

if __name__ == '__main__':
    WeatherApp().run()