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

    list_inputs_A = np.load('database/list_inputs_A.npy')
    list_inputs_B = np.load('database/list_inputs_B.npy')
    list_inputs_C = np.load('database/list_inputs_C.npy')
    list_inputs_D = np.load('database/list_inputs_D.npy')
    list_inputs_E = np.load('database/list_inputs_E.npy')
    list_inputs_F = np.load('database/list_inputs_F.npy')
    list_inputs_G = np.load('database/list_inputs_G.npy')
    list_inputs_H = np.load('database/list_inputs_H.npy')
    list_inputs_I = np.load('database/list_inputs_I.npy')
    list_inputs_K = np.load('database/list_inputs_K.npy')
    list_inputs_L = np.load('database/list_inputs_L.npy')
    list_inputs_M = np.load('database/list_inputs_M.npy')
    list_inputs_N = np.load('database/list_inputs_N.npy')
    list_inputs_O = np.load('database/list_inputs_O.npy')
    list_inputs_P = np.load('database/list_inputs_P.npy')
    list_inputs_Q = np.load('database/list_inputs_Q.npy')
    list_inputs_R = np.load('database/list_inputs_R.npy')
    list_inputs_S = np.load('database/list_inputs_S.npy')
    list_inputs_U = np.load('database/list_inputs_U.npy')
    list_inputs_V = np.load('database/list_inputs_V.npy')
    list_inputs_W = np.load('database/list_inputs_W.npy')
    list_inputs_X = np.load('database/list_inputs_X.npy')
    list_inputs_Y = np.load('database/list_inputs_Y.npy')
    list_inputs = np.concatenate((list_inputs_A[0:10, :], list_inputs_B[0:10, :], list_inputs_C[0:10, :], list_inputs_D[0:10, :],
                                   list_inputs_E[0:10, :], list_inputs_F[0:10, :], list_inputs_G[0:10, :], list_inputs_H[0:10, :],
                                    list_inputs_I[0:10, :],  list_inputs_K[0:10, :],  list_inputs_L[0:10, :], list_inputs_M[0:10, :],
                                        list_inputs_N[0:10, :], list_inputs_O[0:10, :],  list_inputs_P[0:10, :], list_inputs_Q[0:10, :],
                                    list_inputs_R[0:10, :], list_inputs_S[0:10, :], list_inputs_U[0:10, :], list_inputs_V[0:10, :],
                                     list_inputs_W[0:10, :], list_inputs_X[0:10, :], list_inputs_Y[0:10, :]))
    #list_inputs = np.concatenate((list_inputs_A[0:10, :], list_inputs_G[0:10, :], list_inputs_L[0:10, :]))
    #outputs = np.load('list_outputs.npy')


    id_letter = 0
    pos_id_letter = 0 #stores the number of samples that was colected for each letter
    pos_vector_data = 0


    def on_init(self, controller):
        print self.list_inputs
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        #Average a finger position for the last 10 frames

        #time.sleep(3)
        # Get the most recent frame and report some basic information

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        input = np.zeros(180)
        for f in range (0,10):
            self.pos_vector_data = 0
            frame = controller.frame()
            for hand in frame.hands:
                palm_center = hand.palm_position
    
                
                for finger in hand.fingers:
    
    
                    # Get bones
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        prev_joint = bone.prev_joint
                        next_joint = bone.next_joint
                        direction = bone.direction
                        #Add the normalized positions of the fingers bones to the list of inputs
                        input[self.pos_vector_data] += (prev_joint[0]-palm_center[0])
                        input[self.pos_vector_data+1] += (prev_joint[1]-palm_center[1])
                        input[self.pos_vector_data+2] += (prev_joint[2]-palm_center[2])
                        input[self.pos_vector_data+3] += (next_joint[0]-palm_center[0])
                        input[self.pos_vector_data+4] += (next_joint[1]-palm_center[1])
                        input[self.pos_vector_data+5] += (next_joint[2]-palm_center[2])
                        input[self.pos_vector_data+6] += (direction[0]-palm_center[0])
                        input[self.pos_vector_data+7] += (direction[1]-palm_center[1])
                        input[self.pos_vector_data+8] += (direction[2]-palm_center[2])
                        
                        self.pos_vector_data += 9        
            
        input = input/10
            
        #self.check_letter(self, input)
        letters = ['A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ','H ', 'I ', 'K ', 'L ', 'M ', 'N ', 'O ', 'P ', 'Q ', 'R ', 'S ', 'U ', 'V ', 'W ', 'X ', 'Y ']
        #letters = ['A ', 'G ', 'L']
        id_letters = [0, 0, 0]
        min_variances = [99999999, 99999999, 99999999]
        for i in range (0, 230, 1):
            #print "aqui %d \n" % (i)
            average = 0
            count = 0
            for j in range (180):
                #count += 1
                average += abs(self.list_inputs[i, j] - input[j])
                if (count == 6):
                    count = 0
                    j += 3
                
                    
            average = float(average/120)
            variance = 0
            count = 0
            for j in range (180):
                #count += 1
                variance += (self.list_inputs[i, j] - input[j])**2 
                if (count == 6):
                    count = 0
                    j += 3
            
            variance = variance/average

        
            if ( variance < min_variances[0]):
                min_variances[2] = min_variances[1]
                min_variances[1] = min_variances[0]                  
                min_variances[0] = variance
                id_letters[2] = id_letters[1]
                id_letters[1] = id_letters[0]
                id_letters[0] = +i
                
        #print "%d  " % (id_letter)
        print letters[int(id_letters[0]/10)] + letters[int(id_letters[1]/10)]+ letters[int(id_letters[2]/10)] 
        print '\n\n'
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
