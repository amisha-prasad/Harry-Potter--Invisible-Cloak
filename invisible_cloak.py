import cv2
import numpy as np

def main():
    # Capture video from the default webcam
    cap = cv2.VideoCapture(0)

    # Allow the camera to warm up
    print("Please wait for a few seconds...")

    # Capture the background for 60 frames (for a clean background)
    for _ in range(60):
        ret, background = cap.read()
    background = np.flip(background, axis=1)  # Flip the background

    # Ask for the color that should be made invisible
    color_to_hide = input("Enter the color to hide (red/blue/green): ").strip().lower()
    print(f"You entered: {color_to_hide}")

    # Define color range based on input
    if color_to_hide == 'red':
        lower_bound = np.array([0, 120, 70])
        upper_bound = np.array([10, 255, 255])
        lower_bound2 = np.array([170, 120, 70])
        upper_bound2 = np.array([180, 255, 255])
    elif color_to_hide == 'blue':
        lower_bound = np.array([94, 80, 2])
        upper_bound = np.array([126, 255, 255])
    elif color_to_hide == 'green':
        lower_bound = np.array([40, 40, 40])
        upper_bound = np.array([70, 255, 255])
    else:
        print("Color not recognized! Choose red, blue, or green.")
        cap.release()
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally (mirror effect)
        frame = np.flip(frame, axis=1)

        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Generate masks for the specified color
        if color_to_hide == 'red':
            mask1 = cv2.inRange(hsv, lower_bound, upper_bound)
            mask2 = cv2.inRange(hsv, lower_bound2, upper_bound2)
            mask = mask1 + mask2
        else:
            mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Refine the mask (remove noise)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))

        # Create an inverse mask to capture the area without the chosen color
        inverse_mask = cv2.bitwise_not(mask)

        # Segment out the area with the chosen color and replace it with the background
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=inverse_mask)

        # Combine the two results to create the final output
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Display the output
        cv2.imshow("Invisible Cloak", final_output)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
