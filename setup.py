from setuptools import setup, find_packages

setup(
    name="qURL",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["app", "ui", "service"],
    entry_points={
        "console_scripts": [
            "qURL=app:create_app",
        ],
    },
    include_package_data=True,
    package_data={
        "components": ["*.qss"]
    }
)
