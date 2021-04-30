from setuptools import setup, find_packages


setup(
        name='flask_crm', # module's name
        version='1.0',
        py_modules=['app'], # the file that needs to be installed
        install_requirs=[
                'flask',
                'jwt'],
        entry_points='''
                [console_scripts]
                app=app:app
        '''
)
