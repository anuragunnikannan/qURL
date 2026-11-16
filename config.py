import platform

config = {}

if platform.system() == "Windows":
    config = {
        "fixed_width_font": "Cascadia Code"
    }
elif platform.system() == "Linux":
    config = {
        "fixed_width_font": "monospace"
    }