# meraki_clone_same_switch
This project saves the configuration, removes the switch from the network, adds it back, and configures the device and switch as before 


This Python script is intended to remove one or more Meraki switches from the network before saving the configuration and then adding this or these switches back to the network and then configuring them with the same configuration.

The script goes completely independently and searches in the list of organizations the name or the ID as well as on basis of the network names the suitable ID. So this must not be searched out separately in advance.

At the top of the script the variables "organizationname", "networkname", "api_key" & "seriallist" have to be filled.
With the variable "seriallist" the entries of the list must always be written in quotation marks and separated with a comma, except for the last one which does not get a comma.

All other variables are filled by the script itself. The script gives a status code for each operation whether this operation was successful or not.
