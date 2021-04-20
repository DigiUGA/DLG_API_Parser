"""
GUI that gets the required script arguments (path to input CSV, place to save output CSV, name for output CSV)
and then runs the script to create the CSV so users don't need to interact with the command line.

Probably will actually include it in the dlg_json2csv.py document itself, but experimenting with it separately.
"""
# TODO: need fields for optional encode and mapping

import os
import PySimpleGUI as sg
import subprocess


"""Makes and displays a window for users to provide the input and output csv."""

sg.theme("DarkTeal6")

layout = [[sg.Text('Path to CSV with DLG URLs'), sg.Input(key="input_csv"), sg.FileBrowse()],
          [sg.Text('Folder to save output'), sg.Input(key="output_location"), sg.FolderBrowse()],
          [sg.Text('Name for the output CSV'), sg.Input(key="output_name")],
          [sg.Text()],
          [sg.Text("Optional information. Only enter if not using the default value.")],
          [sg.Text("Mapping, if not DLG_Mapping.csv"), sg.Input(key="map"), sg.FileBrowse()],
          [sg.Submit(key="submit"), sg.Cancel()]]

window = sg.Window("Make an Omeka CSV from DLG JSON", layout)

while True:
    event, values = window.read()
    if event == "submit":
        output_csv = os.path.join(values["output_location"], values["output_name"])
        # Error testing
        # TODO: error check if output csv already exists, do you want to override
        if values["input_csv"] == "":
            sg.Popup("CSV can't be blank")
        elif values["output_name"] == "":
            sg.Popup("Output name can't be blank")
        # Run script
        else:
            if os.path.exists(output_csv):
                override = sg.PopupYesNo("Do you want to replace existing csv?")
                # GUI remains open for data input if override is no.
                # Could do something fancy to change color of boxes with errors OR clear values if errors by updating layout.
                if override == "Yes":
                    script_command = f'python dlg_json2csv.py --input "{values["input_csv"]}" --output "{output_csv}"'
                    if not values["map"] == "":
                        script_command += f' --mapping {values["map"]}'
                    subprocess.run(script_command, shell=True)
            else:
                script_command = f'python dlg_json2csv.py --input "{values["input_csv"]}" --output "{output_csv}"'
                if not values["map"] == "":
                    script_command += f' --mapping {values["map"]}'
                subprocess.run(script_command, shell=True)
    # User closes the GUI
    if event in ("Cancel", None):
        exit()

# Not sure if we need this. Right now user closes GUI.
# Put in code where want it to auto-close, if we do, or PSG recommends.
# window.close()



# # Gets the script argument values from the user, validates the values, and reformats the information.
# # Continues giving the user the GUI and processing the input until all values are valid.
# # TODO: check all the values before giving the GUI again?
# # TODO: merge this error checking better with argparse in dlg_json2csv.py or replace it.
# message = ""
# while True:
#
#     # Displays a GUI to the user and gets input.
#     status, arguments = display_gui(message)
#
#     # If the user clicked cancel or the X on the GUI, ends the script.
#     if status in ("Cancel", None):
#         exit()
#
#     # If the provided value for the URLs CSV is empty or is not a valid path, displays the GUI again.
#     input_csv = arguments["input_csv"]
#     if input_csv == "":
#         message = "Please try again. The path to the CSV with the DLG URLs cannot be blank."
#         continue
#     elif not os.path.exists(input_csv):
#         message = "Please try again. The path to the CSV with the DLG URLs was not a valid path."
#         continue
#
#     # If the provided value for the output folder is empty or is not a valid path, displays the GUI again.
#     output_location = arguments["output_location"]
#     if output_location == "":
#         message = "Please try again. The folder to save the output to cannot be blank."
#         continue
#     elif not os.path.exists(output_location):
#         message = "Please try again. The folder to save the output to was not a valid path."
#         continue
#
#     # If the provided value for the output CSV name is empty, displays the GUI again.
#     output_file = arguments["output_name"]
#     if output_file == "":
#         message = "Please try again. The name for the output CSV cannot be blank."
#         continue
#
#     # Adds file extension to the end of the provided file name if it is not already present.
#     if not output_file.endswith(".csv"):
#         output_file = output_file + ".csv"
#
#     # Creates the path for the script output CSV using the provided values for the output location and file name.
#     output_csv = os.path.join(output_location, output_file)
#
#     # If the provided value for the mapping file (which is option) is not a valid path, displays the GUI again.
#     if not arguments["map"] == "" and not os.path.exists(arguments["map"]):
#         message = "Please try again. The path to the mapping CSV was not a valid path."
#         continue
#
#     # If all values are valid, quits the loop.
#     break

# # Runs the dlg_json2csv.py script with the user-provided information as the arguments.
# # Builds the script command by starting with the required values and then adding the optional value if provided.
# script_command = f'python dlg_json2csv.py --input "{input_csv}" --output "{output_csv}"'
# if not arguments["map"] == "":
#     script_command += f' --mapping {arguments["map"]}'
# subprocess.run(script_command, shell=True)
