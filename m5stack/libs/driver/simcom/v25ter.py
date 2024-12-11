from .common import AT_CMD

(
    "A/",  # Re-issues the Last Command Given
    "ATA",  # Call answer
    "ATD",  # Mobile Originated Call to Dial A Number
    "ATD><n>",  # Originate call from active memory(1)
    "ATD><str>",  # Originate call from active memory(2)
    "ATDL",  # Redial last telephone number used
    "ATE",  # Enable command echo
    "ATH",  # Disconnect existing call
    "ATI",  # Display product identification information
    "ATL",  # Set monitor speaker loudness
    "ATM",  # Set monitor speaker mode
    "+++",  # Switch from data mode to command mode
    "ATO",  # Switch from command mode to data mode
    "ATP",  # Select pulse dialling
    "ATQ",  # Set Result Code Presentation Mode
    "ATS0",  # Set number of rings before automatically answering the call
    "ATS3",  # Set command line termination character
    "ATS4",  # Set response formatting character
    "ATS5",  # Set command line editing character
    "ATS6",  # Pause before blind dialling
    "ATS7",  # Set number of seconds to wait for connection completion
    "ATS8",  # Set number of seconds to wait for comma dial modifier encountered in dial string of D command
    "ATS10",  # Set disconnect delay after indicating the absence of data carrier
    "ATT",  # Select tone dialing
    "ATV",  # TA response format
    "ATX",  # Set connect result code format and monitor call progress
    "ATZ",  # Restore the user setting from ME
    "AT&C",  # Set DCD function mode
    "AT&D",  # Set DTR function mode
    "AT&F",  # Factory defined configuration
    "AT&V",  # Display current configuration
    "AT&W",  # Save the user setting to ME
    "AT+GCAP",  # Request overall capabilities
    "AT+GMI",  # Request manufacturer identification
    "AT+GMM",  # Request TA model identification
    "AT+GMR",  # Request TA revision identification of software release
    "AT+GOI",  # Request global object identification
    "AT+GSN",  # Request TA serial number identification (IMEI)
    "AT+ICF",  # Set TE-TA control character framing
    "AT+IFC",  # Set TE-TA local data flow control
    "AT+IPR",  # Set TE-TA fixed local rate
    "AT+HVOIC",  # Disconnect Voice Call Only
)


class V25Ter:
    def __init__(self):
        pass
