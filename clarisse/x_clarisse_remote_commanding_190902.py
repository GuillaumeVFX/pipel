#
# status: Working :)
import sys
import clarisse_net as ix

rclarisse = ix.ClarisseNet('gaf',55000)

# rclarisse.connect('',55000)

rclarisse.run('print "REMOTE Hello World!"')


rclarisse.run('print "This is great I can send stuff to my clarisse :) wow that is too much"')

#  @a Creating a Sphere
rclarisse.run('ix.cmds.CreateObject("polysphere_created_remotely", "GeometryPolysphere")')
ix.cmds.DisableItems(["project://scene/polysphere_created_remotely"], True)
