def convert_time_string_to_second(runtime):
    runtime = runtime.split()
    if len(runtime) >2:
        runtimeToSecond = int(runtime[0])*3600 + int(runtime[2])*60
    else:
        runtimeToSecond = int(runtime[0])*60
    return runtimeToSecond