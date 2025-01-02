# radioCenter

* Author: Ruslan Dolovaniuk (Ukraine)
* PayPal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B3VG4L8B7CV3Y&source=url

this addon allows you to play online radio stations and save audio stream to file.
Recording one radio station does not interfere with listening to another radio station.

In addition to Internet catalogs, it is also possible to add a local catalog with m3u files to collections.
To get a local collection, you must specify the base path to the catalog in the settings.
All m3u files in this catalog and all its subdirectories will be checked automatically.

Warnings!
Checking radio stations from collections is a rather lengthy and resource-intensive process.
It is recommended to perform it in parts, periodically closing the window, and rerun it later.
After reopening the collections window, testing will continue until all radio stations have been checked.
Also, the health status of links often changes, so it is recommended to check the health of the link at the moment before adding it to the general list.


## List of hotkeys:
* NVDA+ALT+P: play/pause radio;
* NVDA+ALT+P double click: turn off the radio;
* NVDA+ALT+SHIFT+R: Enable/disable recording;
* NVDA+ALT+M: enable/disable muting;
* NVDA+ALT+UpArrow: volume up;
* NVDA+ALT+DownArrow: volume down;
* NVDA+ALT+RightArrow: station next;
* NVDA+ALT+LeftArrow: station previous;
* NVDA+ALT+O: get station info;
* NVDA+ALT+R: open window control center;
* ESC: close Control Center and Collections windows;
* CTRL+C: copy the link to the radio station to the clipboard;

When manually sorting in the list of stations:
* ALT+Up Arrow: move the station to a higher position;
* ALT+Down arrow: move the station to a lower position;

In the lists of collections:
* ALT+Up Arrow or ALT+Right Arrow: switch the link to the next one (if the radio station has several links to the audio stream);
* ALT+Down Arrow or ALT+Left Arrow: switch the link to the previous one (if the radio station has several links to the audio stream);
* CTRL+C: copy the link to the radio station to the clipboard;

## Sorting stations:
* without sorting;
* by name in forward direction;
* by name in the reverse direction;
* by priority and name in the forward direction;
* by priority and name in the reverse direction;
* manually;

## List of changes:
### Version 4.5.0
* added context menu on the list of radio stations in the main window;
* added a keyboard shortcut for recording a radio station;
* fixed the availability of recording without having to start playing the radio station;
* fixed the change of labels on buttons in the main window;
* fixed the change of labels of elements in the nvda service menu;
* synchronized change of labels on buttons in the main window, nvda service menu elements, context menu elements, when pressing key combinations;
* added Arabic translation (وفيق طاهر);

### Version 4.2.1
* added extraction of station name, if any, when processing m3u file;
* the option to show a link to a station has been added to the settings;
* the option to show the number of stations in a portion to check has been added to the settings;
* some errors in automatic station checking have been fixed;

### Version 4.0.0
* for nvda 2023 made collections compatible, except for one Radio Browser;
* created a collection for checking m3u files on local storage;
* added a control menu to the nvda menu;
* moved filters to a separate dialog box;
* added sound playback when manually checking a station in collections;
* fixed a floating error when checking a station after applying filters;

### Version 3.6.0
* made changes for compatibility with nvda 2023 (collections are disabled for 2023 version);
* added support for m3u links;
* added ignoring the case of letters when filtering by name and/or information;
* added cleaning of spaces at the beginning and end of the radio station name when parsing in collections;
* added pronunciation of the station status when manually checking by the test button in collections;
* fixed a floating error when updating collections;

### Version 3.2.0
* added support for .pls links;
* added a name from the audio stream information when saving the recorded file;
* added error handling when recording cannot be started;

### Version 3.0.0
* created a collection mechanism for selecting radio stations from catalogs;
* added 3 collections with radio stations;
* made a mechanism for automatically checking each radio station in the collections for functionality;
* added a manual check of the radio station for functionality;
* added playback of the radio station directly in the list of collections;
* added saving radio stations from the collection to the general list;
* added filtering in collections by status;
* added filtering in collections by text in the title;
* added filtering in collections by text in additional information;
* added closing dialog boxes by pressing ESC;
* added copying the link to the radio station to the clipboard in the main list and in collection lists;
* improved switching stations using hot keys, as previously it did not always switch;

### Version 2.1.0
* added checking and correction if errors are found in the indexing of stations;
* added Spanish localization (Rémy Ruiz);
* added French localization (Rémy Ruiz);

### Version 2.0.0
* added the ability to record an audio stream to a file;

### Version 1.5.3
* added Czech localization (Jiri Holz);

### Version 1.5.1
* added a link functionality check before adding a new radio station;
* added a link functionality check before changing the radio station link;
* fixed a number of minor errors in operation;

### Version 1.4.2
* added manual sorting of stations;
* added a key combination for mute mode;

### Version 1.2.5
* added settings to the nvda settings panel;
* added the ability to edit an existing radio station;
* added several options for sorting radio stations;
* changed the muting function;
* fixed the problem of opening several control windows;

### Version 1.1.1
* added Turkish localization (Umut Korkmaz);

### Version 1.1.0
* added GUI control center;

### Version 1.0.0
* created online radio on base vlc player;
