# arp-spoof
A python 2.7 program written to manipulate protocols on layer 2 of OSI model. It effectively places you as MITM in connection. 

## Getting Started
To run this program, you should already be in the network (wireless or wired). This program effectively updates the ARP tables on both the router and the target. 

## Running the program
Written in python 2.7, make sure to use the appropriate interrupter. You should know the IPs of router and target. Do an Nmap scan if unknown.

## Example usage
python ARP_spoof.py --ip 192.168.0.10 --router 192.168.0.1 --victim 192.168.0.10

## Attention
Please do not use this program where unauthorized.

## Credits

|                                      |             |
| ------------------------------------ | ----------- |
| **Author**                           | @bryanwei   |

## License
See the [LICENSE](https://github.com/bryanweielio/arp-spoof/blob/master/LICENSE) file.
