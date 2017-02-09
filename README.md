# Description

Action handler to save every pomodoro event from gnome-pomodoro. This requires the "Custom Actions" plugin to be enabled in gnome-pomodoro.

# Usage

1. Install (setup.py install)
2. Configure a custom action in gnome-pomodoro with this command line

    `pomodoro_tracker $(state) $(duration) $(elapsed) $(triggers)`

3. `pomodoro_db summary` gives you a basic summary
4. `pomodoro_db dump` dumps the db to a csv formatted output
