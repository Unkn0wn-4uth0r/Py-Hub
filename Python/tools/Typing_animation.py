import time
import sys

def type_like_gif(text, cps=7):
   """
   Types text at approx. the same speed as the iamb demo GIF.
   cps = characters per second (default ~7)
   """
   delay = 1 / cps
   for char in text:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(delay)
   print()

# Example usage:
demo_text = "Welcome to the demo! This is typed at GIF speed."
type_like_gif(demo_text)
