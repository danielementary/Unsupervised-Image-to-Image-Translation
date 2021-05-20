# Command generator
This script can be used as follows to easily generate commands, i.e. running multiple times similar commands to run a trained FUNIT model.

## How to use
1. Open `command_generator.py`
2. Set and save:
	- `path_to_config`
	- `path_to_model`
	- `model_iteration`
	- `inputs`
	- `outputs`
3. Run `python command_generator.py`
4. Make the generated file executable `chmod +x translations_to_do`
5. Run all the commands `./translations_to_do` at the root of the FUNIT code and wait...
6. The generated images can be found in the folder `trained/*model iteration*`

## Warning
Make sure all the folders the script will be set to write to exist.
