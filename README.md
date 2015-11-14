# netmo
<p>
NetMo is a Python implementation of a network sniffer, with a dynamic HTML user interface for monitoring network activity. It is designed to provide server administrators with a high-level real-time overview of network activity, identifying hosts which are connecting to
the server, indicating which ports are being used, and displaying readable samples of the data sent and received by the server.   
</p>

<p>
<br>
<img class="centered fancyimage" src="http://codebox.org.uk/graphics/netmo.png" alt="NetMo web interface"/>
<br>
</p>

<p>
NetMo works nicely on Linux. I have tested it on OSX, and although it runs it doesn't capture any packets. I'm pretty sure there is no chance it will work on Windows.
</p>

<p>
The utility uses a <a href="http://en.wikipedia.org/wiki/Raw_socket">raw socket</a> to detect network packets, and therefore does not require any third-party packet-capture libraries
(the technique is very well explained by <a href="http://www.binarytides.com/python-packet-sniffer-code-linux/">Binary Tides</a>). 
</p>

<p>
The web interface takes advantage of the HTML5 capabilities of modern web-browsers, and no effort has been made to provide compatibility with legacy clients (if you have read this far you probably aren't using Internet Explorer 6). 
Packet data is streamed to the browser over a single persistent network connection using <a href="https://developer.mozilla.org/en-US/docs/Server-sent_events/Using_server-sent_events">Server-Sent Events</a>, and a second connection is used
to report the results of reverse DNS lookups which are automatically performed against each remote IP address which connects to the server. 
</p>
