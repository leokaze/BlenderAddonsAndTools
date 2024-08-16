version = "0.0.1"

import os
import subprocess
import time
import re

# time countdown function
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


def get_last_rendered_frame(path):
    last_frame = 0

    # check if the directory exists, if not create it
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        files = os.listdir(path)
        if not files or len(files) == 0:
            raise Exception("No files found in the directory")
        last_file = files[-1]
        # get the last digits from the file name with regex
        digits = re.findall(r'\d+', last_file)
        if len(digits) == 0:
            raise Exception("No digits found in the file name")
        last_frame = int(digits[-1])
        print("LAST FRAME: ", last_frame)
    except Exception as e:
        print("GET LAST FRAME ERROR: ", e)
    finally:
        return last_frame


def render_animation(start_frame, end_frame, output_path, blender_path, blend_file, engine, wait_time=10):
    last_frame = get_last_rendered_frame(output_path)
    try:
        error = True
        error_counter = 0
        start_render_time = time.time()

        if last_frame >= end_frame:
            error = False
            print("RENDER ANIMATION: Animation already rendered")
        elif last_frame > 0 and last_frame < end_frame:
            error_counter += 1
            start_frame = last_frame

        while error:
            command = ''
            command += blender_path
            command += ' --background '
            command += blend_file
            command += ' --engine '
            command += engine
            command += ' --frame-start '
            command += str(start_frame)
            command += ' --frame-end '
            command += str(end_frame)
            command += ' --render-anim'

            print("COMMAND", command)

            # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
            # print(result.stdout.decode("utf-8"))
            subprocess.run(command, shell=True)

            print("REDERER: errors counter: ", error_counter)
            last_frame = get_last_rendered_frame(output_path)
            if last_frame >= end_frame:
                error = False
                print("RENDERER: Animation rendered successfully")
            elif last_frame > 0 and last_frame < end_frame:
                error_counter += 1
                start_frame = last_frame

            countdown(wait_time)

        end_render_time = time.time()
        total_render_time = end_render_time - start_render_time
        # print start and end render time in HH:MM:SS format
        print("RENDER START TIME: ", time.strftime("%H:%M:%S", time.gmtime(start_render_time)))
        print("RENDER END TIME: ", time.strftime("%H:%M:%S", time.gmtime(end_render_time)))
        # print total render time in HH:MM:SS format
        print("RENDER TIME: ", time.strftime("%H:%M:%S", time.gmtime(total_render_time)))
        # print total of errors
        print("RENDERER: Total errors: ", error_counter)

    except Exception as e:
        print("RENDER ANIMATION ERROR: ", e)
    finally:
        return True
