
<img src="images/pluginIcon_grey.svg" height="23">&ensp;Helsing
===============================================================

[![Downloads](https://img.shields.io/jetbrains/plugin/d/12553-helsing)](https://plugins.jetbrains.com/plugin/12553-helsing)

This is a dark color theme for JetBrains products for working under the sunlight.
It is designed to be visible even in enormously bright environment.

<img src="images/screenshot.png" width="400">

Installation
------------

Open __Settings__ of your IDE and install the plugin from __Plugins__ dialog.
Or install it from here https://plugins.jetbrains.com/plugin/12553-helsing.

Tips for working on plain air
-----------------------------

1. Wear dark.
   Your screen will reflect your bright clothes.
   Even a matte display won't help if the sun will be shining on your white T-shirt.
2. Try to find a shadow.
   But try to not use trees.
   A lot of trees produce tiny drops of a resin.
   They are hard to clean from your screen.
3. Set the brightness level to the maximum.
4. Have a cleaning cloth with you. A dust is very distracting in the sun.
5. Try [garlic](https://github.com/igrmk/garlic) theme
   for GNOME Terminal and [kitty](https://sw.kovidgoyal.net/kitty/).
   Also try [hull](https://github.com/igrmk/kull-vim) theme for Vim.

Build
-----

The page at https://plugins.jetbrains.com/docs/intellij/setting-up-theme-environment.html
describes how to set up an environment for theme development.
Here are some additional details to address potential questions:

1. When adding the JDK as described in the page above, use JetBrains Runtime 17.
2. As a JetBrains Toolbox user on macOS, my correct path to the IntelliJ Platform Plugin SDK
   is `/Users/igrmk/Applications/IntelliJ IDEA Community Edition.app/Contents`.
   The SDK should be added to the project, not the module.
   You can do this via **File | Project Structure | Project Settings | Project | SDK**.
   The module SDK is set to the Project SDK by default and should remain unchanged.

To build the plugin, select **Build | Prepare Plugin Module 'Helsing' For Deployment**.
After doing so, locate the **Helsing.jar** file in the project directory. This is the file to publish.

Some helpful tables
-------------------

Here are the possible values for the `FONT_TYPE` attribute:

| Value | Interpretation |
|-------|----------------|
| 0     | Normal         |
| 1     | Bold           |
| 2     | Italics        |
| 3     | Bold italics   |

Here are the possible values for the `EFFECT_TYPE` attribute:

| Value | Interpretation   |
|-------|------------------|
| 0     | No effects       |
| 1     | Underscored      |
| 2     | Underwaved       |
| 3     | Strikeout        |
| 4     | Bold underscored |
| 5     | Dotted line      |

You can likely find an up-to-date description of theme attributes at this link:
[IntelliJPlatform.themeMetadata.json](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-resources/src/themes/metadata/IntelliJPlatform.themeMetadata.json).

Thanks to
---------

[![JetBrains](images/jetbrains.svg)](https://www.jetbrains.com/?from=helsing)
