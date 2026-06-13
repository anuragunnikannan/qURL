from setuptools import setup, find_packages

setup(
    name="qURL",
    version="1.0.0",
    # find_packages() will look for directories with __init__.py
    # and include components/ and utils/ automatically
    packages=find_packages(),
    # Since app.py, ui.py, etc., are in the root, we list them as modules
    py_modules=["app", "ui", "service"],
    entry_points={
        "console_scripts": [
            # This creates the 'qurl' command which runs the start()
            # function inside your app.py
            "qURL=app:create_app",
        ],
    },
    # This ensures image.png and other non-python files are included
    include_package_data=True,
)
