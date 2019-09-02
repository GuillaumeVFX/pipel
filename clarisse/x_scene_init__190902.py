#
# @status: In progress
#
# @status: Working :)
import clarisse_net as ix


# REMOTE HOST VARIABLE TO SETUP
# @action Setup Host name|ip
hostAddr = '192.168.0.169'
# @action Setup Host port
hostPort = 55000

helloMsg = '"Hello World!"'

#rclarisse = ix.ClarisseNet()

# @a Connecting to the Host
rclarisse = ix.ClarisseNet(hostAddr,hostPort)


#  @a Printing a message
rclarisse.run('print '+ helloMsg)

#  @a Creating a Sphere
rclarisse.run('ix.cmds.CreateObject("polysphere", "GeometryPolysphere")')


# @a Sets Render to 100%
rclarisse.run('ix.cmds.SetValues(["project://scene/image.resolution_multiplier"], ["2"])')

# @a Sets Render to 50%
rclarisse.run('print "Rendering set to 50%"')
rclarisse.run('ix.cmds.SetValues(["project://scene/image.resolution_multiplier"], ["1"])')


