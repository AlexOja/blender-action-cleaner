# blender-action-cleaner
A simple tool to delete multiple animation actions with checkboxes. While blender handles it poorly, you can delete action only by unlinking it from everything, restarting the project and hoping that it will be gone, with this tool you can delete all the actions you want in a simple click of a button.

# Features
- Delete multiple animation actions at once
- Visual confirmation dialog showing all selected actions
- Select/Deselect/Invert selection options
- Clear warnings when actions are in use
- Fixed panel in the Dope Sheet sidebar
  
# Installation
1. Download the latest release ZIP file
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install from files" and select the ZIP file
4. Enable the add-on

# Usage
1. Open the Animation tab

![tutor1](https://github.com/user-attachments/assets/2a5f50ca-354f-4ac3-8c05-bd16ab47fdc6)

2. Open the Dope Sheet editor

![tutor2](https://github.com/user-attachments/assets/35f43b84-ea65-45ad-935d-4efdaaec04fa)

3. Press N to open the sidebar if not visible

![tutor3](https://github.com/user-attachments/assets/56cb1981-8f59-4b47-9baf-2b5d3bcd09d4)

4. In the Tool tab:
- Check the boxes for actions you want to delete
- Click the Delete button
- Confirm the deletion in the popup dialog

![tutor4](https://github.com/user-attachments/assets/90052ace-2630-4177-be97-4c035b3031c8)

# Requirements
Blender 4.4, not tested on older versions

# WARNING
Deleting actions cannot be undone! Use with caution.
