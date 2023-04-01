import time

import obsws_python as obs

# list of requests accessible to obsws_python. Just call them in snake case
# https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests


def toggle_fsb_visual(emotion):
    passes = load_websocket_passes()
    cl = obs.ReqClient(host='localhost', port=passes[0], password=passes[1])

    # Duration of how long the source will be enabled before reverting back to hidden
    graphic_duration = 4

    # The streamer chose this name. Change to the name of scene the sources are under
    scene_name = 'StreamingPoop'

    # I know starting with Python 3.10 there are switch statements, but I wrote this in 3.9
    if emotion == 'positive':
        source_name = 'fsbPositive'
    elif emotion == 'negative':
        source_name = 'fsbNegative'
    elif emotion == 'neutral':
        source_name = 'fsbNeutral'
    elif emotion == 'insane':
        source_name = 'fsbInsane'
    else:
        source_name = 'fsbNeutral'

    source_id = cl.get_scene_item_id(scene_name, source_name)

    cl.set_scene_item_enabled('StreamingPoop', source_id.scene_item_id, True)
    time.sleep(graphic_duration)
    cl.set_scene_item_enabled('StreamingPoop', source_id.scene_item_id, False)


def load_websocket_passes():
    with open('.obs-websocket') as f:
        return f.read().splitlines()
