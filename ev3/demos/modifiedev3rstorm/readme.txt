Demos for the modified ev6rstorm. The modifications are:
- touch & color sensors at the end of the arm in place of the "hand".
The color sensor works in the reflection mode and is used for detecting obstacles
(same as IR sensor working in proximity mode). Pressing the touch sensor breaks current demo
(it still can be resumed - how to do it is mentioned below). Launch it with:

python demo.py $VERSION

where $VERSION is either 1, 2 or 3.

Demo 1 & 2 are very similar. In both the robot just "walks around" trying to avoid obstacles. The difference is
in decision making when some obstacle gets in robot's way. In demo 1 it always turns right unless after the turn
it still hits an obstacle. If it's the case it turns 180 degrees (so left comparing to the starting position) and goes
this way unless it's also impossible in which case it turns left again i.e. goes back. In the demo 2 it turns right
tries to check how far the next obstacle is and if nothing is in a sight it goes that way. Otherwise it checks also left
and takes the way on which the next obstacle is further. If both are not good it goes back. The demos are ready when 
the LED starts blinking green. Press Enter to start the demo (also after demo is stopped by pressing the touch sensor).
Back ends demos completely.
In demo 3 it's possible to "tell" the robot where it should go to. The protocol is:
- when the demo is ready LED start blinking green. Press enter to enter the path programming mode (LED changes to ORANGE - still blinking).
In that mode UP, LEFT, RIGHT arrows mean "go straight", "turn left", "turn right" respectively (DOWN is ignored). After pressing an arrow
the mode changes to the move time programming (LED blinks RED in this mode). Time is entered using DOWN key. 1 press means 2 second.
After entering time ENTER has to be pressed to confirm the move. E.g pressing
UP DOWN DOWN DOWN ENTER LEFT DOWN ENTER UP DOWN DOWN DOWN DOWN DOWN ENTER RIGHT DOWN ENTER UP DOWN DOWN ENTER means
"Go straight [UP] for 6 seconds [3 x DOWN], then turn left [LEFT] and make the turn for 2 seconds [DOWN]. Next
go straight [UP] for 10 secs (5 x DOWN), turn right [RIGHT] and the turn should be done for 2 secs [DOWN] and finally
go straight [UP] for 4 secs [2 x DOWN].

Press ENTER again to cause the robot to follow the entered path (Enter also resumes the demo after it is stopped
by pressing the touch sensor). Back ends it completely.