
# class Player

Audio player now can support mp3,amr and wav, if more types are needed, please add the decoder in function audio_player_create.

## class audio.Player

## Constructors

### `class audio.Player([state_callback])`

    Create a Player, state_callback is a monitor of player state, when state changed, this callback will be invoked.

## Methods

### `Player.play(uri, pos=0, volume=-1, sync=True, verify=None)`

    Play the audio file.

    - Parameter `uri` (`str`): The uri of the audio file. e.g. "file:///flash/test.mp3", "file:///sd/test.mp3", "https://dl.espressif.com/dl/audio/ff-16b-2c-44100hz.mp3"
    - Parameter `pos` (`int`): The position to start playing, in byte.
    - Parameter `volume` (`int`): The volume of the player, 0-100. -1 means the default volume.
    - Parameter `sync` (`bool`): Whether to play synchronously.
    - Parameter `verify` (`str`): ssl verify, default is None.

### `Player.play_raw(data, sample=16000, stereo=False, bits=16, pos=0, volume=-1, sync=True)`

    Play the raw audio data.

    - Parameter `data` (`bytes`): The raw audio data.
    - Parameter `sample` (`int`): The sample rate of the audio data.
    - Parameter `stereo` (`bool`): Whether the audio data is stereo.
    - Parameter `bits` (`int`): The bits of the audio data.
    - Parameter `pos` (`int`): The position to start playing, in byte.
    - Parameter `volume` (`int`): The volume of the player, 0-100. -1 means the default volume.
    - Parameter `sync` (`bool`): Whether to play synchronously.

### `Player.play_tone(freq, time, volume=-1, sync=True)`

    Play a tone.

    - Parameter `freq` (`int`): The frequency of the tone.
    - Parameter `time` (`float`): The duration of the tone.
    - Parameter `volume` (`int`): The volume of the player, 0-100. -1 means the default volume.
    - Parameter `sync` (`bool`): Whether to play synchronously.

### `Player.pause()`

    Pause the player.

### `Player.resume()`

    Resume the player.

### `Player.stop()`

    Stop the player.

### `Player.pos()`

    Get the position of the player.

    - Returns: The position of the player.

### `Player.set_vol(volume)`

    Set the volume of the player.

    - Parameter `volume` (`int`): The volume of the player, 0-100.

### `Player.get_vol()`

    Get the volume of the player.

    - Returns: The volume of the player.
