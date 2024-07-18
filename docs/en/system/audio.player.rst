.. currentmodule:: audio

class Player
============

.. include:: ../refs/system.audio.player.ref

Audio player now can support mp3,amr and wav, if more types are needed, please add the decoder in function audio_player_create.


class audio.Player
------------------

Constructors
------------

.. class:: audio.Player([state_callback])

    Create a Player, state_callback is a monitor of player state, when state changed, this callback will be invoked.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Player.play(uri, pos=0, volume=-1, sync=True, verify=None)

    Play the audio file.

    :param str uri: The uri of the audio file. e.g. "file:///flash/test.mp3", "file:///sd/test.mp3", "https://dl.espressif.com/dl/audio/ff-16b-2c-44100hz.mp3"
    :param int pos: The position to start playing, in byte.
    :param int volume: The volume of the player, 0-100. -1 means the default volume.
    :param bool sync: Whether to play synchronously.
    :param str verify: ssl verify, default is None.

    UIFLOW2:

        |play_local_file.png|

        |play_local_file1.png|

        |play_sdcard_file.png|

        |play_cloud_file.png|


.. method:: Player.play_raw(data, sample=16000, stereo=False, bits=16, pos=0, volume=-1, sync=True)

    Play the raw audio data.

    :param bytes data: The raw audio data.
    :param int sample: The sample rate of the audio data.
    :param bool stereo: Whether the audio data is stereo.
    :param int bits: The bits of the audio data.
    :param int pos: The position to start playing, in byte.
    :param int volume: The volume of the player, 0-100. -1 means the default volume.
    :param bool sync: Whether to play synchronously.

    UIFLOW2:

        |play_raw.png|


.. method:: Player.play_tone(freq, time, volume=-1, sync=True)

    Play a tone.

    :param int freq: The frequency of the tone.
    :param float time: The duration of the tone.
    :param int volume: The volume of the player, 0-100. -1 means the default volume.
    :param bool sync: Whether to play synchronously.

    UIFLOW2:

        |play_tone.png|


.. method:: Player.pause()

    Pause the player.

    UIFLOW2:

        |pause.png|


.. method:: Player.resume()

    Resume the player.

    UIFLOW2:

        |resume.png|


.. method:: Player.stop()

    Stop the player.

    UIFLOW2:

        |stop.png|


.. method:: Player.pos()

    Get the position of the player.

    :return: The position of the player.

    UIFLOW2:

        |pos.png|


.. method:: Player.set_vol(volume)

    Set the volume of the player.

    :param int volume: The volume of the player, 0-100.

    UIFLOW2:

        |set_vol.png|


.. method:: Player.get_vol()

    Get the volume of the player.

    :return: The volume of the player.

    UIFLOW2:

        |get_vol.png|
