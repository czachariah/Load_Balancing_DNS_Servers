IT Project 2: Load Balancing DNS Servers
READ-ME

0.  Please write down the full names and netids of all your team members.

        Oscar Hong - oh66
        Chris Zachariah - cvz2

1.  Briefly discuss how you implemented the LS functionality of tracking which
    TS responded to the query and timing out if neither TS responded.

        The LS will first receive a URL from the client. That URL is then sent to both
        of the TS servers to query within their respective DNS tables to find an IP address.

        The 'select' command is used by the LS server to wait on the TS servers for 7
        seconds. This command returns special types of descriptors. These descriptors are used by
        LS to read from. The LS server will first try to read from the TS1 descriptor. If nothing can
        be read from the TS1 server's descriptor, then LS will read from TS2 server's descriptor.
        If one of the servers has sent back an IP, that IP is then returned to the client.

        In the case that both the servers do not send back any info, then after 7 seconds, the select command
        will timeout and throw an appropriate timeout descriptor. LS will check for and catch this descriptor and
        send back a 'Error:HOST NOT FOUND' message to the client.

2.  Are there known issues or functions that aren't working currently in your
    attached code? If so, explain.

        No. Our code works as according to the instructions given to us.

3.  What problems did you face developing code for this project?

        We had to figure out a clear and efficient way to correctly wait for the TS servers to send back
        any info. In original design, the LS would wait for each connection to timeout before sending back
        the a 'Error:HOST NOT FOUND' message to the client. This made the process too long and did not complete
        the task at hand. Thus, through careful planning and testing, we decided to used the 'select' command in
        order to get descriptors for reading and timeout. This fixed our efficiency problem and made the program
        run as described in the instructions.

4.  What did you learn by working on this project?

        We learned how to use commands like 'select' in order to work with the Unix-system to read from and wait for
        connections from servers. This new knowledge really helped shape the project as it is and made it efficient.


