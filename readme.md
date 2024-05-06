# TJA Randomizer

generate random TJA files for Taiko no Tatsujin with provided random seed. For PRACTISE ONLY, NOT FOR commercial use.

## Build
```powershell
pip install -r requirements.txt
pyinstaller --onefile --icon=icon.ico tja_randomizer.py
```
release file in `dist` folder.

## Usage
```powershell
dist\tja_randomizer.exe --seed [seed] --random-level 0 test\test.tja
```
A file named `test_crazy_seed_[seed].tja` will be generated in the same folder.
For more detail, use
```commandline
dist\tja_randomizer.exe --help
```
