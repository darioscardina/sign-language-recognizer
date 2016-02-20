################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import numpy as np
import Leap, sys, thread, time, cmath

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    number_letters = 4
    data_per_letter = 180 #5 fingers * 4 bones * (start, end, direction)

    list_inputs_A = np.load('list_inputs_A.npy')
    list_inputs_B = np.load('list_inputs_B.npy')
    list_inputs_C = np.load('list_inputs_C.npy')
    list_inputs_D = np.load('list_inputs_D.npy')
    list_inputs_E = np.load('list_inputs_E.npy')
    list_inputs = np.concatenate((list_inputs_A[0:10, :], list_inputs_B[0:10, :], list_inputs_C[0:10, :], list_inputs_D[0:10, :],
                                   list_inputs_E[0:10, :]))
    #outputs = np.load('list_outputs.npy')


    id_letter = 0
    pos_id_letter = 0 #stores the number of samples that was colected for each letter
    pos_vector_data = 0
    
    #def check_letter(self, input):
    #    letters = ['A', 'B', 'C', 'D']
    #    id_letter = 0
    #    min_sum = 99999999;
    #    for i in range (20):
    #        sum_of_difference = 0
    #        for j in range (180):
    #            sum_of_difference += abs(self.list_input[i, j] - input[j])
    #        if (sum_of_difference < min_sum):
    #            min_sum = sum_of_difference
    #            id_letter = int(i/5)
    #    print "%d \n\n" % (letters[id_letter])

    def on_init(self, controller):
        print self.list_inputs
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        
        #time.sleep(3)
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:
            palm_center = hand.palm_position

            input = []
            for finger in hand.fingers:


                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    prev_joint = bone.prev_joint
                    next_joint = bone.next_joint
                    direction = bone.direction
                    #Add the normalized positions of the fingers bones to the list of inputs
                    input.append(prev_joint[0]-palm_center[0])
                    input.append(prev_joint[1]-palm_center[1])
                    input.append(prev_joint[2]-palm_center[2])
                    input.append(next_joint[0]-palm_center[0])
                    input.append(next_joint[1]-palm_center[1])
                    input.append(next_joint[2]-palm_center[2])
                    input.append(direction[0]-palm_center[0])
                    input.append(direction[1]-palm_center[1])
                    input.append(direction[2]-palm_center[2])
                    self.pos_vector_data += 9
            
            #self.check_letter(self, input)
            letters = ['A\n\n', 'B\n\n', 'C\n\n', 'D\n\n', 'E\n\n']
            id_letter = 0
            min_variance = 99999999;
            for i in range (0, 50, 1):
                #print "aqui %d \n" % (i)
                average = 0
                for j in range (180):
                        average += abs(self.list_inputs[i, j] - input[j])
                        average = float(average/180)
                variance = 0
                for j in range (180):
                    variance += (self.list_inputs[i, j] - input[j])**2  
                
                variance = variance/average
                if (variance < min_variance):
                    min_variance = variance
                    id_letter = i
                    
            #print "%d  " % (id_letter)
            print (letters[int(id_letter/10)])
            self.pos_vector_data = 0;


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        print "here"
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
