# Changelog

## [1.06] - 2022-06-14
- Modify installer and readme
- Make the application use main branch when checking for updates

## [1.05] - 2022-06-08
- Add installer
- Add new version notification

## [1.04] - 2022-06-08
- Add support for Epic's Game Launcher
- Disable startup message box
- Prevent user from saving if Steam is running
- Improve GUI layout, split games by launcher
- Improve CLI experience, remove unnecessary logs
- Added progress information when downloading images

## [1.03] - 2022-06-07
- Improve shortcut loading and saving compatibility

## [1.02] - 2022-06-07
- Update window title
- Try running in GUI mode by default
- Disable terminal when running via SteamJar.desktop file
- Many small improvements in CLI
- Refactor how we store shortcuts to improve compatibility

## [1.01] - 2022-06-06
- Make shortcuts class case insensitive when reading steam shortcuts

## [1.0] - 2022-06-06
- Blazing fast searching for games. It is almost immediate now.
- Huge refactor in preparation for searching for games outside Bottles
- Better interface
- Tested working on Manjaro with Steam installed in different locations

## [0.3] - 2022-05-31
- Much faster registry parsing, resulting in fast game finding and generating shortcuts

## [0.2] - 2022-05-31
- Importing game list from [GOG Galaxy](https://www.gog.com/galaxy)
- Hide terminal when starting via SteamBottles.desktop
- Add ability to download missing images from GUI
- Cleanup the code (very)slightly
- Add this changelog

# [0.1] - 2022-05-30
- Graphical user interface with Gtk
- Downloading missing images from [SteamGridDB](https://steamgriddb.com)
- Importing game list from [Ubisoft Connect](https://ubisoftconnect.com/en-US/)
- Loading and saving Steam shortcuts by parsing shortcuts.vdf
