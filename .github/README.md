<p align="center">
  <img width="500" alt="GUI preview screenshot" src="./preview_gui.png">
</p>

# What is SteamJar
SteamJar is a tool that helps you add all of your non-steam games to Steam.  
It will search for games from all supported game launchers from all known sources (Bottles, Wineprefixes) and add them as a non-steam applications.
Additionally - when missing pictures are detected, this tool will download them from SteamGridDB if you wish.
  
**[See Changelog](./CHANGELOG.md)**  
  
**Important!**  
Tested only on Steam Deck. I made sure that I use generic paths and methods to obtain things - it should work on other systems. But this is not tested! If you encounter problems, please open an Issue 👍 
  
# Installation
- Go to the Desktop mode
- Download this repository: [Download](https://github.com/pbaja/SteamJar/archive/refs/heads/main.zip)
- Unzip it and run by clicking on the `SteamJar.desktop` file

Note: Make sure that you have [Bottles](https://usebottles.com/) in (**flatpak version**).

# Usage
- *Optionally* Press `Refresh games` button to search for games
- Enable or disable shortcuts. Disabled shortcuts will be removed.  
You can enable all by clicking on the `Enable all` button
- *Optionally* Click on the `Download images` button to download missing grid images
- Exit Steam if you haven't already
- Click on the `Save changes` to save enabled shortcuts to Steam 

## Roadmap
Things to do, sorted by priority.  
  
- [x] Adding games from GOG Galaxy
- [x] Graphical user interface
- [x] Downloading missing grid images
- [x] Improve registry access performance
- [ ] Add simpler installation method
- [x] Adding games from Ubisoft Connect
- [ ] Adding games from Epic Launcher
- [ ] Adding games from Origin
- [ ] Code cleanup and documentation (types)
- [ ] Ability to edit shortcuts
- [ ] Ability to change images when editing
- [ ] Tests
- [ ] Juicify GUI - icons, tooltips, padding
- [ ] Adding standalone games
- [ ] Backing up your shortcuts, multiple sets?

### Extra
There is also a command line interface: `python run.py`. You can use it remotely via ssh.  
To run GUI version from terminal add `--gui` flag.  
  
<img width="300" alt="GUI preview screenshot" src="./preview_cli.png">