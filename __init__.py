import bpy

bl_info = {
    "name": "Action Cleaner Pro",
    "author": "Aleksei Oja",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "Dope Sheet > Tool Panel",
    "description": "Advanced action management with confirmation dialog",
    "warning": "Deleted actions cannot be restored",
    "doc_url": "https://github.com/AlexOja/blender-action-cleaner",
    "category": "Animation",
}

class DeleteActionsOperator(bpy.types.Operator):
    bl_idname = "anim.delete_actions_operator"
    bl_label = "Delete Selected Actions"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return any(a.select for a in bpy.data.actions)

    def invoke(self, context, event):
        self.selected_actions = [a for a in bpy.data.actions if a.select]
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.label(text="You are about to delete:", icon='ERROR')
        box = col.box()
        
        for action in self.selected_actions:
            row = box.row()
            row.label(text=f"• {action.name}")

        col.separator()
        col.label(text="This action cannot be undone!", icon='CANCEL')

    def execute(self, context):
        for action in self.selected_actions:
            # Unlink from objects
            for obj in bpy.data.objects:
                if obj.animation_data and obj.animation_data.action == action:
                    obj.animation_data.action = None
            # Delete action
            bpy.data.actions.remove(action)
        
        self.report({'INFO'}, f"Deleted {len(self.selected_actions)} actions")
        return {'FINISHED'}

class ACTION_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Action Cleaner Pro"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"
    
    def draw(self, context):
        layout = self.layout
        
        # Header with selection controls
        row = layout.row()
        row.operator("anim.select_all_actions", text="All").action = 'SELECT'
        row.operator("anim.select_all_actions", text="None").action = 'DESELECT'
        row.operator("anim.select_all_actions", text="Invert").action = 'INVERT'
        
        # Scrollable action list
        layout.template_list(
            "ACTION_UL_List", 
            "", 
            bpy.data, 
            "actions", 
            context.scene, 
            "action_list_index"
        )
        
        # Fixed footer with delete button
        selected_count = sum(1 for a in bpy.data.actions if a.select)
        if selected_count > 0:
            col = layout.column(align=True)
            col.alert = True  # Red color for warning
            col.operator("anim.delete_actions_operator", 
                        text=f"Delete ({selected_count})", 
                        icon='TRASH')
            col.alert = False

class SelectAllActionsOperator(bpy.types.Operator):
    bl_idname = "anim.select_all_actions"
    bl_label = "Select/Deselect All Actions"
    action: bpy.props.EnumProperty(
        items=[
            ('SELECT', 'Select All', ''),
            ('DESELECT', 'Deselect All', ''),
            ('INVERT', 'Invert Selection', '')
        ]
    )
    
    def execute(self, context):
        if self.action == 'INVERT':
            for action in bpy.data.actions:
                action.select = not action.select
        else:
            for action in bpy.data.actions:
                action.select = (self.action == 'SELECT')
        return {'FINISHED'}

class ACTION_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.prop(item, "select", text="")
        
        # Show action name with icon
        row.label(text=item.name, icon='ACTION')
        
        # Show warning if action is used
        if any(obj.animation_data and obj.animation_data.action == item 
               for obj in bpy.data.objects):
            row.label(text="", icon='OBJECT_DATA')

def register():
    # Add selection property to actions
    bpy.types.Action.select = bpy.props.BoolProperty(
        default=False,
        description="Mark action for deletion"
    )
    
    # Register classes
    classes = (
        DeleteActionsOperator,
        ACTION_PT_CustomPanel,
        SelectAllActionsOperator,
        ACTION_UL_List,
    )
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # For list functionality
    bpy.types.Scene.action_list_index = bpy.props.IntProperty()

def unregister():
    # Unregister everything
    classes = (
        DeleteActionsOperator,
        ACTION_PT_CustomPanel,
        SelectAllActionsOperator,
        ACTION_UL_List,
    )
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove properties
    del bpy.types.Action.select
    del bpy.types.Scene.action_list_index

if __name__ == "__main__":
    register()