# PyCO2Sys-GUI
A simple, straight-forward GUI for the python program CO2Sys, used for the estimation of carbonate system parameters in climate and ocean sciences.

Included in the GUI are instructions for use and are repeated as follows:
    1. Initialize the program
    2. Select TWO parameters for which you have known values, then click "Next"
    3. Input the measured values for the parameters, the initial fluid conditions, and all associated errors
    4. Once fully and correctly inputted, click "Next" or if you need to change your parameters, click "Back" and repeat Step 2
    5. Select your desired constant sets from each dropdown for H2CO3, HSO4-, Total Borate, and HF
    6. Once all constant sets are selected, click "Get Results" to get results or click "Back" to edit input values
    7. Results are presented in the form "Parameter Name: Parameter Value ± Error Value"
    8. Results are cleared and replaced anytime the "Get Results" button is pressed but can be manually cleared using the "Clear Results" button
    9. Inputs are locked for editing once the "Next" buttons are pressed and "Back" buttons must be pressed to edit earlier inputs/selections
    10. Enjoy! 

To create a .EXE version of the GUI, navigate to the folder containing the file PyCO2Sys_App.py and paste the following in Command Prompt:
    python -m PyInstaller --onefile PyCO2Sys_app.py

