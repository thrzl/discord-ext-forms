import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
        name='discord-ext-forms', 
        version='3.0.3',
        packages=["discord.ext.forms"], 
        author='terabyte3', 
        author_email='terabyte@terabyteis.me', 
        license='MIT',
        description='Easy forms and surveys for discord.py.', 
        long_description=long_description, 
        long_description_content_type='text/markdown', 
        url='https://github.com/terabyte3/discord-ext-forms', 
#        packages=setuptools.find_packages(), 
        classifiers=[
            'Programming Language :: Python :: 3.7', 
            'Programming Language :: Python :: 3.8', 
            'Programming Language :: Python :: 3.9', 
            'License :: OSI Approved :: MIT License', 
            'Operating System :: OS Independent', 
            'Topic :: Communications :: Chat', 
            'Intended Audience :: Developers', 
        ], 
        python_requires='>=3.7', install_requires=['discord.py>=1.5', 'emoji']
)
