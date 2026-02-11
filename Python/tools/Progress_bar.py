import time
import sys

def progress_bar(total=30, cps=7):
   """
   Draws a progress bar that fills at about the same speed as the GIF.
   cps = characters per second (how fast the bar fills)
   total = total number of steps/blocks in the bar
   """
   delay = 1 / cps

   for i in range(total + 1):
       filled = "#" * i
       empty = "-" * (total - i)
       bar = f"[{filled}{empty}] {int((i/total)*100)}%"
      
       sys.stdout.write("\r" + bar)
       sys.stdout.flush()
       time.sleep(delay)

   print()  # move to new line at the end


# Example usage:
print("Loading…")
progress_bar(total=30, cps=7)
print("Done!")

