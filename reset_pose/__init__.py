#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

import bpy

# Version History
# 1.0.0 - 2020-06-27: Original version
# 1.0.1 - 2020-07-02: Made it compatible with Weight Paint mode.
# 1.0.2 - 2020-12-20: Fixed a bug where get_rig_name() was pulling from the DATA name, not the actual name of the OBJECT.
# 1.0.3 - 2022-08-07: Misc formatting cleanup before uploading to GitHub.

bl_info = {
    "name": "Reset Pose",
    "author": "Jeff Boller",
    "version": (1, 0, 3),
    "blender": (2, 93, 0),
    "location": "",
    "description": "This Blender add-on resets the pose for the currently-selected rig." \
                   "To run this, make a Blender keyboard shortcut and this for the action: wm.reset_pose "\
                   "If you want to call this manually from Python, use this command: bpy.ops.wm.reset_pose()",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

def get_rig_name():
    if bpy.context.mode == 'PAINT_WEIGHT':
        # We need to iterate through the selected objects and find the one that's an armature.
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                for modifier in obj.modifiers:
                    if modifier.type == 'ARMATURE':
                        return modifier.object.name
    return bpy.context.object.name  # This is what you need in Pose Mode. We know what object we need to look at, since it's selected.

class WM_OT_reset_pose(bpy.types.Operator):
    bl_idname = 'wm.reset_pose'
    bl_label = 'Reset Pose'
    bl_description = 'Call bpy.ops.wm.reset_pose()'
    bl_options = {'UNDO'}

    def execute(self, context):
        rig_name = get_rig_name()
        if bpy.context.mode != 'PAINT_WEIGHT':
            try:
                bpy.ops.object.mode_set(mode='POSE')

            except:
                self.report({'ERROR'}, '  ERROR: Cannot switch to Pose Mode. Is an armature selected?')
                return {'FINISHED'}

        bpy.data.objects[rig_name].data.pose_position = 'REST' # Go to Rest Position
        bpy.ops.pose.armature_apply(selected=False) # Go to Pose -> Apply Pose as Rest Pose
        bpy.data.objects[rig_name].data.pose_position = 'POSE' # Switch back to Pose Position
        return {'FINISHED'}

def register():
    bpy.utils.register_class(WM_OT_reset_pose)

def unregister():
    bpy.utils.unregister_class(WM_OT_reset_pose)

if __name__ == "__main__":
    register()
