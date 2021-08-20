

import PulseblasterClassObjects as pb

Thingy1=pb.PulseBlaster()


# create a basic pulse blaster sequence
'''
Thingy1.ResetProg()
Thingy1.WriteCommand([2], 0, 5000)
Thingy1.InsertCommand([], 0, 1000,1)
Thingy1.InsertCommand([2], 0, 5000,2)
Thingy1.InsertCommand([], 6, 1000,3)
Thingy1.ViewProg()
'''

# To create a looped sequence in the pulse blaster. 
'''
Thingy1.ResetProg()
Thingy1.WriteCommand([0,1], 2, 1, 3) # 1us Trigger for AFG and AWG and Loop
Thingy1.WriteCommand([], 0, 30*1e6) # Do nothing for duration of Burn
Thingy1.WriteCommand([], 3, 15000,0)  # waiting in us and end the loop
Thingy1.WriteCommand([6,2], 0, 20*1e6) # Trigger 6 AWG for read, and scope for the duration of the read pulse
Thingy1.WriteCommand([], 1, 5000) # Do Nothing. 
Thingy1.ViewProg()
'''

# Create and edit the sequence of the pulse blaster. 
'''
Thingy1.ResetProg()
Thingy1.WriteCommand([2], 2, 100,3)
Thingy1.WriteCommand([], 3, 100,0)
Thingy1.WriteCommand([2], 2, 300, 3)
Thingy1.WriteCommand([], 3, 100,2)
Thingy1.WriteCommand([], 6, 500)
Thingy1.WriteProg()
Thingy1.ViewProg()
'''
#Thingy1.PopCommand(2)
#Thingy1.WriteProg()
# Start the sequence of the pulseblaster running, Wait for Key Press, then stop it. 
Thingy1.Start()
print("Continuing will stop program execution\n");
input("Please press a key to continue.")
Thingy1.Stop()

#Close the pulse blaster
Thingy1.Close()




