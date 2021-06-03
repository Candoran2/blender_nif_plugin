Armatures
=========
.. _armature-armatures:

Armature Bones
==============

* The following section deals with Armatures. Note that, in order for any animations to display in Blender like they
  would in-game, ``Preserve Volume`` must be turned off in the Armature modifier.

.. _armature-flags:

Bone Flags
----------

* These are set upon export if left at ``0``.
* Only change the value in very specific cases: 
 * Oblivion Clothing uses ``0x000F``

.. Otherwise no idea what they do, more research needed.

.. _armature-invmarker:

Inventory Marker
----------------

* This is a special type of bone which is used to position an object in the inventory display.
* It may also be used for animation placement involving multiple NPCs
* The InvMarker bone should only be used in engines that can support them.

**Example:**
 
#. Create this item in the same manner as you would for a standard armature bone.
#. Parent must be Armature root.
#. Naming must start with InvMarker and can only be appended with ``.000``

   A model with 4 inventory marker bone items should be named as ``InvMarker``, ``InvMarker.001``, ``InvMarker.002``,
   ``InvMarker.003``

**Notes:**

* Games known to support this include: 
	- The Elder Scrolls - Skyrim.

.. warning::
		Exporting this type of bone into engines that do not support it will cause
		crashes!